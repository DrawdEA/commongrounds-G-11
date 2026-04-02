from django.urls import path

from .views import project_add, project_list, project_detail

urlpatterns = [
    path('projects/', project_list, name='project_list'),
    path('project/<int:pk>', project_detail,
         name='project_detail'),
    path('project/add', project_add,
         name='project_add')
]


app_name = "diyprojects"
