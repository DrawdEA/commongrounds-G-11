from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType, 
        on_delete = models.SET_NULL,
        null = True,
        related_name='categories',
    )
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True,  null=True)
