from django.db import models
from django.urls import reverse


# Create your models here.

class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('projectcategory_list', args=[str(self.name)])
    
    class Meta:
        ordering = ['name']
        verbose_name = 'project category'
        verbose_name_plural = 'project categories'

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    # Reference for auto_now and auto_now_add: https://docs.djangoproject.com/en/6.0/ref/models/fields/
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    updated_on = models.DateTimeField(null=False, auto_now=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, related_name='projects', null=True)

    def __str__(self):
        return '{} under {}'.format(self.title, self.category.name)
    
    def get_absolute_url(self):
        return reverse('diyprojects:project_detail', args=[str(self.pk)])
    
    def splitMaterials(self):
        return self.materials.split("|")
    
    def splitSteps(self):
        return self.steps.split("|")
    
    class Meta:
        ordering = ['created_on']
        verbose_name = 'project'
        verbose_name_plural = 'projects'
    
