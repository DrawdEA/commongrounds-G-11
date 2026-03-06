from django.contrib import admin
from .models import Event, EventType


class EventAdmin(admin.ModelAdmin):
    model = Event


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
