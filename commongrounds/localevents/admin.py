from django.contrib import admin
from .models import Event, EventType, EventSignup


class EventAdmin(admin.ModelAdmin):
    model = Event
    filter_vertical = ('organizer',)


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType


class EventSignupAdmin(admin.ModelAdmin):
    model = EventSignup


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventSignup, EventSignupAdmin)
