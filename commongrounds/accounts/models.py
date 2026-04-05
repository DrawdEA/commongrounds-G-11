from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('commission_maker', 'Commission Maker'),
        ('regular_user', 'Regular User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='regular_user'
    )

    def __str__(self):
        return self.user.username