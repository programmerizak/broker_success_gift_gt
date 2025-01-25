from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .models import Wallet,Withdrawal,WalletConnected,Deposit
from .forms import WithdrawalForm, WalletConnectionForm, DepositForm,SwapForm
from currency.models import Currency
from django.utils import timezone
# THRID PARTY IMPORT #
import requests, json, sweetify
from decimal import Decimal
import sweetify
import json
from .crypto_interface import generate_crypto_address
#############
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Wallet, Deposit, GeneratedWalletAddress
from .crypto_interface import generate_crypto_address
from wallet.tasks import run_check_trades

import logging
logger = logging.getLogger(__name__)



# BASIC
BASE_API_URL = 'https://rest.coinapi.io/v1/'
COIN_API_KEY = settings.COIN_API_KEY
LIVE_COIN_WATCH_API_KEY = settings.LIVE_COIN_WATCH_API_KEY


@login_required
def swap(request):
	context = {'page_title':'Swap Coin'}
	user = request.user
	if request.method == "POST":
		form = SwapForm(request.POST)
		if form.is_valid():
			from_coin = form.cleaned_data.get("from_coin")
			to_coin = form.cleaned_data.get("to_coin")
			amount_entered = form.cleaned_data.get("from_amount")
			#----------------------------------------------------------------------#
			wallet_selected = Wallet.objects.get(user=user,currency__symbol=from_coin)
			if amount_entered > wallet_selected.balance:
				# sweetify.error(request, f"You can't swap more than your available balance {wallet_selected.balance}")
				sweetify.error(
					request,
					"Swap Unsuccessfully",
					text=f"You can't swap more than your available balance {wallet_selected.balance}",
					persistent="Close",
				)

				return redirect("wallet:swap")

			result = get_rate(from_coin,to_coin)
			fromm = from_coin,
			to = to_coin,
			rate = result
			context.update({
				'from':fromm,
				'to':to,
				'rate':rate
			})
			if request.htmx:
				return render(request,"wallet/partials/rate.html",context)
			#Do actual swap
			### Deduct the amount swap from the wallet
			wallet_selected.balance -= amount_entered
			wallet_selected.save()
			to_wallet = Wallet.objects.get(user=user,currency__symbol=to_coin)
			to_wallet.balance += amount_entered*Decimal(result)
			to_wallet.save()
			sweetify.success(
					request,
					"Swap Done Successfully",
					text=f"{result} {to[0]} has been added to your {to[0]} wallet",
					persistent="Close",
				)
			return redirect("wallet:swap")

	form = SwapForm()
	context['form'] = form
	return render(request, "wallet/swap.html", context)


def get_rate(asset_id_base,asset_id_quote):
	context = {'page_title':"Done Swapping"}
	#------------------------------------------------------------ #
	url = F"https://rest.coinapi.io/v1/exchangerate/{asset_id_base}/{asset_id_quote}"
	payload={}
	headers = {
	  'Accept': 'text/plain',
	  'X-CoinAPI-Key': f'{COIN_API_KEY}'
	}
	response = requests.request("GET", url, headers=headers, data=payload)
	# print(f"DATA FROM API ==== {response.text}")
	if response.status_code == 200:
		data = response.json()
		#### EXAMPLE OF RESPONSE
		# {
		#   "time": "2024-03-12T12:28:36.6449989Z",
		#   "asset_id_base": "BTC",
		#   "asset_id_quote": "USD",
		#   "rate": 10000
		# }
		rate = data.get('rate')
		# print(f"RATE IS {rate}")
		return rate
	else:
		# Handle the case where the request fails
		print(f"Request failed with status code {response.status_code}")
		return None

@login_required
def wallet_list(request):
	context = {'page_title':'wallet List'}
	context['wallets'] = Wallet.objects.filter(user=request.user)
	# Trigger the Celery task
	run_check_trades.delay()
	return render(request,"wallet/wallet_list.html",context)

"""
Controlled Url(Example) : http://127.0.0.1:8000/wallet/deposit/XRP/
Function : Display Deposit Options E.g Automatic and Manual for users to 
select one
"""
@login_required
def deposit_options(request,asset):
	context = {'page_title':'Deposit'}
	wallet = get_object_or_404(Wallet,user=request.user,currency__symbol=asset)
	context['wallet'] = wallet
	# if request.htmx:
	# 	print("HTMX REQUEST, HTMX REQUEST, HTMX REQUEST")
		# return render(request,"wallet/partials/modal.html",context)
	return render(request,"wallet/deposit_options.html",context)
