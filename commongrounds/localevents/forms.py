from django import forms
from .models import Event, EventSignup


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']


class SignupForm(forms.ModelForm):
    class Meta:
        model = EventSignup
        fields = ['new_registrant']
        label = {'new_registrant': 'Name'}
