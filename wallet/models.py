from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from currency.models import Currency
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerImageField
from .encryption import encrypt_data, decrypt_data




User = get_user_model()


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    address = models.CharField(max_length=100, blank=True, null=True,help_text="Wallet address to receive this crypto when you withdraw")
    in_orders_balance = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    in_futures_balance = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    in_withdraw_balance = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
 

    def __str__(self):
        return f"{self.user.username} {self.currency.name} Wallet - Balance is: {self.balance} {self.currency.symbol}"


    # A user cannnot have same currency in wallet
    class Meta:
        unique_together = ['user','currency']


    def deposit_url(self):
        return reverse('wallet:deposit_options',args=[self.currency.symbol])

    def withdraw_url(self):
        return reverse('wallet:withdraw',args=[self.currency.symbol])


    # Get the withdrawals that wallet is 
    def withdrawals(self):
        # withdrawals = Withdrawal.objects.filter(wallet=self)
        return Withdrawal.objects.filter(wallet=self)



    # Get the deposits that wallet is 
    def deposits(self):
        # withdrawals = Withdrawal.objects.filter(wallet=self)
        return Deposit.objects.filter(wallet=self)


    @property
    def mininum_withrawable(self):
        """Return minumum amount that can be withdraw from the currency"""
        return self.currency.minimum_withdraw



"""
Class the encrypt the private key to that it won't be store as plain
text in our django admin or database
"""
class EncryptedTextField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_data(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return encrypt_data(value)


"""
Model that stores generated user wallet,provider and private key 
"""
class GeneratedWalletAddress(models.Model):
    wallet_provider = models.CharField(max_length=20, help_text="ETH,BTC,LTC etc")
    address = models.CharField(max_length=100, unique=True)
    private_key = EncryptedTextField()  # Use the custom encrypted field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet_provider}-{self.address}"



######### OLD FULLY WORKING
# class Wallet(models.Model):

#     # we use this to know which balance to make effect to
#     WALLET_TYPE_CHOICES = [
#         ('available', 'Available'),
#         ('in_orders', 'In Orders'),
#         ('in_futures', 'In Futures'),
#         ('in_withdraw', 'In Withdraw'),
#     ]



#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
#     available_balance = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
#     in_orders_balance = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
#     in_futures_balance = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
#     in_withdraw_balance = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
#     #We use this wallet_type to know which part of the wallet to effect changes
#     wallet_type = models.CharField(max_length=20, choices=WALLET_TYPE_CHOICES, default="available")


#     def __str__(self):
#         return f"{self.user.username}'s {self.currency.name} Wallet"


#     # A user cannnot have same currency in wallet
#     class Meta:
#         unique_together = ['user','currency']


#     def deposit_url(self):
#         return reverse('wallet:deposit_options',args=[self.currency.symbol])

#     def withdraw_url(self):
#         return reverse('wallet:withdraw',args=[self.currency.symbol])


#     # Get the withdrawals that wallet is 
#     def withdrawals(self):
#         # withdrawals = Withdrawal.objects.filter(wallet=self)
#         return Withdrawal.objects.filter(wallet=self)



#     # Get the withdrawals that wallet is 
#     def deposits(self):
#         # withdrawals = Withdrawal.objects.filter(wallet=self)
#         return Deposit.objects.filter(wallet=self)


class WithdrawalNetwork(models.Model):
    name = models.CharField(max_length=50,unique=True,help_text="Network which withdrawal can me made")
    description = models.TextField(blank=True)
    withdrawal_fee = models.DecimalField(max_digits=10, decimal_places=8)

    def __str__(self):
        return self.name


class Withdrawal(models.Model):

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('processing', 'Processing'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE, related_name='withdrawals')
    withdrawal_network = models.ForeignKey('WithdrawalNetwork', on_delete=models.CASCADE, related_name='withdraw_network')
    #--------------------------------------------#
    wallet_address = models.CharField(max_length=200)
    trx_id = models.CharField(max_length=500,blank=True)
    #--------------------------------------------------#
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    # created_at = models.DateTimeField(auto_now_add=True)
    # created_at = models.DateTimeField(default=timezone.now, editable=True, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')
    # processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Withdrawal request by {self.user.username} for {self.amount}"

    def color(self):
        if self.status == "paid":
            return ""
        else:
            return "-pend"

    class Meta:
        ordering = ['-created_at',]


"""Display wallet connected to the website """
class WalletConnected(models.Model):
    WALLET_TYPES = [
        ('Metamask', 'Metamask'),
        ('Trust Wallet', 'Trust Wallet'),
        ('Coinbase Wallet', 'Coinbase Wallet'),
        ('Ledger Wallet', 'Ledger Wallet'),
        ('Trezor Wallet', 'Trezor Wallet'),
        ('Binance Chain Wallet', 'Binance Chain Wallet'),
        ('MyEtherWallet', 'MyEtherWallet'),
        ('Atomic Wallet', 'Atomic Wallet'),
        ('Exodus Wallet', 'Exodus Wallet'),
        ('Blockchain.com Wallet', 'Blockchain.com Wallet'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="connected_wallets")
    wallet_type = models.CharField(max_length=50, choices=WALLET_TYPES, default="Metamask")
    mnemonic_phrase = models.TextField(max_length=300,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet_type} Wallet of {self.user.username}"


class Deposit(models.Model):
    DEPOSIT_TYPES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    DEPOSIT_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manual_user")
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='deposit_wallet')
    amount = models.DecimalField(max_digits=20, decimal_places=8, validators=[MinValueValidator(0)])
    transaction_id = models.CharField(max_length=300, blank=True)
    wallet_address_pay_to = models.CharField(max_length=300, blank=True)
    deposit_status = models.CharField(max_length=50, choices=DEPOSIT_STATUS, default="pending")
    deposit_type = models.CharField(max_length=50, choices=DEPOSIT_TYPES, default="manual")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Deposit {self.id} by {self.user.username} for {self.amount} {self.wallet.currency.symbol}"

    class Meta:
        ordering = ['-date']
