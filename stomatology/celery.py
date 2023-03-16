import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stomatology.settings')

app = Celery('stomatology')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_user_token_every_day': {
        'task': 'employee.tasks.delete_user_token_every_day',
        # Начало времени выполнения зависит от настройки CELERY_TIMEZONE
        'schedule': crontab(hour=7, minute=0),
    }
}
