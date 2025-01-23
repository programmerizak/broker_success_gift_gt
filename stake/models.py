from django.db import models
from django.utils import timezone
from django.urls import reverse
from currency.models import Currency
from django.contrib.auth import get_user_model
from wallet.models import Wallet

User = get_user_model()



class Duration(models.Model):
	duration_days = models.PositiveIntegerField()
	percentage_return = models.PositiveIntegerField()

	def __str__(self):
		return f"{self.duration_days} Days to give {self.percentage_return}% "


class StakePlan(models.Model):
	coin = models.OneToOneField(
		Currency,
		on_delete=models.CASCADE,
		related_name="coin_stake",
		limit_choices_to={'is_crypto': True}  # Filter currencies with is_crypto=True
	)
	minimum_stake_amount = models.DecimalField(max_digits=20, decimal_places=8)
	maximum_stake_amount = models.DecimalField(max_digits=20, decimal_places=8)
	durations = models.ManyToManyField(Duration)
	active = models.BooleanField(default=True, help_text="Still allow stakers or not")
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"{self.coin.name} Stake Plan"

	class Meta:
		ordering = ['-created_at']

	def get_absolute_url(self):
		return reverse('stake:stake_now', args=[self.coin.symbol])



	def status_color(self):
		if self.active :
			return "com"
		# elif self.status == "ongoing":
			# return "com-pend"
		else:
			return "com-lim"




class Stake(models.Model):
	## This is same as in the user model

	STAKE_OUTCOME = [
		('win_stakes', 'Win Stakes'),
		('loose_stakes', 'Loose Stakes'),
	]
	
	STAKE_STATUS = [
		('ongoing', 'Ongoing'),
		('lost', 'Lost'),
		('won', 'Won'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staker")
	stake_plan = models.ForeignKey(StakePlan, on_delete=models.CASCADE, related_name="stakes")
	staking_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="stake_wallet")
	stake_duration = models.ForeignKey(Duration, on_delete=models.CASCADE, related_name="stake_duratin")
	######
	stake_amount = models.DecimalField(max_digits=20, decimal_places=8)
	estimated_return = models.DecimalField(max_digits=20, decimal_places=8,blank=True,null=True)
	stake_status = models.CharField(max_length=50, choices=STAKE_STATUS,default="ongoing") 
	stake_outcome = models.CharField(max_length=50, choices=STAKE_OUTCOME, 
		default='loose_stakes',help_text="Determine if Trader will loose or win stakes", editable=False)
	###########################################################
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.user.username}'s Stake in {self.stake_plan.coin.name}"


	def status_color(self):
		if self.status == "won":
			return "com"
		elif self.status == "ongoing":
			return "com-pend"
		else:
			return "com-lim"