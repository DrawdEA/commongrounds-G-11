from django import forms
from .models import Project, ProjectRating, ProjectReview


class ProjectForm(forms.ModelForm):
    # https://www.geeksforgeeks.org/python/disabled-django-form-field-validation
    creator = forms.CharField(disabled=True, required=False)

    class Meta:
        model = Project
        exclude = ['creator']


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ['comment', 'image']


class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['score']
