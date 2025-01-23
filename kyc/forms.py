from django import forms
from .models import Kyc


from . models import Kyc
from django import forms

# My own custom  widget for datetime
class DateInput(forms.DateInput):
	input_type = 'date'

class KycForm(forms.ModelForm):
	class Meta:
		model = Kyc
		# fields = ['']
		exclude = ['user','verify_status','created','updated',]
		widgets = {'date_of_birth':DateInput()}
		


# class KycForm(forms.ModelForm):
#     class Meta:
#         model = Kyc
#         fields = ['first_name', 'last_name', 'email_address', 'date_of_birth', 'phone_number', 
#                   'address_line_1', 'address_line_2', 'city', 'state', 'nationality', 'zip_code',
#                   'ID_front', 'ID_back',]

#         # Customizing the date_of_birth field to use a date widget
#         date_of_birth = forms.DateField(
#             widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
#         )


