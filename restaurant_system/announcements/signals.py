from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from reservations.models import Announcement

@receiver(post_save, sender=Announcement)
def announce_update(sender, instance, created, **kwargs):
    if not instance.is_active:
        return
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "announcements",
        {
            "type": "announcement.event",
            "data": {
                "title": instance.title,
                "message": instance.message,
                "priority": instance.priority,
                "created_at": instance.created_at.isoformat(),
            },
        },
    )
