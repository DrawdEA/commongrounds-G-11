from django import forms
from .models import Project, ProjectRating, ProjectReview, Favorite


class ProjectForm(forms.ModelForm):
    #https://www.geeksforgeeks.org/python/disabled-django-form-field-validation/
    creator = forms.CharField(disabled=True)
    class Meta:
        model = Project
        fields = '__all__'


class ProjectReviewForm(forms.ModelForm):
    class Meta:
        model = ProjectReview
        fields = ['comment', 'image']
