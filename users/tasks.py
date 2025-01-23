from celery import shared_task
from wallet.models import Wallet
from currency.models import Currency
from django.contrib.auth import get_user_model


User = get_user_model()
"""When a new currency is created, create currency wallet for every user"""
@shared_task
def create_wallets_for_currency(currency_id):
    currency = Currency.objects.get(id=currency_id)
    users = User.objects.all()
    
    for user in users:
        Wallet.objects.create(
            user=user,
            currency=currency,
            balance=0,
            in_orders_balance=0,
            in_futures_balance=0,
            in_withdraw_balance=0,
        )




"""
This signal create Coin/Currency wallet for any new user 
"""
@shared_task
def create_wallets_for_user(user_id):
    user = User.objects.get(id=user_id)  # Get the user instance
    currencies = Currency.objects.all()

    for currency in currencies:
        Wallet.objects.create(
            user=user,
            currency=currency,
            balance=0,
            in_orders_balance=0,
            in_futures_balance=0,
            in_withdraw_balance=0,
        )

