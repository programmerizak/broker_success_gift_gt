from django.urls import path
from . import views

app_name = "launchpad"

urlpatterns = [
	path('', views.launchpad_list, name='launchpad_list'),
	path('active/', views.launchpad_list, {'status': 'active'},
		name='launchpad_active'),
	path('upcoming/', views.launchpad_list, {'status': 'upcoming'},
		name='launchpad_upcoming'),
	path('completed/', views.launchpad_list, {'status': 'completed'},
		name='launchpad_completed'),
	path('single/<str:status_given>/<int:launchpad_id>/', views.launchpad_detail,
		name='launchpad_detail'),

]
