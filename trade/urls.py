from django.urls import path
from .import views

app_name = "trade"

urlpatterns = [
	path("", views.market_list, name="market_list"),
	path("asset-<str:base_asset>/", views.market_list,
		name="market_specific"),#used when base asset is selected
	# ------------------------------------------------------- #
	path("orders/", views.orders, name="orders"),
	path("order-history/", views.orders, name="order_history"),
	#---------------------------------------------------------#
	path("trade-now/", views.place_a_trade, name="place_a_trade"),
	path("change/wallet/", views.change_wallet, name="change_wallet"),#HTMX
	path("<str:trade_asset>-<str:base_asset>/", views.market_detail, name="market_detail"),
]