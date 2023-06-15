from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Action, Door, Breaking


# @receiver(post_save, sender=Action)
# def append_response(sender, instance, **kwargs):
#     door = Door.objects.get(id=instance.door.id)
#     door.is_open = instance.is_open
#     door.history.add(instance)

#     door.save()

#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "mk",
#         {
#             "type": "send_action",
#             "message": "open" if instance.is_open == True else "close",
#         },
#     )


@receiver(post_save, sender=Breaking)
def append_response(sender, instance, **kwargs):
    door = Door.objects.get(id=instance.door.id)
    door.breaking_history.add(instance)

    door.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "bot",
        {
            "type": "send_action",
            "message": "thief",
        },
    )
