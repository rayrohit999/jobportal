from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from hub_apps.profiles.models import UserProfile
from hub_apps.applications.models import JobApplication
from hub_apps.jobs.models import Job

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
        # Recruiter Dashboard Context
        jobs = Job.objects.filter(posted_by=request.user)
        active_jobs_count = jobs.filter(is_active=True).count()
        total_applications = JobApplication.objects.filter(job__posted_by=request.user).count()
        pending_applications_count = JobApplication.objects.filter(job__posted_by=request.user, status='Pending').count()
        hired_count = JobApplication.objects.filter(job__posted_by=request.user, status='Accepted').count()  # Mapping 'Accepted' to 'hired'
        recent_jobs = jobs.order_by('-created_at')[:3]
        recent_applications = JobApplication.objects.filter(job__posted_by=request.user).order_by('-applied_at')[:5]

        return render(request, 'authentication/recruiter_dashboard.html', {
            'profile': user_profile,
            'active_jobs_count': active_jobs_count,
            'total_applications': total_applications,
            'pending_applications_count': pending_applications_count,
            'hired_count': hired_count,
            'recent_jobs': recent_jobs,
            'recent_applications': recent_applications,
        })
    elif request.user.is_superuser:
        return redirect('admin:index')
    else:
        # Job Seeker Dashboard Context
        applications = JobApplication.objects.filter(applicant=request.user)
        recent_applications = applications.order_by('-applied_at')[:5]
        applications_count = applications.count()
        pending_applications_count = applications.filter(status='Pending').count()
        saved_jobs_count = 0  # Replace with SavedJob model logic if exists
        interviews_count = 0  # Replace with Interview model logic if exists
        applications_progress = min(applications_count * 10, 100)  # Example progress

        return render(request, 'authentication/jobseeker_dashboard.html', {
            'profile': user_profile,
            'applications_count': applications_count,
            'pending_applications_count': pending_applications_count,
            'recent_applications': recent_applications,
            'saved_jobs_count': saved_jobs_count,
            'interviews_count': interviews_count,
            'applications_progress': applications_progress,
        })