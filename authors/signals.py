from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post
from .tasks import send_mail_after_create_article, send_mail_after_delete_post


@receiver(post_save, sender=Post)
def notify_managers_post(sender, instance, created, **kwargs):
    send_mail_after_create_article.delay(instance.id, created)


@receiver(post_delete, sender=Post)
def notify_managers_post_delete(sender, instance, created, **kwargs):
    send_mail_after_delete_post.delay(instance.id, created)