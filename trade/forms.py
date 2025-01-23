from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML
from crispy_forms.bootstrap import InlineField


from .models import Trade


class TradeSearchForm(forms.Form):
    trade_pair = forms.ChoiceField(label='Trade Pair', choices=Trade.trade_pair_choices)
    trade_type = forms.ChoiceField(label='Trade Type', choices=Trade.TRADE_TYPE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            InlineField('trade_pair', template="custom_trade_pair_field.html")
        )





# {{form.trade_pair|as_crispy_field}}


class TradeForm(forms.ModelForm):
	class Meta:
		model = Trade
		fields = ['trade_pair','trading_amount','duration','strike_rate']

		labels = {
			'trade_pair': '',
			'trading_amount': '',
			'duration': '',
			'strike_rate': '',
		}
		widgets = {
			'trade_pair': forms.Select(attrs={'class': 'input-box', 'placeholder': 'Select Trade Pair'}),
			'trading_amount': forms.NumberInput(attrs={'class': 'input-box', 'placeholder': 'Enter amount'}),
			'duration': forms.NumberInput(attrs={'class': 'input-box', 'placeholder': 'Time in Minutes'}),
			'strike_rate': forms.Select(attrs={'class': 'input-box'}),
			# 'wallet_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter wallet address'}),
		}

