from django.utils.deprecation import MiddlewareMixin
from .models import UserSession
import uuid


class SessionMiddleware(MiddlewareMixin):
    """
    Middleware для обработки сессий пользователей. Проверяет наличие session_id в cookies. Если его нет,
    генерирует новый и сохраняет в cookies и базе данных.
    """
    def process_request(self, request):
        session_id = request.COOKIES.get('session_id')

        if not session_id:
            session_id = str(uuid.uuid4())
            request.session_id = session_id

        UserSession.objects.update_or_create(session_id=session_id)

        request.session_id = session_id
