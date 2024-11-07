"""
ASGI config for django_delivery project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_delivery.settings')

application = get_asgi_application()


''' Входные данные
{ 
    "name": "Одежда",
    "weight": "2.50",
    "content_value_usd": "100.00",
    "parcel_type_name": "Одежда"
}
'''