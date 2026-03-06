from django.urls import path
from .views import event_detail, event_list 

urlpatterns = [
    path('events/', event_list, name = 'event_list'),
    path('event/<int:pk>/', event_detail, name = 'event_detail'),
]

app_name = "localevents"