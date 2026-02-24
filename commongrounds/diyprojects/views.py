from django.http import HttpResponse
from .models import Project
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
# Create your views here.

def index(request):
    return HttpResponse('Hello World! This came from the index view')

class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/project_list.html'

class ProjectDetailView(DetailView):
    model = Project 
    template_name = 'diyproject/project_detail.html'