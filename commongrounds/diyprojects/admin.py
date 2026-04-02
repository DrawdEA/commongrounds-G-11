from django.contrib import admin

# Register your models here.

from .models import (Favorite, Project, ProjectCategory,
                     ProjectRating, ProjectReview)


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory


class ProjectAdmin(admin.ModelAdmin):
    model = Project


class ProjectRatingAdmin(admin.ModelAdmin):
    model = ProjectRating


class ProjectReviewAdmin(admin.ModelAdmin):
    model = ProjectReview


# registering the model and the admin is what tells
# Django that admin pages must be generated for the models specified
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)
admin.site.register(ProjectReview, ProjectReviewAdmin)
