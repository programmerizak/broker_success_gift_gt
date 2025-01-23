from django.urls import path
from . import views
app_name= "kyc"

urlpatterns = [
    path('kyc/', views.kyc_form, name='kyc_form'),
]
