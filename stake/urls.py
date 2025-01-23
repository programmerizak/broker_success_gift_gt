from django.urls import path
from . import views

app_name = "stake"

urlpatterns = [
	path('available-coin/', views.available_coin,
		name='available_coin'),
	##### We set my_staking as True and pass into the url
	path('my-staking/', views.available_coin, 
		{'my_staking': True},name='my_staking'),
	path('<str:coin_symbol>/stake-now/', views.stake_now,name='stake_now'),
]
