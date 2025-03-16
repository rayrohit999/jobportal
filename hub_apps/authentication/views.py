from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from hub_apps.profiles.models import UserProfile


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)  # Auto login after registration
            return redirect('dashboard')  # Redirect to a dashboard page
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.user.is_recruiter:
        return render(request, 'authentication/recruiter_dashboard.html', {'profile': user_profile})
    else:
        return render(request, 'authentication/jobseeker_dashboard.html', {'profile': user_profile})
