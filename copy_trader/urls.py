from django.urls import path
from . import views

app_name = "copy_traders"

urlpatterns = [
	path('', views.copy_trader, name='copy_trader'),
]
