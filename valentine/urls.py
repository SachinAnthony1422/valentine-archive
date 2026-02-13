from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('unlock/<int:day_id>/', views.unlock_day, name='unlock_day'),
    path('teddy/', views.teddy, name='teddy'),
    path('promise/', views.promise, name='promise'),
    path('hug-reveal/', views.hug_reveal, name='hug_reveal'),
    path('kiss-reveal/', views.kiss_reveal, name='kiss_reveal'),
]