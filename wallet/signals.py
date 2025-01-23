from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


from .models import Wallet, Withdrawal, Deposit
from currency.models import Currency

User = get_user_model()


"""
Reduce wallet balance when a withdrawal is created and send email (DONE)
"""
@receiver(post_save, sender=Withdrawal)
def reduce_wallet_balance(sender, instance, created, **kwargs):
    if created:
        wallet = instance.wallet
        wallet.balance -= instance.amount
        wallet.save()
        #-------- USER-------------#
        user = instance.user
        user.last_withdrawal = f"{instance.amount} {instance.wallet.currency.symbol}"
        user.save()
        ######### UNCOMMENT WHEN PORT IS OPEN
        #Send email notification to user
        subject = 'Withdrawal Notification'
        html_message = render_to_string('wallet/email/withdrawal_email.html', 
            {'amount': instance.amount, 'status': instance.status, 'symbol':wallet.currency.symbol})
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, f'{settings.DEFAULT_FROM_EMAIL}', [instance.user.email], html_message=html_message)

# ##### old fully functional
# """
# Reduce wallet balance when a withdrawal is created and send email (DONE)
# """
# @receiver(post_save, sender=Withdrawal)
# def reduce_wallet_balance(sender, instance, created, **kwargs):
#     if created:
#         wallet = instance.wallet
#         wallet_type = instance.wallet.wallet_type

#         with transaction.atomic():
#             if wallet_type == 'available':
#                 wallet.balance -= instance.amount
#             elif wallet_type == 'in_orders':
#                 wallet.in_orders_balance -= instance.amount
#             elif wallet_type == 'in_futures':
#                 wallet.in_futures_balance -= instance.amount
#             elif wallet_type == 'in_withdraw':
#                 wallet.in_withdraw_balance -= instance.amount
#             wallet.save()

#             ######### UNCOMMENT WHEN PORT IS OPEN
#             #Send email notification to user
#             subject = 'Withdrawal Notification'
#             html_message = render_to_string('wallet/email/withdrawal_email.html', 
#                 {'amount': instance.amount, 'status': instance.status, 'symbol':wallet.currency.symbol})
#             plain_message = strip_tags(html_message)
#             send_mail(subject, plain_message, f'{settings.DEFAULT_FROM_EMAIL}', [instance.user.email], html_message=html_message)


"""
Refund wallet balance when Withdrawal is change to cancel and also send email (DONE)
"""
@receiver(pre_save, sender=Withdrawal)
def refund_wallet_balance(sender, instance, **kwargs):
    if instance.pk:  # Check if the instance has already been saved (i.e., it's not a new instance)
        original_withdrawal = Withdrawal.objects.get(pk=instance.pk)
        #only reverse amount if the previous state is not cancel and the new state is cancel
        if original_withdrawal.status != 'cancelled' and instance.status == 'cancelled':
            wallet = instance.wallet
            wallet.balance += original_withdrawal.amount
            wallet.save()
        
            ######### UNCOMMENT WHEN PORT HAS BEEN OPEN
            # Send email notification to user
            subject = 'Withdrawal Cancellation Notification'
            html_message = render_to_string('wallet/email/withdrawal_cancellation_email.html', 
                {'amount': original_withdrawal.amount,'symbol':wallet.currency.symbol})
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, f'{settings.DEFAULT_FROM_EMAIL}', [instance.user.email], html_message=html_message)


#### OLD FULLY FUNCTIONAL
# """
# Refund wallet balance when Withdrawal is change to cancel and also send email (DONE)
# """
# @receiver(pre_save, sender=Withdrawal)
# def refund_wallet_balance(sender, instance, **kwargs):
#     if instance.pk:  # Check if the instance has already been saved (i.e., it's not a new instance)
#         original_withdrawal = Withdrawal.objects.get(pk=instance.pk)
#         #only reverse amount if the previous state is not cancel and the new state is cancel
#         if original_withdrawal.status != 'cancelled' and instance.status == 'cancelled':
#             wallet = instance.wallet
#             wallet_type = instance.wallet.wallet_type

#             with transaction.atomic():
#                 if wallet_type == 'available':
#                     wallet.balance += original_withdrawal.amount
#                 elif wallet_type == 'in_orders':
#                     wallet.in_orders_balance += original_withdrawal.amount
#                 elif wallet_type == 'in_futures':
#                     wallet.in_futures_balance += original_withdrawal.amount
#                 elif wallet_type == 'in_withdraw':
#                     wallet.in_withdraw_balance += original_withdrawal.amount
#                 wallet.save()
#                 ######### UNCOMMENT WHEN PORT HAS BEEN OPEN
#                 # Send email notification to user
#                 subject = 'Withdrawal Cancellation Notification'
#                 html_message = render_to_string('wallet/email/withdrawal_cancellation_email.html', 
#                     {'amount': original_withdrawal.amount,'symbol':wallet.currency.symbol})
#                 plain_message = strip_tags(html_message)
#                 send_mail(subject, plain_message, f'{settings.DEFAULT_FROM_EMAIL}', [instance.user.email], html_message=html_message)


"""
Send Email when Deposit is created (DONE)
"""
@receiver(post_save, sender=Deposit)
def handle_deposit_creation(sender, instance, created, **kwargs):
    if created:
        ########### UNCOMMENT WHEN PORT IS OPEN
        # 1. Send email notification
        subject = f"New Deposit Made - Deposit ID: 5xxxxxxxxxx{instance.id}"
        message = render_to_string('wallet/email/deposit_created_email.html', {'deposit': instance})
        recipient_email = instance.user.email
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
        #---------- USER UPDATE-------------------#



        # 2. Increment wallet balance if deposit status is confirmed
        if instance.deposit_status == 'confirmed':
            instance.wallet.balance += instance.amount
            instance.wallet.save()

            #-------- USER-------------#
            user = instance.user
            user.last_deposit = f"{instance.amount} {instance.wallet.currency.symbol}"
            user.save()


"""
If updated from pending to confirm, Increase balance and also send email(DONE)
"""
@receiver(pre_save, sender=Deposit)
def handle_deposit_status_update(sender, instance, **kwargs):
    if instance.pk: # Check if the instance has already been saved (i.e., it's not a new instance)
        original_deposit = Deposit.objects.get(id=instance.pk)
        #only credit amount if the previous status is pending  and the new state is confirmed
        if original_deposit.deposit_status == 'pending' and instance.deposit_status == 'confirmed':  
            # Increment user wallet balance and send email notification
            instance.wallet.balance += instance.amount
            instance.wallet.save()
            #-------- USER-------------#
            user = instance.user
            user.last_deposit = f"{instance.amount} {instance.wallet.currency.symbol}"
            user.save()

            ############ OPEN BACK WHEN PORT OPEN
            subject = "Deposit Confirmed"
            message = render_to_string('wallet/email/deposit_confirmed_email.html', {'deposit': instance})
            recipient_email = instance.user.email
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [recipient_email])



"""
Only send email when user deposit is rejected
"""
######### UNCOMMENT BACK WHEN PORT IS OPEN
@receiver(post_save, sender=Deposit)
def handle_deposit_rejected(sender, instance, created, **kwargs):
    if not created and instance.deposit_status == 'rejected':
        # Send email notification for rejected deposit
        subject = "Deposit Rejected"
        message = render_to_string('wallet/email/deposit_rejected_email.html', {'deposit': instance})
        recipient_email = instance.user.email
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

