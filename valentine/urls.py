from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('unlock/<int:day_id>/', views.unlock_day, name='unlock_day'),
    path('teddy/', views.teddy, name='teddy'),
]