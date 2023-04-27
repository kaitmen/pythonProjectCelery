from datetime import datetime, timedelta
from django.core.mail import mail_managers, send_mail
from celery import shared_task
import time

from .models import Category, Post


@shared_task
def send_mail_after_create_article(instance_id, created):
    instance = Post.objects.get(pk=instance_id)
    if created:
        subject = f'{instance.title} {instance.created_at.strftime("%d %m %Y")}'
    else:
        subject = f'Post changed for {instance.title} {instance.created_at.strftime("%d %m %Y")}'

    message = f'Post created: {instance.title}. Description: {instance.text}'
    mail_managers(
        subject=subject,
        message=message,
    )


@shared_task
def send_mail_after_delete_post(instance_id, created):
    instance = Post.objects.get(pk=instance_id)
    if created:
        subject = f'{instance.title} {instance.created_at.strftime("%d %m %Y")}'
    else:
        subject = f'Post deleted for {instance.title} {instance.created_at.strftime("%d %m %Y")}'

    message = f'Post created: {instance.title}. Description: {instance.text}'
    mail_managers(
        subject=subject,
        message=message,
    )

@shared_task
def send_mail_every_monday_to_subscribers():
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