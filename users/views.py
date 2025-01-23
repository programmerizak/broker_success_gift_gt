from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import User
from .forms import UserEditForm
from wallet.models import Wallet
from decimal import Decimal
from wallet.tasks import run_check_trades

"""Views that can only be access by verified email users """
# from allauth.account.decorators import verified_email_required

# @verified_email_required
# def verified_users_only_view(request):
# 	pass





import requests

@login_required
def dashboard(request):
	context = {'page_title': 'Dashboard'}
	user = get_object_or_404(User, id=request.user.id)
	context['user'] = user
	wallets = Wallet.objects.filter(user=user)
	# Trigger the Celery task
	run_check_trades.delay()
	context['wallets'] = wallets
	
	# Fetch real-time cryptocurrency prices
	asset_prices = {}
	try:
		# Get prices from CoinGecko API
		response = requests.get(
			'https://api.coingecko.com/api/v3/simple/price',
			params={'ids': ','.join([wallet.currency.name.lower() for wallet in wallets]), 'vs_currencies': 'usd'}
		)
		if response.status_code == 200:
			asset_prices = response.json()
	except Exception as e:
		context['price_error'] = f"Error fetching asset prices: {str(e)}"

	# Calculate total value in USD
	total_value = 0
	for wallet in wallets:
		asset = wallet.currency.name.lower()
		balance = wallet.balance
		price = asset_prices.get(asset, {}).get('usd', 0)
		total_value += balance * Decimal(price)

	context['total_value'] = total_value

	return render(request, 'users/dashboard.html', context)


# @login_required
# def dashboard(request):
# 	context = {'page_title':'Dashboard '}
# 	user = get_object_or_404(User,id=request.user.id)
# 	context['user'] = user
# 	context['wallets'] = Wallet.objects.filter(user=user)
# 	return render(request,'users/dashboard.html',context)



@login_required
def edit_profile(request):
	context = {'page_title':'Edit Profile'}
	user = request.user
	if request.method == 'POST':
		form = UserEditForm(instance=user, data=request.POST,files=request.FILES)
		if form.is_valid():
			updated_form = form.save(commit=False)
			updated_form.save()
			messages.success(request, 'Profile Updated Successfully')
			
	else:
		form = UserEditForm(instance=user)
	context['form'] = form
	return render(request,'users/edit_profile.html',context)
