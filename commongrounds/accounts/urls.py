from django.urls import path
from .views import index, profile_update

urlpatterns = [
    path('', index, name="index"),
    path('<str:username>/', profile_update, name='profile_update') 
]


app_name = "accounts"