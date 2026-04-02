from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Profile, Favorite, ProjectReview
# Create your views here.


def project_list(request):
    projects = Project.objects.all()
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        created_projects = Project.objects.filter(creator=profile)
        reviewed_projects = Project.objects.filter(project_reviews__reviewer=profile)
        favorited_projects = Project.objects.filter(favorites__profile=profile)

        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#in
        user_interacted_project_ids = (created_projects | reviewed_projects | favorited_projects).distinct().values_list('id')
        other_projects = Project.objects.exclude(id__in=user_interacted_project_ids)

        return render(request, 'diyprojects/project_list.html',
                    {'other_projects':other_projects,
                     'created_projects': created_projects,
                     'reviewed_projects': reviewed_projects,
                     'favorited_projects': favorited_projects})
    else:
        return render(request, 'diyprojects/project_list.html',
                    {'project_list':projects})


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'diyprojects/project_detail.html',
                  {'project': project})