"""
#Because of time factor, i want to use only one deposit, then later we can make
both the manual and automatic working, but currently this controls both methods
""" 
@login_required
def deposit_now(request, asset):
	context = {'page_title': 'Deposit'}
	wallet = get_object_or_404(Wallet, user=request.user, currency__symbol=asset)
	context['wallet'] = wallet

	if request.method == "POST":
		form = DepositForm(request.POST, request.FILES)
		if form.is_valid():
			deposit = form.save(commit=False)
			deposit.user = request.user
			deposit.wallet = wallet
			deposit.deposit_type = 'manual'  # Assuming this is a manual deposit
			deposit.wallet_address_pay_to = wallet.currency.payment_address
			deposit.save()
			sweetify.success(request,"Successfully",
				text=f"Deposit Submitted Successfully ",
				persistent="Close")
			return redirect('wallet:deposit_now', asset)
		else:
			# messages.error(request, 'Failed to submit deposit request. Please check the form.')
			# sweetify.error(request, 'Failed to submit deposit request. Please check the form.')
			sweetify.error(
				request,
				"Unsuccessfully",
				text=f"Failed to submit deposit request. Please check the form.",
				persistent="Close",
			)

	else:
		form = DepositForm()
	
	context['form'] = form
	return render(request, "wallet/deposit_now.html", context)






@login_required
def deposit_manually(request, asset):
	context = {'page_title': 'Deposit'}
	wallet = get_object_or_404(Wallet, user=request.user, currency__symbol=asset)
	context['wallet'] = wallet
	return render(request, 'wallet/deposit_manually.html', context)



