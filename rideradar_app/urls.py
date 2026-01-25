from django.urls import path
from . import views


urlpatterns = [    
    path('', views.home, name='home'),
    path('fleet-admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('fleet-admin/login/', views.admin_login, name='admin_login'),
    path('fleet-admin/register/', views.admin_register, name='admin_register'),
    path('fleet-admin/analytics/', views.admin_analytics, name='admin_analytics'),
    path('fleet-admin/fleet-tracking/', views.admin_fleet_tracking, name='admin_fleet_tracking'),
    path('fleet-admin/smart-recommendations/', views.admin_smart_recommendations, name='admin_smart_recommendations'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/register/', views.user_register, name='user_register'),
    path('user/live-tracking/', views.user_live_tracking, name='user_live_tracking'),
    path('user/tickets/', views.user_tickets, name='user_tickets'), 
]