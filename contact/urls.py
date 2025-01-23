from django.urls import path
from . import views


app_name = "contact"

urlpatterns = [

	path('', views.contact, name='contact'),
    path('submit-form/', views.form_submission_view, name='form_submission'),

]