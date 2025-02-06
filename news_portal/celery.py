import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')
app = Celery('news_portal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-weekly-newsletter': {
        'task': 'news.tasks.send_weekly_newsletter',
        'schedule': crontab(day_of_week='mon', hour=8, minute=0),  # Каждый понедельник в 8:00
    },
}