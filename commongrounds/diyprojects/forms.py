from django import forms
from .models import Project, ProjectCategory


class ProjectForm(forms.ModelForm):
    #https://www.geeksforgeeks.org/python/disabled-django-form-field-validation/
    creator = forms.CharField(disabled=True)
    class Meta:
        model = Project
        fields = '__all__' #TODO: make category a dropdown of only two unique values
