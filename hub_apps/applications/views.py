from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from hub_apps.jobs.models import Job
from hub_apps.applications.models import JobApplication
from .forms import JobApplicationForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.is_recruiter:
        return redirect('list_jobs')  # Prevent recruiters from applying

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('list_jobs')  # Redirect after successful application
    else:
        form = JobApplicationForm()

    return render(request, 'applications/apply.html', {'form': form, 'job': job})

@login_required
def view_applications(request):
    if not request.user.is_recruiter:
        return redirect('dashboard')  # Prevent job seekers from accessing this page

    jobs_posted = Job.objects.filter(posted_by=request.user)
    applications = JobApplication.objects.filter(job__in=jobs_posted)

    return render(request, 'applications/view_applications.html', {'applications': applications})

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def update_application_status(request, application_id):
    if request.method == 'POST' and request.user.is_recruiter:
        application = get_object_or_404(JobApplication, id=application_id, job__posted_by=request.user)
        old_status = application.status
        new_status = request.POST.get('status', 'Pending')

        if old_status != new_status:
            application.status = new_status
            application.save()

            # Render the email template
            subject = "Your Job Application Status Updated"
            html_message = render_to_string('emails/application_status_update.html', {
                'applicant': application.applicant.username,
                'job_title': application.job.title,
                'company': application.job.company,
                'status': new_status,
            })
            plain_message = strip_tags(html_message)  # Convert HTML to plain text

            email = EmailMultiAlternatives(subject, plain_message, 'your-email@gmail.com', [application.applicant.email])
            email.attach_alternative(html_message, "text/html")
            email.send()

        return HttpResponseRedirect(reverse('view_applications'))

@login_required
def track_applications(request):
    if request.user.is_recruiter:
        return redirect('dashboard')  # Recruiters shouldn't see this page

    applications = JobApplication.objects.filter(applicant=request.user).select_related('job')
    paginator = Paginator(applications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'applications/track_applications.html', {'applications': applications,'page_obj':page_obj})

@login_required
def view_job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)  # Ensure only job owner can see applicants
    applications = JobApplication.objects.filter(job=job).select_related('applicant')

    return render(request, 'applications/view_job_applicants.html', {'job': job, 'applications': applications})
