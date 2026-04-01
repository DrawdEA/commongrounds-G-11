from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileUpdateForm

# Create your views here.
def index(request):
    return HttpResponse("This came from the index view of the accounts app")

@login_required
def profile_update(request, username):
    profile = Profile.objects.get(user=request.user)
    # https://docs.djangoproject.com/en/6.0/topics/forms/modelforms/#overriding-the-default-fields
    form = ProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:index')
    context = {'form': form, 'display_name': profile.display_name}
    return render(request, 'accounts/profile_update_form.html', context)