from celery import shared_task
from .models import Deposit
from .crypto_interface import check_crypto_balance
from django.core.management import call_command


#Putting management command as a shared task, to be run periodically
@shared_task
def run_check_trades():
    call_command('check_trades')

@shared_task
def monitor_deposits():
    deposits = Deposit.objects.filter(deposit_status='pending', deposit_type='manual')
    for deposit in deposits:
        try:
            balance = check_crypto_balance(deposit.wallet.currency.symbol, deposit.wallet_address_pay_to)
            if balance > 0:
                deposit.amount = balance
                deposit.deposit_status = 'confirmed'
                deposit.save()

                deposit.wallet.balance += balance
                deposit.wallet.save()
        except Exception as e:
            print(f"Error processing deposit: {e}")


@shared_task
def send_email(subject, message, recipient):
    # Code to send email
    pass

# from celery import shared_task
# from .models import Deposit
# from .crypto_interface import check_crypto_balance
# from .crypto_handlers.ethereum import move_to_central_wallet

# @shared_task
# def monitor_deposits():
#     deposits = Deposit.objects.filter(deposit_status='pending', deposit_type='manual')
#     for deposit in deposits:
#         try:
#             balance = check_crypto_balance(deposit.wallet.currency.symbol, deposit.wallet_address_pay_to)
#             if balance > 0:
#                 deposit.amount = balance
#                 deposit.deposit_status = 'confirmed'
#                 deposit.save()

#                 deposit.wallet.balance += balance
#                 deposit.wallet.save()

#                 # Move ETH to central wallet
#                 if deposit.wallet.currency.symbol == 'ETH':
#                     private_key = get_private_key_for_address(deposit.wallet_address_pay_to)  # Implement securely
#                     move_to_central_wallet(private_key, settings.CENTRAL_WALLET_ADDRESS, balance)
#         except Exception as e:
#             print(f"Error processing deposit: {e}")








@shared_task
def my_task():
    # Your task code here
    print("YES CELERY IS WORKING !!! ")
    print("YES CELERY IS WORKING !!! ")
    print("YES CELERY IS WORKING !!! ")


@shared_task
def generate_report(data):
    # Code to generate report
    pass