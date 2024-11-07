import uuid

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, filters
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from common.models import UserSession
from .models import Parcel, ParcelType
from .serializers import ParcelSerializer, ParcelTypeSerializer


class ParcelViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):

    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'parcel_type': ['exact'],
        'delivery_cost_rub': ['isnull'],
    }
    ordering_fields = '__all__'
    ordering = ['registered_at']

    @action(methods=['get'], detail=False)
    def types(self, request):
        """Возвращает список всех типов посылок."""
        parcel_types = ParcelType.objects.all()
        serializer = ParcelTypeSerializer(parcel_types, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Создаёт новую посылку, связывая её с текущей сессией."""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        session_id = request.session_id
        parcel = serializer.save(session_id=session_id)
        response = Response({'id': parcel.id}, status=status.HTTP_201_CREATED)
        if not request.COOKIES.get('session_id'):
            response.set_cookie('session_id', session_id)  # Устанавливаем cookie, если его нет

        return response

    def retrieve(self, request, *args, **kwargs):
        """Возвращает информацию о посылке по её ID и проверяет корректность сессии."""
        session_id_str = request.COOKIES.get('session_id')
        parcel_id = kwargs.get('pk')

        if not parcel_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            parcel = Parcel.objects.get(id=parcel_id)
        except Parcel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            session_id = uuid.UUID(session_id_str)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if parcel.session_id != session_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(parcel)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Возвращает список посылок, относящихся к текущей сессии."""
        session_id = request.COOKIES.get('session_id')

        if not session_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        parcels = Parcel.objects.filter(session_id=session_id)
        parcels = self.filter_queryset(parcels)
        page = self.paginate_queryset(parcels)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(parcels, many=True)
        return Response(serializer.data)
