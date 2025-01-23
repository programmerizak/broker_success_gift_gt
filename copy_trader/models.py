from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse


User = get_user_model()


class CopyTrader(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="expert")
	name = models.CharField(max_length=20,unique=True,
		help_text="Copy Trader full name ")
	photo = ThumbnailerImageField(upload_to='copy_trader/',help_text="Picture of the CopyTrader")
	no_wins = models.PositiveIntegerField(default=0)
	no_loose = models.PositiveIntegerField(default=0)
	no_copiers = models.PositiveIntegerField(default=0)
	date_joined = models.DateTimeField(default=timezone.now)
	copiers = models.ManyToManyField(User)

	def __str__(self):
		return f"Copy Trader {self.user.username}"

	class Meta:
		ordering = ['-date_joined']


	@property
	def total_trades(self):
		return self.no_wins + self.no_loose

	@property
	def win_percentage(self):
		total_trades = self.total_trades
		return f"{(self.no_wins / total_trades) * 100:.2f}%" if total_trades > 0 else "0%"

	@property
	def loose_percentage(self):
		total_trades = self.total_trades
		return f"{(self.no_loose / total_trades) * 100:.2f}%" if total_trades > 0 else "0%"


# class Copier(models.Model):
# 	copy_trader = models.ForeignKey(User)
# 	users = models.ManyToManyField(CopyTrader)
