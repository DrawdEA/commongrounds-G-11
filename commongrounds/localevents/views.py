from django.shortcuts import render
from .models import Event

def event_list(request):
    events = Event.objects.all()
    ctx = {
    'events': events
    }
    return render(request, 'localevents/event_list.html', ctx)

def event_detail(request, pk):
    event = Event.objects.get(id=pk)
    ctx = { "event" : event}

    return render(request, 'localevents/event_detail.html', ctx)

