from django.urls import path
from . import views

app_name = 'plans'

urlpatterns = [
    path('', views.plan_list, name='plan_list'),  # List all plans
    # path("subscribe/", views.subscribe_plan, name="subscribe_plan"),
    # path('<int:plan_id>/', views.plan_detail, name='plan_detail'),  # View a specific plan
    # path('<int:plan_id>/deposit/', views.deposit_on_plan, name='deposit_on_plan'),  # Deposit into a specific plan
    path('<str:plan_name>/deposit/', views.deposit_on_plan, name='deposit_on_plan'),  # Deposit into a specific plan
]
