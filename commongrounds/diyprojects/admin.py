from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, ProjectCategory

class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory

class ProjectAdmin(admin.ModelAdmin):
    model = Project

# registering the model and the admin is what tells
# Django that admin pages must be generated for the models specified
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)