from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('data/', views.water_level_data, name='api_data'),
     path('api/live/', views.live_summary, name='live_summary'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('stats/', views.stats_view, name='stats'),
    path('add/', views.add_water_level, name='add_water'),
    path('chart/', views.water_chart, name='water_chart'),
    path('accounts/login/', views.login_view, name='login'),
]