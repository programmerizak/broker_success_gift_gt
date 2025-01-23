
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import string
import datetime
from decimal import Decimal

from wallet.models import Wallet


User = get_user_model()

def ran_gen(size, chars=string.ascii_uppercase + string.digits): 
	return ''.join(random.choice(chars) for x in range(size))

class Trade(models.Model):
	TRADE_TYPE = [
		('buy', 'Buy'),
		('sell', 'Sell'),
	]


	TRADE_STATUS = [
		('ongoing', 'Ongoing'),
		('lost', 'Lost'),
		('won', 'Won'),
	]

	## This is same as in the user model
	TRADE_OUTCOME = [
		('win_trades', 'Win Trades'),
		('loose_trades', 'Loose Trades'),
	]

	STRIKE_RATE = [
		('highest_buy', 'Highest Buy'),
		('high_buy', 'High Buy'),
		('normal', 'Normal'),
		('highest_sell', 'Highest Sell'),
		('high_sell', 'High Sell'),
	]


	trade_pair_choices = [
		('BTC/ETH', 'BTC/ETH'),
		('BTC/XRP', 'BTC/XRP'),
		('BTC/LTC', 'BTC/LTC'),
		('BTC/BCH', 'BTC/BCH'),
		('BTC/EOS', 'BTC/EOS'),
		('BTC/ADA', 'BTC/ADA'),
		('BTC/TRX', 'BTC/TRX'),
		('BTC/XLM', 'BTC/XLM'),
		('BTC/DOT', 'BTC/DOT'),
		('BTC/BNB', 'BTC/BNB'),
		('BTC/USDT', 'BTC/USDT'),
		('ETH/BTC', 'ETH/BTC'),
		('ETH/XRP', 'ETH/XRP'),
		('ETH/LTC', 'ETH/LTC'),
		('ETH/BCH', 'ETH/BCH'),
		('ETH/EOS', 'ETH/EOS'),
		('ETH/ADA', 'ETH/ADA'),
		('ETH/TRX', 'ETH/TRX'),
		('ETH/XLM', 'ETH/XLM'),
		('ETH/DOT', 'ETH/DOT'),
		('ETH/BNB', 'ETH/BNB'),
		('ETH/USDT', 'ETH/USDT'),
		('XRP/BTC', 'XRP/BTC'),
		('XRP/ETH', 'XRP/ETH'),
		('XRP/LTC', 'XRP/LTC'),
		('XRP/BCH', 'XRP/BCH'),
		('XRP/EOS', 'XRP/EOS'),
		('XRP/ADA', 'XRP/ADA'),
		('XRP/TRX', 'XRP/TRX'),
		('XRP/XLM', 'XRP/XLM'),
		('XRP/DOT', 'XRP/DOT'),
		('XRP/BNB', 'XRP/BNB'),
		('XRP/USDT', 'XRP/USDT'),
		('LTC/BTC', 'LTC/BTC'),
		('LTC/ETH', 'LTC/ETH'),
		('LTC/XRP', 'LTC/XRP'),
		('LTC/BCH', 'LTC/BCH'),
		('LTC/EOS', 'LTC/EOS'),
		('LTC/ADA', 'LTC/ADA'),
		('LTC/TRX', 'LTC/TRX'),
		('LTC/XLM', 'LTC/XLM'),
		('LTC/DOT', 'LTC/DOT'),
		('LTC/BNB', 'LTC/BNB'),
		('LTC/USDT', 'LTC/USDT'),
		('BCH/BTC', 'BCH/BTC'),
		('BCH/ETH', 'BCH/ETH'),
		('BCH/XRP', 'BCH/XRP'),
		('BCH/LTC', 'BCH/LTC'),
		('BCH/EOS', 'BCH/EOS'),
		('BCH/ADA', 'BCH/ADA'),
		('BCH/TRX', 'BCH/TRX'),
		('BCH/XLM', 'BCH/XLM'),
		('BCH/DOT', 'BCH/DOT'),
		('BCH/BNB', 'BCH/BNB'),
		('BCH/USDT', 'BCH/USDT'),
		('EOS/BTC', 'EOS/BTC'),
		('EOS/ETH', 'EOS/ETH'),
		('EOS/XRP', 'EOS/XRP'),
		('EOS/LTC', 'EOS/LTC'),
		('EOS/BCH', 'EOS/BCH'),
		('EOS/ADA', 'EOS/ADA'),
		('EOS/TRX', 'EOS/TRX'),
		('EOS/XLM', 'EOS/XLM'),
		('EOS/DOT', 'EOS/DOT'),
		('EOS/BNB', 'EOS/BNB'),
		('EOS/USDT', 'EOS/USDT'),
		('ADA/BTC', 'ADA/BTC'),
		('ADA/ETH', 'ADA/ETH'),
		('ADA/XRP', 'ADA/XRP'),
		('ADA/LTC', 'ADA/LTC'),
		('ADA/BCH', 'ADA/BCH'),
		('ADA/EOS', 'ADA/EOS'),
		('ADA/TRX', 'ADA/TRX'),
		('ADA/XLM', 'ADA/XLM'),
		('ADA/DOT', 'ADA/DOT'),
		('ADA/BNB', 'ADA/BNB'),
		('ADA/USDT', 'ADA/USDT'),
		('TRX/BTC', 'TRX/BTC'),
		('TRX/ETH', 'TRX/ETH'),
		('TRX/XRP', 'TRX/XRP'),
		('TRX/LTC', 'TRX/LTC'),
		('TRX/BCH', 'TRX/BCH'),
		('TRX/EOS', 'TRX/EOS'),
		('TRX/ADA', 'TRX/ADA'),
		('TRX/XLM', 'TRX/XLM'),
		('TRX/DOT', 'TRX/DOT'),
		('TRX/BNB', 'TRX/BNB'),
		('TRX/USDT', 'TRX/USDT'),
		('XLM/BTC', 'XLM/BTC'),
		('XLM/ETH', 'XLM/ETH'),
		('XLM/XRP', 'XLM/XRP'),
		('XLM/LTC', 'XLM/LTC'),
		('XLM/BCH', 'XLM/BCH'),
		('XLM/EOS', 'XLM/EOS'),
		('XLM/ADA', 'XLM/ADA'),
		('XLM/TRX', 'XLM/TRX'),
		('XLM/DOT', 'XLM/DOT'),
		('XLM/BNB', 'XLM/BNB'),
		('XLM/USDT', 'XLM/USDT'),
		('DOT/BTC', 'DOT/BTC'),
		('DOT/ETH', 'DOT/ETH'),
		('DOT/XRP', 'DOT/XRP'),
		('DOT/LTC', 'DOT/LTC'),
		('DOT/BCH', 'DOT/BCH'),
		('DOT/EOS', 'DOT/EOS'),
		('DOT/ADA', 'DOT/ADA'),
		('DOT/TRX', 'DOT/TRX'),
		('DOT/XLM', 'DOT/XLM'),
		('DOT/BNB', 'DOT/BNB'),
		('DOT/USDT', 'DOT/USDT'),
		('BNB/BTC', 'BNB/BTC'),
		('BNB/ETH', 'BNB/ETH'),
		('BNB/XRP', 'BNB/XRP'),
		('BNB/LTC', 'BNB/LTC'),
		('BNB/BCH', 'BNB/BCH'),
		('BNB/EOS', 'BNB/EOS'),
		('BNB/ADA', 'BNB/ADA'),
		('BNB/TRX', 'BNB/TRX'),
		('BNB/XLM', 'BNB/XLM'),
		('BNB/DOT', 'BNB/DOT'),
		('BNB/USDT', 'BNB/USDT'),
		('BNB/USDT', 'BNB/USDT'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_trades")
	trade_id = models.CharField(max_length=50, default='#'+ran_gen(10))
	trade_pair = models.CharField(max_length=20, choices=trade_pair_choices, default="BTC/ETH")
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="trade_wallet")
	trading_amount = models.DecimalField(max_digits=20, decimal_places=8)
	# trading_amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.00)
	expected_payout = models.DecimalField(max_digits=20, decimal_places=8, default=0.00, blank=True, null=True)
	start_time = models.DateTimeField(default=timezone.now)
	duration = models.PositiveIntegerField(help_text="Duration of the trade in minutes")
	# duration = models.PositiveIntegerField(default=1, help_text="Duration of the trade in minutes")
	end_time = models.DateTimeField(blank=True, null=True,help_text="Time trade will end")
	strike_rate = models.CharField(max_length=50, choices=STRIKE_RATE, default="High Buy")
	trade_status = models.CharField(max_length=50, choices=TRADE_STATUS, default='ongoing')
	#Trade outcome gets his result from the user model, at the time the trade is been carried out
	trade_outcome = models.CharField(max_length=50, choices=TRADE_OUTCOME, 
		default='loose_trades',help_text="Determine if Trader will loose or win", editable=False)

	trade_type = models.CharField(max_length=50, choices=TRADE_TYPE, default='buy')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.username + ' - ' + self.trade_pair

	'''
	Because of the frontend design, these methods are to bring
	out the desire color output
	'''

	def color(self):
		if self.trade_type == "buy":
			return "green"
		else:
			return "red"

	def order_color(self):
		if self.trade_type == "buy":
			return "com"
		else:
			return "com-lim"



