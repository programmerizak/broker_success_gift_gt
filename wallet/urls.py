from django.urls import path
from .import views

app_name = "wallet"

urlpatterns = [
	path("", views.wallet_list, name="wallet_list"),
    path('connect-wallet/', views.ConnectWalletView.as_view(), name='connect_wallet'),
    path('connect-options/', views.connect_options, name='connect_options'),
    path("deposit-automatic/<str:asset>/", views.deposit_automatic, name="deposit_automatic"),
    path('deposit-confirm/', views.deposit_confirm, name='deposit_confirm'),
    path('generate_deposit_address/', views.generate_deposit_address, name='generate_deposit_address'),

	path("deposit/<str:asset>/", views.deposit_options, name="deposit_options"),
	path("deposit-now/<str:asset>/", views.deposit_now, name="deposit_now"),

	path("deposit-manually/<str:asset>/", views.deposit_manually, name="deposit_manually"),
	

	path("deposit/online/<str:asset>/", views.deposit_online,
		name="deposit_online"),
	path("connect-manually/", views.connect_manually,
		name="connect_manually"),

	path("withdraw/<str:asset>/", views.withdraw, name="withdraw"),
	path("swap/", views.swap, name="swap"),
	
	path("rate/<str:asset_id_base>/<str:asset_id_quote>/", views.get_rate, name="get_rate"),
]
