# DJANGO IMPORTS #
from django.shortcuts import render,redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.core.serializers import serialize
from wallet.tasks import run_check_trades

# THRID PARTY IMPORT #
import requests, json


# PROJECT IMPORT #
from currency.models import Currency
from .forms import TradeForm,TradeSearchForm
from .models import Trade
from wallet.models import Wallet

# BASIC
BASE_API_URL = 'https://rest.coinapi.io/v1/'
COIN_API_KEY = settings.COIN_API_KEY
LIVE_COIN_WATCH_API_KEY = settings.LIVE_COIN_WATCH_API_KEY





""" MARKET """

#MARKET LIST

# Return all other assets rate to base asset, default is USDT
def get_crypto_listings(asset_id_base='USDT'):
	headers = {
		'X-CoinAPI-Key': COIN_API_KEY,
	}

	response = requests.get(f"{BASE_API_URL}/exchangerate/{asset_id_base}", headers=headers)
	if response.status_code == 200:
		data = response.json()
		# Process the data here
		return data
	else:
		print(f"Failed to fetch crypto listings: {response.status_code}")
		return None


def market_list(request,base_asset="USDT"):
	context = {'page_title':'Market list'}
	# Trigger the Celery task
	# run_check_trades.delay()
	
	return render(request,"trade/market_list.html", context)


def get_coin_list(asset_id_base='USDT'):
	url = "https://api.livecoinwatch.com/coins/list"

	payload = json.dumps({
	  "currency": f"{asset_id_base}",#Dynamically set the asset_id_base 
	  "sort": "rank",
	  "order": "ascending",
	  "offset": 0,
	  "limit": 2,
	  "meta": False
	})

	headers = {
	  'content-type': 'application/json',
	  'x-api-key': LIVE_COIN_WATCH_API_KEY
	}

	response = requests.request("POST", url, headers=headers, data=payload)
	# response = requests.get(f"{BASE_API_URL}/exchangerate/{asset_id_base}", headers=headers)
	if response.status_code == 200:
		data = response.json()
		# Process the data here
		return data
	else:
		print(f"Failed to fetch crypto listings: {response.status_code}")
		return None


@login_required
def place_a_trade(request):
	context = {'page_title': 'Place Trade'}
	user = request.user
	form = TradeForm()  # Define the form here
	# Trigger the Celery task
	run_check_trades.delay()
	if request.method == "POST":
		wallet_id = request.session.get("selected_wallet_id")
		wallet_selected = Wallet.objects.get(id=wallet_id)
		if 'buy_btn' in request.POST:
			form = TradeForm(request.POST)
			if form.is_valid():
				amount_entered = form.cleaned_data['trading_amount']
				if amount_entered > wallet_selected.balance:
					# print("AMOUNT ENTER IS TOO MUCH")
					messages.error(request,"You can't Buy above your available balance")
					return redirect('trade:place_a_trade')

				trade = form.save(commit=False)
				trade.user = request.user
				trade.wallet = wallet_selected
				trade.trade_type = "buy"
				trade.save()
				messages.success(request, 'Buy Order submitted successfully.')
				return redirect('trade:place_a_trade')



		elif 'sell_btn' in request.POST:
			form = TradeForm(request.POST)
			if form.is_valid():
				amount_entered = form.cleaned_data['trading_amount']
				if amount_entered > wallet_selected.balance:
					# print("AMOUNT ENTER IS TOO MUCH")
					messages.error(request,"You can't Sell above your available balance")
					return redirect('trade:place_a_trade')

				trade = form.save(commit=False)
				trade.user = request.user
				trade.wallet = wallet_selected
				trade.trade_type = "sell"
				trade.save()
				messages.success(request, 'Buy Order submitted successfully.')
				return redirect('trade:place_a_trade')


		# else:
		# 	print("I DON'T KNOW THE BUTTON CLICKED ")
		# 	print("I DON'T KNOW THE BUTTON CLICKED ")
		# 	print("I DON'T KNOW THE BUTTON CLICKED ")
	# else:
	#     form = TradeForm()  # Set the form if it's not a POST request

	context['form'] = form
	context['buy_trades'] = Trade.objects.filter(user=user, trade_type="buy")
	context['sell_trades'] = Trade.objects.filter(user=user, trade_type="sell")
	context['open_trades'] = Trade.objects.filter(user=user, trade_status="ongoing")
	context['trades'] = Trade.objects.filter(user=user)
	# context['user_wallets'] = Wallet.objects.filter(user=user)
	wallet = Wallet.objects.filter(user=user).order_by('-balance').first()
	context['wallet'] = wallet

	'''
	Am putting the wallet in session so that i can know the selected wallet
	and then when a trade occurs i know which wallet to debit from  
	'''
	request.session['selected_wallet_id'] = wallet.id
	context['user_wallets'] = Wallet.objects.filter(user=user).order_by('-balance')


	return render(request, "trade/place_a_trade.html", context)



