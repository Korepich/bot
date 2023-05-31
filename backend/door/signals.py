from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Action, Door

@receiver(post_save, sender=Action)
def append_response(sender, instance, **kwargs):
    door = Door.objects.get(id=instance.door.id)
    door.is_open = instance.is_open
    door.history.add(instance)

    door.save()
