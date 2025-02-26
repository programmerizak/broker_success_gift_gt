from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField





class User(AbstractUser):
	gender_choices = (
		('Male','Male'),
		('Female','Female'),
		('Rather Not Specify','Rather Not Specify'),)
	TRADE_OUTCOME = [
		('win_trades', 'Win Trades'),
		('loose_trades', 'Loose Trades'),
	]

	STAKE_OUTCOME = [
		('win_stakes', 'Win Stakes'),
		('loose_stakes', 'Loose Stakes'),
	]

	phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$',
		message = "Valid format: '+9999999999'. Up to 14 digits allowed .")
	profile_verified = models.BooleanField(default=False)
	#################################################################
	country = CountryField(default="US")
	######## what determine whether trader profile will be visible or not in copy traders
	social_trader = models.BooleanField(default=False,
		help_text="Marking this will make this user be visible for other users to copy his trade")

	trade_outcome = models.CharField(max_length=50, choices=TRADE_OUTCOME, 
		default='loose_trades',help_text="Determine if Trader will loose or win his trade")

	stake_outcome = models.CharField(max_length=50, choices=STAKE_OUTCOME, 
		default='loose_stakes',help_text="Determine if Staker will loose or win stakes")

	##################################################################################
	profile_picture = ThumbnailerImageField(upload_to="profile/", default="no-pic.png")
	gender = models.CharField(choices=gender_choices,max_length=30,blank=True)
	##################################################################################
	last_deposit = models.CharField(max_length=100,default="N/A")
	last_withdrawal = models.CharField(max_length=100,default="N/A")


	class Meta:
		ordering = ['-date_joined',]
