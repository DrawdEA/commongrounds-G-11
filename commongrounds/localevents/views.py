from django.shortcuts import render, redirect
from .models import Event, EventSignup
from .forms import EventForm, SignupForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

def event_list(request):
    all_events = Event.objects.all()

    if request.user.is_authenticated:
        profile = request.user.profile
        my_events = Event.objects.filter(organizer=profile)
        signedup_events = Event.objects.filter(signups__user_registrant=profile)
        events = all_events.exclude(id__in=my_events).exclude(id__in=signedup_events)
        ctx = {
            'events': events,
            'my_events': my_events,
            'signedup_events': signedup_events    
        }
        return render(request, 'localevents/event_list.html', ctx)
    else: 
        ctx = {
            'events': all_events
        }
        return render(request, 'localevents/event_list.html', ctx)


def event_detail(request, pk):
    event = Event.objects.get(id=pk)
    signed_up = False
    if request.user.is_authenticated:
        signed_up = event.signups.filter(user_registrant=request.user.profile).exists()
    if request.method == "POST":
        if request.user.is_authenticated:
            EventSignup.objects.create(
                event = event,
                user_registrant = request.user.profile
            )
            if event.signups.count() >= event.event_capacity:
                event.status = 'FULL'
                event.save()
            return redirect('localevents:event_list')
        else:
            return redirect('localevents:event_signup', pk=pk)
    ctx = {
        "event": event,
        "signedup": signed_up}
    return render(request, 'localevents/event_detail.html', ctx)


@login_required
@role_required("Event Organizer")
def event_create(request):
    profile = request.user.profile
    event_form = EventForm()
    if (request.method == "POST"):
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            event = event_form.save()
            event.organizer.add(request.user.profile)
            return redirect('localevents:event_detail', pk=event.pk)
    ctx = {"event_form": event_form, }
    return render(request, 'localevents/event_create.html', ctx)

@login_required
@role_required("Event Organizer")
def event_update(request, pk):
    event = Event.objects.get(pk=pk)
    profile = request.user.profile
    
    if not event.organizer.filter(id=profile.id).exists():
        return redirect('localevents:event_list')

    else:
        event_form = EventForm(request.POST, request.FILES, instance=event)
        if (request.method == "POST"):
            event_form = EventForm(request.POST, request.FILES, instance=event)
            if event_form.is_valid():
                event = event_form.save()
                if event.status != 'DONE' and event.status != 'CANCEL':
                    if event.signups.count() >= event.event_capacity:
                        event.status = 'FULL'
                    else:
                        event.status = 'AVAIL'
                    event.save()
                return redirect('localevents:event_detail', pk=event.pk)
        ctx = {"event_form": event_form}
        return render(request, 'localevents/event_update.html', ctx)

def event_signup(request, pk):
    event = Event.objects.get(pk=pk)
    signup_form = SignupForm(request.POST, request.FILES)
    if signup_form.is_valid() and request.method == 'POST':
        signup = signup_form.save(commit=False)
        signup.event = event
        signup.save()
        if event.signups.count() >= event.event_capacity:
            event.status = 'FULL'
            event.save()
        return redirect('localevents:event_list')
    ctx = {"event": event, "signup_form": signup_form }
    return render(request, 'localevents/event_signup.html', ctx)