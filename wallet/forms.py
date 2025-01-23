from django import forms
from .models import Withdrawal,WalletConnected, Deposit
from mnemonic import Mnemonic
from currency.models import Currency


class WithdrawalForm(forms.ModelForm):
	class Meta:
		model = Withdrawal
		fields = ['withdrawal_network', 'amount', 'wallet_address']
		labels = {
			'withdrawal_network': 'Withdrawal Network',
			'amount': 'Amount',
			'wallet_address': 'Wallet Address',
		}
		widgets = {
			'withdrawal_network': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select withdrawal network'}),
			'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter withdrawal amount'}),
			'wallet_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter wallet address'}),
		}


class WalletConnectionForm(forms.ModelForm):
	class Meta:
		model = WalletConnected
		fields = ['wallet_type', 'mnemonic_phrase']

		labels = {
			'mnemonic_phrase': '12/24-Word Mnemonic Phrase'
		}

		widgets = {
			### Use when the model field is CharField
			# 'mnemonic_phrase': forms.TextInput(attrs={'placeholder': 'Enter your 24-word mnemonic phrase'}),
			### Use when the model field is TextField
			'mnemonic_phrase': forms.Textarea(attrs={'placeholder': 'Enter your 12/24-word mnemonic phrase', 'rows': 4}),
			'wallet_type': forms.Select(attrs={'class': 'input-box'}),
			# 'mnemonic_phrase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 24-Word Mnemonic Phrase'}),
		}




# class DepositForm(forms.ModelForm):
# 	class Meta:
# 		model = Deposit
# 		fields = ['amount','transaction_id','payment_screenshot',]


class DepositForm(forms.ModelForm):
	class Meta:
		model = Deposit
		fields = ['amount', 'transaction_id']

		labels = {
			# 'withdrawal_network': 'Withdrawal Network',
			'amount': 'Amount Deposited',
			# 'wallet_address': 'Wallet Address',
		}
		widgets = {
			# 'withdrawal_network': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select withdrawal network'}),
			# 'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter withdrawal amount'}),
			# 'wallet_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter wallet address'}),
		}




	def __init__(self, *args, **kwargs):
		super(DepositForm, self).__init__(*args, **kwargs)
		# Increase the dimensions of the form fields
		for field_name in self.fields:
			self.fields[field_name].widget.attrs['class'] = 'form-control'
			self.fields[field_name].widget.attrs['style'] = 'width: 100%; height: 40px;'


class SwapForm(forms.Form):
    from_coin = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_crypto=True),
        empty_label=None, 
        label='',
        widget=forms.Select(attrs={'class': 'moot'})
    )
    from_amount = forms.DecimalField(
        max_digits=10, decimal_places=2,
        label='',
        widget=forms.TextInput(attrs={'class': 'amt', 'id': 'amtR', 'value': '1'})
    )
    to_coin = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_crypto=True),
        empty_label=None, 
        label='',
        widget=forms.Select(attrs={'class': 'moot'})
    )
    to_amount = forms.DecimalField(
        max_digits=10, decimal_places=2,
        label='',
        widget=forms.TextInput(attrs={'class': 'amt', 
        	'readonly': 'readonly','value':0})
    
)
    def clean(self):
        cleaned_data = super().clean()
        from_coin = cleaned_data.get("from_coin")
        to_coin = cleaned_data.get("to_coin")

        if from_coin == to_coin:
            raise forms.ValidationError("From coin and to coin cannot be the same.")

        return cleaned_data



class MoveAssetForm(forms.Form):
    destination_address = forms.CharField(max_length=100, help_text="Destination Ethereum address")
    amount_eth = forms.DecimalField(max_digits=20, decimal_places=8, help_text="Amount of ETH to transfer")


######### WORKING MAR 26TH 1:32AM
# class SwapForm(forms.Form):
# 	from_coin = forms.ModelChoiceField(queryset=Currency.objects.filter(is_crypto=True),
# 		empty_label=None, label='')
# 	# from_amount = forms.DecimalField(max_digits=10, decimal_places=2, initial=1, label='Amount')
# 	from_amount = forms.DecimalField(max_digits=10, decimal_places=2)
# 	# from_amount = forms.DecimalField(max_digits=10, decimal_places=2, initial=1, label='')
# 	to_coin = forms.ModelChoiceField(queryset=Currency.objects.filter(is_crypto=True), empty_label=None, label='')
# 	to_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}), label='')


# 	def clean(self):
# 		cleaned_data = super().clean()
# 		from_coin = cleaned_data.get("from_coin")
# 		to_coin = cleaned_data.get("to_coin")

# 		if from_coin == to_coin:
# 			raise forms.ValidationError("From coin and to coin cannot be the same.")

# 		return cleaned_data
