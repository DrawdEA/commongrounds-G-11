from django.urls import path
from .views import profile_update

urlpatterns = [
    path('<str:username>/', profile_update, name='profile_update') 
]


app_name = "accounts"