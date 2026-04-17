from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='events',
    )
    organizer = models.ManyToManyField(Profile)
    event_image = models.ImageField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    event_capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        choices = [('AVAIL', 'Available'), ('FULL', 'Full'), ('DONE', 'Done'), ('CANCEL', 'Cancelled')]
    )
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True,  null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("localevents:event_detail", args=[str(self.id)])

    class Meta:
        ordering = ['-created_on']


class EventSignup():
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        related_name='signups',
    )
    user_registrant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True;
        related_name='signup_user'
    )
    new_registrant = models.CharField(
        null=True,
        blank=True
    )