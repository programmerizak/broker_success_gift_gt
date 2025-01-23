from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import MinValueValidator


class Currency(models.Model):
    name = models.CharField(max_length=20,unique=True,
    	help_text="E.g Ripple,Ethereum,US Dollar,Bitcoin,Euro")
    symbol = models.CharField(max_length=10, unique=True, help_text="E.g XRP,ETH,USD,BTC,EUR")
    address_prefix = models.CharField(max_length=10, blank=True, null=True,help_text="What comes b4 the address")
    # description = models.TextField(blank=True)
    icon = ThumbnailerImageField(upload_to='currency_icons/', default='default_currency_icon.png',
    	help_text="Picture of the Currency, the picture should not have background. That is .png format")
    is_crypto = models.BooleanField(default=True,help_text="To differentiate coin from fiat")
    is_active = models.BooleanField(default=True,help_text="If asset should be display or not ")
    # ------------PAYMENT ---------------#
    payment_address = models.CharField(max_length=300,
        help_text="Wallet address to receive payment/deposit for this Currency")
    barcode = ThumbnailerImageField(upload_to="payment_address",help_text="Barcode of the wallet address to receive payment ")
    percentage_deposit_fee = models.DecimalField(max_digits=10, decimal_places=8, validators=[MinValueValidator(0)])
    minimum_deposit = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    minimum_withdraw = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0.0000001)], default=0.0000001)



    # def __str__(self):
    #     return f"{self.name} ({self.symbol})"

    def __str__(self):
        return f"{self.symbol}"



    class Meta:
        verbose_name_plural = 'Currencies'

    def get_balance(self, wallet_type):
        """
        Calculate and return the total balance for a specific wallet type (e.g., available, in orders, etc.)
        """
        wallets = self.wallet_set.filter(wallet_type=wallet_type)
        total_balance = sum(wallet.balance for wallet in wallets)
        return total_balance

    def get_wallets(self, wallet_type):
        """
        Return all wallets of the given wallet type associated with this currency.
        """
        return self.wallet_set.filter(wallet_type=wallet_type)

    def get_transactions(self):
        """
        Return all transactions involving this currency.
        """
        return self.transaction_set.all()

    def get_last_transaction(self):
        """
        Return the last transaction involving this currency.
        """
        return self.transaction_set.latest('timestamp')

    def get_default_icon(self):
        """
        Return the default icon for the currency.
        """
        return 'default_currency_icon.png'
