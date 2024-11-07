from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_delivery.settings')

app = Celery('django_delivery')
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/1'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['registration'])

app.conf.beat_schedule = {
    'update_delivery_cost_every_5_minutes': {
        'task': 'registration.tasks.update_delivery_cost',
        'schedule': crontab(minute='*/5'),
    },
}
