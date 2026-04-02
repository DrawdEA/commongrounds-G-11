from django.urls import path

from .views import project_add, project_list, project_detail, project_edit

urlpatterns = [
    path('projects/', project_list, name='project_list'),
    path('project/<int:pk>', project_detail,
         name='project_detail'),
    path('project/add', project_add,
         name='project_add'),
     path('project/<int:pk>/edit', project_edit, name='project_edit')
]


app_name = "diyprojects"
