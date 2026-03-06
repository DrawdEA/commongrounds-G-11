from django.urls import path
from .views import CommissionListView, CommissionDetailView, CommissionCreateView

app_name = "commissions"

urlpatterns = [
    path("requests/", CommissionListView.as_view(), name="commission_list"),
    path("request/new/", CommissionCreateView.as_view(), name="commission_create"),
    path("request/<int:pk>/", CommissionDetailView.as_view(), name="commission_detail"),
]