from rest_framework import serializers
from .models import Parcel, ParcelType


class ParcelSerializer(serializers.ModelSerializer):
    parcel_type_name = serializers.CharField(write_only=True)
    parcel_type = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Parcel
        fields = ['name', 'weight', 'content_value_usd', 'parcel_type_name', 'parcel_type', 'registered_at',
                  'delivery_cost_rub', 'id']

    def create(self, validated_data):
        """Создаёт новую посылку, связывая её с типом посылки, указанным в `parcel_type_name`."""
        parcel_type_name = validated_data.pop('parcel_type_name')
        try:
            parcel_type = ParcelType.objects.get(name=parcel_type_name)
        except ParcelType.DoesNotExist:
            raise serializers.ValidationError({"parcel_type_name": "Указанный тип посылки не найден."})

        parcel = Parcel.objects.create(parcel_type=parcel_type, **validated_data)
        return parcel

    def update(self, instance, validated_data):
        """Обновляет существующую посылку, меняя её данные, включая тип посылки."""
        parcel_type_name = validated_data.pop('parcel_type_name')
        try:
            parcel_type = ParcelType.objects.get(name=parcel_type_name)
        except ParcelType.DoesNotExist:
            raise serializers.ValidationError({"parcel_type_name": "Указанный тип посылки не найден."})

        instance.name = validated_data.get('name', instance.name)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.content_value_usd = validated_data.get('content_value_usd', instance.content_value_usd)
        instance.parcel_type = parcel_type
        instance.registered_at = validated_data.get('registered_at', instance.registered_at)
        instance.save()
        return instance


class ParcelTypeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ParcelType."""
    class Meta:
        model = ParcelType
        fields = '__all__'
