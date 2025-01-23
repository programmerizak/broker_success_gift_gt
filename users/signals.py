# signal.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from currency.models import Currency
from wallet.models import Wallet
from users.tasks import create_wallets_for_currency,create_wallets_for_user

User = get_user_model()

"""
This signal create Coin/Currency wallet for any new user 
"""
@receiver(post_save, sender=User)
def create_user_wallets(sender, instance, created, **kwargs):
    """
    Signal handler to create all available Currency wallets for a new user.
    """
    if created:
        create_wallets_for_user.delay(instance.id)  # Call the Celery task


"""Create wallet for every user when a new currency is added"""
@receiver(post_save, sender=Currency)
def create_currency_wallets(sender, instance, created, **kwargs):
    """
    Signal handler to create a Wallet for all users when a new Currency is created.
    """
    if created:
        create_wallets_for_currency.delay(instance.id)  # Call the Celery task




################# WORKING PERFECTLY BUT NOT USING CELERY
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from currency.models import Currency
# from wallet.models import Wallet

# User = get_user_model()


# @receiver(post_save, sender=Currency)
# def create_currency_wallets(sender, instance, created, **kwargs):
#     """
#     Signal handler to create a Wallet for all users when a new Currency is created.
#     """
#     if created:
#         users = User.objects.all()
#         for user in users:
#             Wallet.objects.create(
#                 user=user,
#                 currency=instance,
#                 balance=0,
#                 in_orders_balance=0,
#                 in_futures_balance=0,
#                 in_withdraw_balance=0,
#             )



