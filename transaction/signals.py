from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Trade, Swap, Deposit, Withdrawal, Transaction

from wallet.tasks import run_check_trades

@receiver(post_save, sender=Trade)
@receiver(post_save, sender=Swap)
@receiver(post_save, sender=Deposit)
@receiver(post_save, sender=Withdrawal)
def create_transaction(sender, instance, created, **kwargs):
	# Trigger the Celery task
	run_check_trades.delay()
	if created:
		# Create a Transaction instance when a new instance of Trade, Swap, Deposit, or Withdrawal is created
		Transaction.objects.create(
			user=instance.user,
			transaction_type=instance._meta.verbose_name.lower(),  # Use model's verbose name as transaction type
			amount=instance.amount,
			currency=instance.currency,
			# Add more fields specific to each transaction type as needed
		)
