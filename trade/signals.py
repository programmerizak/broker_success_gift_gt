from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Trade
from decimal import Decimal
import datetime
import random





"""
This signal set the trade_outcome to the value from the user model if the object is just
created, it also update the value end_time variable in model
"""
@receiver(pre_save, sender=Trade)
def do_these_before_save(sender, instance, **kwargs):
    if not instance.pk:  # Check if the object is being created
        # Set trade_outcome based on the user's win_trades field
        instance.trade_outcome = instance.user.trade_outcome
        instance.end_time = instance.start_time + datetime.timedelta(minutes=instance.duration)
        
        # Calculate expected payout based on the amount traded and percentage gain
        percentage_gain = Decimal(random.randint(10, 90)) / Decimal(100)
        instance.expected_payout = instance.trading_amount + (instance.trading_amount * percentage_gain)






"""
Post save signal that
1. Set the expeced_payout variable, using random percentage and the trading_amount
2. Deduct the amount traded from the user wallet
"""
@receiver(post_save, sender=Trade)
def update_trade_details(sender, instance, created, **kwargs):
	if created:

		# Deducting the traded amount from the user's wallet
		instance.wallet.balance -= instance.trading_amount
		instance.wallet.save()


