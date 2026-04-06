from django.urls import path
from .views import index, profile_update, register

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('<str:username>/', profile_update, name='profile_update') 
]


app_name = "accounts"