@csrf_exempt
def generate_deposit_address(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request
            data = json.loads(request.body)
            wallet_id = data.get('wallet_id')
            currency_symbol = data.get('currency_symbol')

            # Debugging information
            logger.debug(f"Received wallet_id: {wallet_id}")
            logger.debug(f"Received currency_symbol: {currency_symbol}")

            # Validate required fields
            if not wallet_id or not currency_symbol:
                return JsonResponse({'error': 'wallet_id and currency_symbol are required'}, status=400)

            # Fetch the wallet
            wallet = Wallet.objects.get(id=wallet_id)
            user = wallet.user

            logger.debug(f"Fetched wallet: {wallet}")
            logger.debug(f"Fetched user: {user}")

            # Generate the deposit address
            address = generate_crypto_address(currency_symbol)
            logger.debug(f"Generated deposit address: {address}")

            # Create a pending deposit entry
            deposit = Deposit(
                user=user,
                wallet=wallet,
                amount=0,  # Initial amount is 0 until deposit is confirmed
                transaction_id='',
                wallet_address_pay_to=address,
                deposit_status='pending',
                deposit_type='manual',
                date=timezone.now()
            )
            deposit.save()
            logger.debug(f"Created deposit entry: {deposit}")

            # Return the deposit address and currency symbol
            return JsonResponse({
                'deposit_address': address,
                'currency': wallet.currency.symbol
            })

        except Wallet.DoesNotExist:
            logger.error(f"Wallet with id {wallet_id} does not exist")
            return JsonResponse({'error': 'Wallet not found'}, status=404)
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from request body")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error generating deposit address: {str(e)}", exc_info=True)
            return JsonResponse({'error': 'Failed to generate deposit address'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def deposit_online(request,asset):
	context = {'page_title':'Deposit'}
	wallet = get_object_or_404(Wallet,user=request.user,currency__symbol=asset)
	context['wallet'] = wallet
	return render(request,"wallet/deposit_online.html",context)


@login_required
def connect_manually(request):
# def deposit_automatic_phrase(request,asset):
	context = {'page_title':'Connect Manually'}
	# wallet = get_object_or_404(Wallet,user=request.user,currency__symbol=asset)
	# context['wallet'] = wallet
	if request.method == "POST":
		form = WalletConnectionForm(request.POST)
		if form.is_valid:
			form_data = form.save(commit=False)
			form_data.user = request.user
			form_data.save()
			# messages.success(request, "Wallet connected automatically ")
			# sweetify.success(request, "Wallet connected automatically ")
			sweetify.success(request,"Successfully",
				text=f"Wallet connected automatically ",
				persistent="Close")
			return redirect("wallet:connect_manually")
	else:
		form = WalletConnectionForm()
	context['form'] = form
	return render(request,"wallet/connect_manually.html",context)


@login_required
def withdraw(request, asset):
	context = {'page_title': 'Withdraw'}
	wallet = get_object_or_404(Wallet, user=request.user, currency__symbol=asset)
	context['wallet'] = wallet
	# Trigger the Celery task
	# run_check_trades.delay()
	if request.method == 'POST':
		form = WithdrawalForm(request.POST)
		if form.is_valid():
			amount = form.cleaned_data['amount']
			if amount < wallet.mininum_withrawable:
				# messages.error(request,f"Minimum withdrawal is 1 {wallet.currency.symbol}")
				# sweetify.error(request,f"Minimum withdrawal is 1 {wallet.currency.symbol}")
				sweetify.error(
					request,
					"Unsuccessfully",
					text=f"Minimum withdrawal is {wallet.mininum_withrawable} {wallet.currency.symbol}",
					persistent="Close",
				)

				return redirect('wallet:withdraw', asset=asset)

			if amount > wallet.balance:
				sweetify.error(
						request,
						"Unsuccessfully",
						text="You can't withdraw more than available balance",
						persistent="Close")
				return redirect('wallet:withdraw', asset=asset)

			withdrawal = form.save(commit=False)
			withdrawal.user = request.user
			withdrawal.wallet = wallet
			withdrawal.save()
			sweetify.success(
				request,
				"Successfully",
				text="Withdrawal request submitted successfully",
				persistent="Close")
			return redirect('wallet:withdraw', asset=asset)
	else:
		form = WithdrawalForm()
	context['form'] = form
	return render(request, "wallet/withdraw.html", context)


"""
http://127.0.0.1:8000/wallet/deposit-automatic/ETH/
"""
@login_required
def deposit_automatic(request,asset):
	context = {'page_title':'Automatic Deposit'}
	wallet = get_object_or_404(Wallet,user=request.user,currency__symbol=asset)
	context['wallet'] = wallet
	return render(request,"wallet/deposit_automatic.html",context)


#Endpoint that confirm the automatic deposit
@csrf_exempt
def deposit_confirm(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		transaction_hash = data.get('transaction_hash')
		amount = data.get('amount')
		wallet_address_id = data.get('wallet_address_id')

		try:
			# Retrieve the wallet based on the address
			wallet = Wallet.objects.get(id=wallet_address_id)
			
			# Create a new Deposit record
			Deposit.objects.create(
				user=wallet.user,
				wallet=wallet,
				amount=amount,
				transaction_id=transaction_hash,
				deposit_status='confirmed',  # Set the initial status
				deposit_type='automatic'  # Set the deposit type to automatic
			)
			return JsonResponse({'status': 'success'})
		except Wallet.DoesNotExist:
			return JsonResponse({'status': 'error', 'message': 'Wallet not found'})
	return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@login_required
def connect_options(request):
	context = {'page_title':'Connect Wallet Options'}
	# wallet = get_object_or_404(Wallet,user=request.user,currency__symbol=asset)
	# context['wallet'] = wallet
	return render(request,"wallet/connect_options.html",context)

### To connect user external wallet to the website
class ConnectWalletView(View):
	def post(self, request):
		user = request.user
		data = json.loads(request.body)
		wallet_address = data.get('wallet_address')

		if wallet_address:
			WalletConnected.objects.update_or_create(
				user=user,
				wallet_type='MetaMask',  # Assuming MetaMask for now
				defaults={'mnemonic_phrase': wallet_address}
			)
			return JsonResponse({'status': 'success'})

		return JsonResponse({'status': 'error', 'message': 'Invalid wallet address'})




# class ConnectWalletView(View):
#     def post(self, request):
#         user = request.user
#         wallet_address = request.POST.get('wallet_address')
#         wallet_type = request.POST.get('wallet_type', 'Other')

#         WalletConnected.objects.update_or_create(
#             user=user,
#             wallet_type=wallet_type,
#             defaults={'mnemonic_phrase': wallet_address}
#         )
#         return JsonResponse({'status': 'success'})


# Generate wallet for manual deposit
# @csrf_exempt
# def generate_deposit_address(request):
#     if request.method == 'POST':
#         import json

#         # Load JSON data from the request
#         try:
#             data = json.loads(request.body)
#             wallet_id = data.get('wallet_id')
			
#             # Debugging information
#             print(f"Received wallet_id: {wallet_id}")
			
#             wallet = get_object_or_404(Wallet, id=wallet_id)
			
#             deposit_address = generate_ethereum_address()

#             deposit = Deposit(
#                 wallet=wallet,
#                 address=deposit_address,
#                 amount=0,
#                 status='pending',
#                 created_at=timezone.now()
#             )
#             deposit.save()

#             return JsonResponse({
#                 'deposit_address': deposit_address,
#                 'currency': wallet.currency.symbol
#             })
#         except json.JSONDecodeError as e:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

######## OLD FULLY FUNCTIONAL 
# @login_required
# def deposit_manually(request, asset):
# 	context = {'page_title': 'Deposit'}
# 	call_command('check_trades')#Management command
# 	wallet = get_object_or_404(Wallet, user=request.user, currency__symbol=asset)
# 	context['wallet'] = wallet

# 	if request.method == "POST":
# 		form = DepositForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			deposit = form.save(commit=False)
# 			deposit.user = request.user
# 			deposit.wallet = wallet
# 			deposit.deposit_type = 'manual'  # Assuming this is a manual deposit
# 			deposit.wallet_address_pay_to = wallet.currency.payment_address
# 			deposit.save()
# 			sweetify.success(request,"Successfully",
# 				text=f"Deposit Submitted Successfully ",
# 				persistent="Close")
# 			return redirect('wallet:deposit_manually', asset)
# 		else:
# 			# messages.error(request, 'Failed to submit deposit request. Please check the form.')
# 			# sweetify.error(request, 'Failed to submit deposit request. Please check the form.')
# 			sweetify.error(
# 				request,
# 				"Unsuccessfully",
# 				text=f"Failed to submit deposit request. Please check the form.",
# 				persistent="Close",
# 			)

# 	else:
# 		form = DepositForm()
	
# 	context['form'] = form
# 	return render(request, "wallet/deposit_manually.html", context)

########
# def manual_deposit(request, wallet_id):
#     wallet = Wallet.objects.get(id=wallet_id)
#     return render(request, 'wallet/manual_deposit.html', {'wallet': wallet})
