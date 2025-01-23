from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import CopyTrader

@receiver(m2m_changed, sender=CopyTrader.copiers.through)
def update_no_copiers(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        instance.no_copiers += len(pk_set)
        instance.save()
    elif action == 'post_remove':
        instance.no_copiers -= len(pk_set)
        instance.save()
