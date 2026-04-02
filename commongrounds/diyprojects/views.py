from django.shortcuts import render
from .models import Project
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'diyprojects/project_list.html',
                  {'project_list':projects})


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'diyprojects/project_detail.html',
                  {'project': project})