def change_wallet(request):
	if request.method == 'POST':
		selected_wallet_id = request.POST.get('wallet_id')
		if selected_wallet_id is not None:
			try:
				wallet = Wallet.objects.get(id=selected_wallet_id)

				'''
				This update the previously selected one
				'''
				request.session['selected_wallet_id'] = wallet.id
				user_wallets = Wallet.objects.filter(user=request.user).order_by('-balance')
				context = {'wallet': wallet, 'user_wallets': user_wallets}
				if request.htmx:
					return render(request, "trade/partials/specific_wallet.html", context)
				else:
					return JsonResponse({'success': 'Wallet updated successfully'})
			except Wallet.DoesNotExist:
				return JsonResponse({'error': 'Selected wallet does not exist'})
		else:
			return JsonResponse({'error': 'No wallet selected'})
	else:
		return JsonResponse({'error': 'Invalid request method'})




@login_required
def orders(request):
	context = {'page_title': 'Orders'}
	user = request.user

	# Initialize the form
	form = TradeSearchForm(request.GET or None)

	# Check if the search form is submitted and valid
	if form.is_valid():
		trade_pair = form.cleaned_data['trade_pair']
		trade_type = form.cleaned_data['trade_type']
		# Perform search based on trade pair and trade type
		trades = Trade.objects.filter(user=user, trade_pair=trade_pair, trade_type=trade_type)
		context['trades'] = trades
	else:
		# If the ongoing filter is applied
		if 'ongoing' in request.GET:
			trades = Trade.objects.filter(user=user, trade_status='ongoing')
			context['trades'] = trades
		else:
			# Display all trades by default
			trades = Trade.objects.filter(user=user)
			context['trades'] = trades

	context['form'] = form
	context['TRADE_TYPES'] = Trade.TRADE_TYPE
	context['trade_pair_choices'] = Trade.trade_pair_choices

	return render(request, "trade/orders.html", context)


# @login_required
# def orders(request):
#     context = {'page_title': 'Orders'}
#     user = request.user

#     # Check if the search form is submitted
#     if 'trade_pair' in request.GET and 'trade_type' in request.GET:
#         form = TradeSearchForm(request.GET)
#         if form.is_valid():
#             trade_pair = form.cleaned_data['trade_pair']
#             trade_type = form.cleaned_data['trade_type']
#             # Perform search based on trade pair and trade type
#             trades = Trade.objects.filter(user=user, trade_pair=trade_pair, trade_type=trade_type)
#             context['trades'] = trades
#     # Check if the ongoing filter is applied
#     elif 'ongoing' in request.GET:
#         trades = Trade.objects.filter(user=user, trade_status='ongoing')
#         context['trades'] = trades
#     else:
#         # Display all trades by default
#         trades = Trade.objects.filter(user=user)
#         context['trades'] = trades
#         form = TradeSearchForm()

#     context['form'] = form
#     return render(request, "trade/orders.html", context)


# @login_required
# def orders(request):
# 	context = {'page_title':'Orders '}
# 	user=request.user
# 	ongoing = request.GET.get('ongoing', None)

# 	if ongoing:
# 		# Filter ongoing trades
# 		trades = Trade.objects.filter(user=user, trade_status='ongoing')
# 	else:
# 		# Filter all trades for the user
# 		trades = Trade.objects.filter(user=user)

# 	context['trades'] = trades
# 	return render(request,"trade/orders.html",context)





