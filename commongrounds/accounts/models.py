from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLES = ["Market Seller",
             "Event Organizer",
             "Book Contributor",
             "Project Creator",
             "Commission Maker"]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()

    def __str__(self):
        return self.user.username
    