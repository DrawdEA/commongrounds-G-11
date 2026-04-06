from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLES = [("Normal", "Normal"),
             ("Market Seller", "Market Seller"),
             ("Event Organizer", "Event Organizer"),
             ("Book Contributor", "Book Contributor"),
             ("Project Creator", "Project Creator"),
             ("Commission Maker", "Commission Maker")]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLES, default="Normal")

    def __str__(self):
        return self.user.username
    