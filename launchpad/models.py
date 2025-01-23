from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils import timezone
from django.urls import reverse

class LaunchPad(models.Model):
	TRADE_STATUS = [
		('active', 'Active'),
		('upcoming', 'Upcoming'),
		('completed', 'Completed'),
	]

	coin_name = models.CharField(max_length=20,unique=True,
		help_text="E.g Ripple,Ethereum,US Dollar,Bitcoin,Euro")
	coin_symbol = models.CharField(max_length=10, unique=True, help_text="E.g XRP,ETH,USD,BTC,EUR")
	description = models.TextField(blank=True)
	coin_icon = ThumbnailerImageField(upload_to='launchpads/')
	status = models.CharField(max_length=80,choices=TRADE_STATUS,default="upcoming")

	soft_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
	hard_cap = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
	sale_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

	launch_time_start = models.DateTimeField(default=timezone.now)
	launch_time_end = models.DateTimeField(default=timezone.now)
	filled_percent = models.PositiveIntegerField()


	def __str__(self):
		return f"{self.coin_name}"


	class Meta:
		ordering = ['-launch_time_start',]


	def get_absolute_url(self):
		return reverse('launchpad:launchpad_detail',args=[self.status,self.id])

	
	def status_color(self):
		if self.status == "active":
			return "com"
		elif self.status == "upcoming":
			return "com-pend"
		else:
			return "com-lim"