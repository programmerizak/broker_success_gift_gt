from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StakePlan, Stake
from .forms import StakeForm
from wallet.models import Wallet


import sweetify


@login_required
def available_coin(request, my_staking=None):
	context = {'page_title': 'Available Coin'}
	if my_staking:
		my_staking = Stake.objects.filter(user=request.user)
		context['page_title'] = f"My Staking"
		context['my_staking'] = my_staking
		return render(request,"stake/my_staking.html", context)
	else:
		stake_plans = StakePlan.objects.all()
		# stake_plans = StakePlan.objects.filter(active=True)
		context['stake_plans'] = stake_plans
		return render(request, "stake/available_coin.html", context)



@login_required
def stake_now(request,coin_symbol):
	plan = get_object_or_404(StakePlan,coin__symbol=coin_symbol)
	user_wallet = get_object_or_404(Wallet,user=request.user,
		currency__symbol=coin_symbol)
	form = StakeForm()
	call_command('check_trades')#Management command
	context = {
		'plan': plan,
		'page_title': f'Stake {plan.coin.name}',
		'wallet':user_wallet,
	}
	if request.method == "POST":
		form = StakeForm(request.POST)
		if form.is_valid():
			amount_entered = form.cleaned_data.get("stake_amount")
			duration = form.cleaned_data.get("duration")
			print(f" DURATION {duration}")
			print(f" DURATION {duration}")

			if amount_entered > user_wallet.available_balance:
				sweetify.error(request,f"You can't stake more than your wallet balances {user_wallet.available_balance} {coin_symbol}")
				return redirect("stake:stake_now", coin_symbol)
			
			if amount_entered < plan.minimum_stake_amount:
				sweetify.error(request,f"You can't stake less than the minimum amount {plan.minimum_stake_amount} {coin_symbol}")
				return redirect("stake:stake_now", coin_symbol)
			
			if amount_entered > plan.maximum_stake_amount:
				sweetify.error(request,f"You can't stake more than the maximum amount {plan.maximum_stake_amount} {coin_symbol}")
				return redirect("stake:stake_now", coin_symbol)

			form_data = form.save(commit=False)
			form_data.user = request.user
			form_data.stake_plan = plan
			form_data.staking_wallet = user_wallet

            # # Attach the selected duration to the stake instance
            # selected_duration = Duration.objects.get(duration_days=duration)
            # stake.duration = selected_duration


			form_data.save()
			sweetify.success(request,f"You've stake {amount_entered}{coin_symbol} successfully")
			return redirect("stake:stake_now", coin_symbol)

		else:
			sweetify.error(request,"Something wrong with the form")
			return redirect("stake:stake_now", coin_symbol)

	context['form'] = form
	return render(request, 'stake/stake_now.html', context)


	
	# stake_duration = models.ForeignKey(Duration, on_delete=models.CASCADE, related_name="stake_duratin")