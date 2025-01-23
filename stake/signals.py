from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from datetime import timedelta
from .models import Stake
from decimal import Decimal

User = get_user_model()


"""
Post save signal that deduct the stake amount from the user wallet
"""
@receiver(post_save, sender=Stake)
def deduct_stake_amount(sender, instance, created, **kwargs):
    if created:
        # Deducting the stake amount from the user's wallet
        instance.staking_wallet.available_balance -= instance.stake_amount
        instance.staking_wallet.save()



@receiver(pre_save, sender=Stake)
def fill_stake_details(sender, instance, **kwargs):
    if not instance.id:
        # Set the stake outcome from the user model
        instance.stake_outcome = instance.user.stake_outcome
        instance.end_date = instance.start_date + timedelta(days=instance.stake_duration.duration_days)
        instance.estimated_return = Decimal((100+instance.stake_duration.percentage_return)/100)*instance.stake_amount
