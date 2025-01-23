from allauth.account.forms import SignupForm
from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from .models import User

# from allauth.account.forms import LoginForm
# from django.core.validators import RegexValidator
# # from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import gettext_lazy as _ 
# from django.shortcuts import render,redirect, get_object_or_404



# My own custom  widget for datetime
class DateInput(forms.DateInput):
    input_type = 'date'


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','country','gender',
        	'profile_picture',]
        # widgets = {'date_of_birth':DateInput()}


""" custom signup form  """
class CustomSignupForm(SignupForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$',
        message="Valid format: '+9999999999'. Up to 14 digits allowed."
    )
    # currency_choices = (('USD','USD'),('EUR','EUR'),)
    gender_choices = [
        ('', _('Select Gender')),
        ('Male', _('Male')),
        ('Female', _('Female')),
        ('Rather Not Specify', _('Rather Not Specify'))
    ]

    country_choices = [(code, name) for code, name in CountryField().flatchoices]
    country_choices.insert(0, ('', 'Select Country'))

    country = forms.ChoiceField(
        choices=country_choices,
        label=_('Country')
    )


    gender = forms.ChoiceField(
        choices=gender_choices,
        label=_('Gender'),
        required=False
    )


    def save(self, request):
        # Ensure you call the parent class save., save() returns a User object
        user = super(CustomSignupForm, self).save(request)
        # Add your own processing here.
        user.country = self.cleaned_data.get('country')
        user.gender = self.cleaned_data.get('gender')
        user.save()
        # You must return the original result.
        return user


# """ custom signup form  """
# class CustomSignupForm(SignupForm):
#     phone_regex = RegexValidator(
#         regex=r'^\+?1?\d{9,14}$',
#         message="Valid format: '+9999999999'. Up to 14 digits allowed."
#     )
#     # currency_choices = (('USD','USD'),('EUR','EUR'),)
#     gender_choices = [
#         ('', _('Select Gender')),
#         ('Male', _('Male')),
#         ('Female', _('Female')),
#         ('Rather Not Specify', _('Rather Not Specify'))
#     ]

#     # country = forms.ChoiceField(
#     #     # choices=CountryField().blank_label + list(CountryField().choices),
#     #     choices=CountryField().choices + [('', 'Select Country')],
#     #     label=_('Country')
#     # )


#     country_choices = [(code, name) for code, name in CountryField().flatchoices]
#     country_choices.insert(0, ('', 'Select Country'))

#     country = forms.ChoiceField(
#         choices=country_choices,
#         label=_('Country')
#     )


#     gender = forms.ChoiceField(
#         choices=gender_choices,
#         label=_('Gender'),
#         required=False
#     )


#     def save(self, request):
#         # Ensure you call the parent class save., save() returns a User object
#         user = super(CustomSignupForm, self).save(request)
#         # Add your own processing here.
#         user.country = self.cleaned_data.get('country')
#         user.gender = self.cleaned_data.get('gender')
#         # user.date_of_birth = self.cleaned_data.get('date_of_birth')
#         # user.phone_number = self.cleaned_data.get('phone_number')
#         # user.currency = self.cleaned_data.get('currency')
#         user.save()
#         # You must return the original result.
#         return user




""" custom login form  """
# from allauth.account.forms import LoginForm
# class MyCustomLoginForm(LoginForm):

#     def login(self, *args, **kwargs):

#         # Add your own processing here.

#         # You must return the original result.
#         return super(MyCustomLoginForm, self).login(*args, **kwargs)




