from django.db import models
from django.urls import reverse
from accounts.models import Profile
from django.core.validators import MaxValueValidator, MinValueValidator

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
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    updated_on = models.DateTimeField(null=False, auto_now=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL,
                                 related_name='projects', null=True)
    creator = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                                 related_name='created_projects', null=True)

    def __str__(self):
        if not self.category:
            return '{} under uncategorized'.format(self.title) 
        return '{} under {}'.format(self.title, self.category.name)

    def get_absolute_url(self):
        return reverse('diyprojects:project_detail', args=[str(self.pk)])

    def split_materials(self):
        return self.materials.split("|")

    def split_steps(self):
        return self.steps.split("|")

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'project'
        verbose_name_plural = 'projects'


class Favorite(models.Model):
    # https://docs.djangoproject.com/en/6.0/ref/models/fields/#:~:text=Enum%20member%20values%20are%20a,value%20properties%20on%20the%20members.
    class ProjectStatus(models.TextChoices):
        BACKLOG = "Backlog"
        TODO = "To-Do"
        DONE = "Done"
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='favorites')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='user_favorites')
    date_favorited = models.DateField(auto_now_add=True)
    project_status = models.TextField(choices=ProjectStatus,
                                      default=ProjectStatus.TODO)


class ProjectReview(models.Model):
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                 related_name="reviews")
    comment = models.TextField()
    image = models.ImageField(upload_to='images/', null=True)


class ProjectRating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name="ratings")
    # https://stackoverflow.com/questions/42425933/how-do-i-set-a-default-max-and-min-value-for-an-integerfield-django
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )