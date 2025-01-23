from django import forms
from .models import UserPlan


class DepositForm(forms.ModelForm):
    class Meta:
        model = UserPlan
        fields = ['amount_invested']  # Only allow users to input the amount to invest
        widgets = {
            'amount_invested': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter deposit amount'}),
        }

    def clean_amount_invested(self):
        amount = self.cleaned_data['amount_invested']
        if amount <= 0:
            raise forms.ValidationError("Deposit amount must be greater than zero.")
        return amount
