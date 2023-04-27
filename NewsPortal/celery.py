import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()




app.conf.beat_schedule = {
    'send_every_monday': {
        'task': 'tasks.send_mail_every_monday_to_subscribers',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': (),
    },
}