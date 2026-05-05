from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import CustomUserCreationForm, ProfileUpdateForm

# Create your views here.
def index(request):
    return HttpResponse("You are at the index of the accounts page.")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user,
                                   display_name=user.username,
                                   email_address=form.cleaned_data['email'],
                                   role=Profile.COMMUNITY_MEMBER)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_update(request, username):
    # If user tries to access a different profile
    if request.user.username != username:
        return HttpResponse("Sorry, you can't access this.")
    
    profile = Profile.objects.get(user=request.user)
    # https://docs.djangoproject.com/en/6.0/topics/forms/modelforms/#overriding-the-default-fields
    form = ProfileUpdateForm(instance=profile)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile_update', username)
    context = {'form': form, 'display_name': profile.display_name}
    return render(request, 'accounts/profile_update_form.html', context)