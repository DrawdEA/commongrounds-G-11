from django.urls import path

from .views import ProjectListView, ProjectDetailView

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('project/<int:project_number>', ProjectDetailView.as_view(), name='project_detail'),
]


app_name = "diyprojects"