from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.models import Notification
from apps.notification.services.dispatcher import NotificationDispatcher


@receiver(post_save, sender=Notification)
def handle_notification(sender, instance, created, **kwargs):
    if created and instance.send_notify:
        NotificationDispatcher.dispatch(instance)
