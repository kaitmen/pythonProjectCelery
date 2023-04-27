import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail

from authors.models import Category

logger = logging.getLogger(__name__)

def weekly_send_mail():
    one_week_ago = datetime.today() - datetime.timedelta(days=7)

    categories = Category.objects.all()
    for c in categories:
        count = c.posts_set.filter(created_at__gte=one_week_ago).count()
        if count > 0 and len(c.get_subscribers) > 0:

            send_mail(
                'Was added new article to your categories!',
                'hello from news portal!',
                from_email='peterbadson@yandex.ru',
                recipient_list=c.get_subscribers,
            )



def my_job():
    send_mail(
        'Job mail',
        'hello from job!',
        from_email='peterbadson@yandex.ru',
        recipient_list=['skavik46111@gmail.com'],
    )


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
        id = "my_job",
             max_instances = 1,
                             replace_existing = True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            weekly_send_mail,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="weekly_send_mail",
            max_instances=1,
            replace_existing=True,
        )

        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")