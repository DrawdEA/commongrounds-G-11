from django.urls import path

from .views import index

urlpatterns = [
    path('', index, name='index'),
    # TODO: Create urlpatterns for list and detail view
]



app_name = "diyprojects"