from django import forms
from .models import ContactUs
from django.core.validators import RegexValidator
from services.models import ServiceName

from django.utils import timezone
from coupon.models import Coupon



phone_regex = RegexValidator(regex = r'^\+?1?\d{9,14}$',
	message="Valid phone number format:'+99999999999'. Up to 14 digits allowed. ")

class ContactUsForm(forms.ModelForm):
	name = forms.CharField(label="",max_length=70,
		widget=forms.TextInput(attrs={'placeholder':'Your Full Name'}))
	email = forms.EmailField(label="",widget= forms.EmailInput(
		attrs={'placeholder':'Your Email'}))
	phone_number = forms.CharField(label="",validators=[phone_regex],
		max_length=15,widget= forms.TextInput(
			attrs={'placeholder':'Your Phone Number'}))

	service = forms.ModelChoiceField(
		queryset=ServiceName.objects.all(),
		label='',
		empty_label="Select a service",  # Add this line to set a placeholder
		widget=forms.Select(attrs={'class': 'form-control'})  # Add CSS class to the widget
	)

	# project_file = forms.FileField(
	# 	label="",
	# 	widget=forms.FileInput(
	# 		attrs={
	# 			'placeholder': 'Accepted file types: docx, txt',
	# 			'accept': '.docx, .txt'  # Specify accepted file extensions
	# 		}
	# 	),
	# 	required=False  # Make the field optional
	# )

	coupon_code = forms.CharField(label="",max_length=70,required=False,
		widget=forms.TextInput(attrs={'placeholder':'Enter coupon(Optional)'}))
	message = forms.CharField(label="",max_length=70,
		widget=forms.TextInput(attrs={'placeholder':'Enter your message'}))
	class Meta:
		model = ContactUs
		# fields = "__all__"
		exclude = ['percent_off',]



	def clean(self):
		cleaned_data = super().clean()

		coupon_code = self.cleaned_data.get('coupon_code')
		if coupon_code:
			try:
				coupon = Coupon.objects.get(code=coupon_code, expiration_date__gte=timezone.now())
				self.instance.percent_off = coupon.percentage_reduction
			except Coupon.DoesNotExist:
				raise forms.ValidationError("Invalid coupon code")

		return cleaned_data