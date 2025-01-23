from django.urls import path
from . import views



app_name = "pages"

urlpatterns = [
	path('', views.home_page, name='home_page'),
	path('about-us/', views.about_page, name='about_page'),
	path('contact-us/', views.contact_page, name='contact_page'),
	path('terms-conditions/', views.terms_page, name='terms_page'),
	path('privacy-policy/', views.privacy_page, name='privacy_page'),
]
