from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Profile, Favorite, ProjectReview, ProjectRating
from .forms import ProjectForm, ProjectReviewForm, ProjectRatingForm
# Create your views here.


def get_average_rating(project_ratings):
    if len(project_ratings) <= 0:
        return -1

    sum = 0
    count = 0
    for rating in project_ratings:
        sum += rating.score
        count += 1
    return sum/count


def project_list(request):
    projects = Project.objects.all()
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        created_projects = Project.objects.filter(creator=profile)
        reviewed_projects = (Project.objects.filter
                             (project_reviews__reviewer=profile))
        favorited_projects = Project.objects.filter(favorites__profile=profile)

        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#in
        interacted_project_ids = ((created_projects |
                                  reviewed_projects |
                                  favorited_projects)
                                  .distinct().values_list('id'))
        other_projects = Project.objects.exclude(id__in=interacted_project_ids)

        return render(request, 'diyprojects/project_list.html',
                      {'other_projects':  other_projects,
                       'created_projects': created_projects,
                       'reviewed_projects': reviewed_projects,
                       'favorited_projects': favorited_projects})
    else:
        return render(request, 'diyprojects/project_list.html',
                      {'project_list': projects})


@login_required
def project_detail(request, pk):
    # Handling multiple forms: https://stackoverflow.com/questions/866272

    # Basic Preliminary Logic
    project = Project.objects.get(pk=pk)
    project_reviews = ProjectReview.objects.filter(project=project)
    average_rating = get_average_rating(ProjectRating.objects.
                                        filter(project=project))
    is_favorited = Favorite.objects.filter(project=project,
                                           profile=request
                                           .user.profile).exists()

    review_form = ProjectReviewForm()
    rating_form = ProjectRatingForm()
    if request.method == 'POST':
        profile = request.user.profile
        if 'review_form' in request.POST:
            form = ProjectReviewForm(request.POST, request.FILES)
            # https://docs.djangoproject.com/en/6.0/topics/forms/modelforms/
            if form.is_valid():
                review = form.save(commit=False)
                review.reviewer = profile
                review.project = project
                review.save()
        elif 'favorite_toggle' in request.POST:
            favorite = Favorite.objects.filter(project=project,
                                               profile=profile)
            if favorite:
                favorite.delete()
            else:
                Favorite.objects.create(project=project, profile=profile)
        elif 'rating_form' in request.POST:
            rating_form = ProjectRatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.project = project
                rating.profile = profile
                rating.save()
        return redirect('diyprojects:project_detail', pk=pk)
    return render(request, 'diyprojects/project_detail.html',
                  {'project': project,
                   'project_reviews': project_reviews,
                   'average_rating': average_rating,
                   'review_form': review_form,
                   'rating_form': rating_form,
                   'is_favorited': is_favorited})


@login_required
def project_add(request):
    # https://docs.djangoproject.com/en/6.0/ref/forms/api/#s-dynamic-initial-values
    creator_profile = Profile.objects.get(user=request.user)
    form = ProjectForm(initial={'creator': creator_profile.display_name})
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = creator_profile
            project.save()
            return redirect('diyprojects:project_detail', pk=project.pk)
    return render(request, 'diyprojects/project_add.html', {"form": form})


@login_required
def project_edit(request, pk):
    # https://www.geeksforgeeks.org/python/update-view-function-based-views-django/
    project = Project.objects.get(pk=pk)
    form = ProjectForm(initial={'title': project.title,
                                'description': project.description,
                                'materials': project.materials,
                                'steps': project.steps,
                                'category': project.category,
                                'creator': request.user.profile.display_name})
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('diyprojects:project_detail', pk=pk)
    return render(request, 'diyprojects/project_edit.html', {"form": form})
