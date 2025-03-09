import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HHanalyzer.settings')

app = Celery('HHanalyzer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'fetch_vacancies': {
        'task': 'skills_stats.tasks.fetch_vacancies_task',
        'schedule': crontab(minute='*/10'),
    },
}
