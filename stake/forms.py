from django import forms
from .models import Stake,Duration

class Stake555Form(forms.ModelForm):
    DURATION_CHOICES = [
        (30, '30 Days'),
        (60, '60 Days'),
        (180, '180 Days'),
        (365, '365 Days'),
    ]

    duration = forms.ChoiceField(choices=DURATION_CHOICES, widget=forms.RadioSelect(attrs={'class': 'blk blk-inner'}))
    stake_amount = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'blk'}))

    class Meta:
        model = Stake
        fields = ['stake_amount', 'duration']

 

class StakeForm(forms.ModelForm):
    duration = forms.ChoiceField(widget=forms.RadioSelect(), label='', required=False)

    class Meta:
        model = Stake
        fields = ['stake_amount', 'duration']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get all available durations from the Duration model
        durations = Duration.objects.all()
        # Create choices from the durations
        duration_choices = [(duration.duration_days, f"{duration.duration_days} Days") for duration in durations]
        # Update the choices for the duration field
        self.fields['duration'].choices = duration_choices

        # Set placeholder and remove label for stake_amount field
        self.fields['stake_amount'].widget.attrs['placeholder'] = '0.00'
        self.fields['stake_amount'].label = ''