"""Default Base Asset is USDT """
def market_list2222(request,base_asset="USDT"):
	context = {'page_title':'Market list'}
	url = "https://api.livecoinwatch.com/coins/list"

	payload = json.dumps({
	  "currency": f"{base_asset}",
	  "sort": "rank",
	  "order": "ascending",
	  "offset": 0,
	  "limit": 30,
	  "meta": False
	})

	headers = {
		'content-type': 'application/json',
		# 'x-api-key': '188f9199-1b4b-47a6-9a91-49ee0063197a'
		'x-api-key': '8e4fda3c-9c22-4918-b625-fa71003ca45d'
	}

	# response = requests.get(url, headers=headers)#ChatGPT
	response = requests.request("POST", url, headers=headers, data=payload)
	# print("AAAAAAAAAAAAAA", response.text)
	if response.status_code == 200:
		data = response.json()
		context['crypto_data'] = data
		context['base_asset'] = base_asset
		context['base_currencies'] = Currency.objects.filter(is_active=True)
		if request.htmx:
			return render(request, "trade/partials/market_list.html",context)
		return render(request, 'market/market_list.html', context)
	else:
		error_message = f"Failed to fetch crypto data: {response.status_code}"
		context['error_message'] = error_message
		return render(request, 'market/error.html', context)




@login_required
def market_detail(request,trade_asset,base_asset):
	context = {'page_title':'Market Detail'}
	return render(request,"trade/market_detail.html",context)



@login_required
def withdraw(request,asset):
	context = {'page_title':'Withdraw '}
	wallet = get_object_or_404(Wallet,user=request.user,currency__symbol=asset)
	context['wallet'] = wallet
	return render(request,"wallet/withdraw.html",context)






'''

{
	"asset_id_base": "BTC",
	"rates": [
		{
			"time": "2023-07-24T13:00:43.0000000Z",
			"asset_id_quote": "EUR",
			"rate": 26371.195622912368
		},
		{
			"time": "2023-07-24T13:00:43.0000000Z",
			"asset_id_quote": "USD",
			"rate": 29222.332203558577
		},
		{
			"time": "2023-07-24T13:00:43.0000000Z",
			"asset_id_quote": "ETH",
			"rate": 15.780394091251145
		},
		{
			"time": "2023-07-24T13:00:43.0000000Z",
			"asset_id_quote": "XRP",
			"rate": 41915.164263881525
		},
		// ...more BTC exchange rates with various other assets...
}

'''


# url = "https://rest.coinapi.io/v1/exchangerate/:asset_id_base"

# payload={}
# headers = {
#   'Accept': 'text/plain',
#   'X-CoinAPI-Key': '<API_KEY_VALUE>'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)




# @login_required
# def market_list(request):
# 	context = {'page_title':'Market List'}

# 	# Example usage
# 	crypto_listings = get_coin_list()
# 	if crypto_listings:
# 		print("JOYYYY", crypto_listings)
# 		context['crypto_listings'] = crypto_listings

# 	return render(request,"trade/market_list.html",context)


# # Replace 'YOUR_API_KEY' with your actual LiveCoinWatch API key
# API_URL = 'https://api.livecoinwatch.com/coins/list'

# def get_crypto_listings():
#     headers = {
#         'x-api-key': API_KEY,
#     }

#     response = requests.get(API_URL, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         # Process the data here
#         return data
#     else:
#         print(f"Failed to fetch crypto listings: {response.status_code}")
#         return None

# # Example usage
# crypto_listings = get_crypto_listings()
# if crypto_listings:
#     # Process the list of cryptocurrencies as per your project's requirements
#     print(crypto_listings)



# """SWAP/EXCHANGE """
# import requests

# url = "https://rest.coinapi.io/v1/exchangerate/:asset_id_base/:asset_id_quote"

# payload={}
# headers = {
#   'Accept': 'text/plain',
#   'X-CoinAPI-Key': '<API_KEY_VALUE>'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)


"""
SWAP

import requests

def fetch_data():
url = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
headers = {
	"X-CoinAPI-Key": "YOUR-API-KEY" # Replace with your API key
}
response = requests.get(url, headers=headers)
return response.json()

print(fetch_data())

OUTPUT
> python access-coinapi-data.py
{
	"time": "2023-07-24T11:31:56.0000000Z",
	"asset_id_base": "BTC",
	"asset_id_quote": "USD",
	"rate": 29295.929694597355
}


"""


