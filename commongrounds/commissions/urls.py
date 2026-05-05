from django.urls import path
from . import views

app_name = "commissions"

urlpatterns = [
    path("requests/", views.commission_list, name="commission_list"),
    path("request/add/", views.commission_create, name="commission_create"),
    path("request/<int:pk>/", views.commission_detail, name="commission_detail"),
    path("request/<int:pk>/edit/", views.commission_update, name="commission_update"),
]