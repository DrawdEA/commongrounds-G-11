from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Project, Profile, Favorite, ProjectReview
from .forms import ProjectForm
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


@login_required
def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'diyprojects/project_detail.html',
                  {'project': project})


@login_required
def project_add(request):
    # https://docs.djangoproject.com/en/6.0/ref/forms/api/#s-dynamic-initial-values
    creator_profile = Profile.objects.get(user=request.user) 
    form = ProjectForm(initial={'creator': creator_profile.display_name})
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', pk=project.pk)
    return render(request, 'diyprojects/project_add.html', {"form": form})