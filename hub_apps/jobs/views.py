from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job
from django.core.paginator import Paginator

@login_required
def post_job(request):
    if not request.user.is_recruiter:
        return redirect('dashboard')  # Prevent job seekers from posting

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user  # Assign recruiter as the job owner
            job.save()
            return redirect('list_jobs')  # Redirect to job listing after posting
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})



def list_jobs(request):
    jobs = Job.objects.filter(is_active=True)  # Show only active jobs

    # Get search query and filters from request
    search_query = request.GET.get('q', '')
    job_type_filter = request.GET.get('job_type', '')
    location_filter = request.GET.get('location', '')
    sort_option = request.GET.get('sort', 'newest')  # Default: Newest jobs first


    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    if job_type_filter:
        jobs = jobs.filter(job_type=job_type_filter)

    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)

    if sort_option == 'newest':
        jobs = jobs.order_by('-created_at')  # Newest jobs first
    elif sort_option == 'highest_salary':
        jobs = jobs.order_by('-salary')  # Highest salary first


    paginator = Paginator(jobs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/list_jobs.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'job_type_filter': job_type_filter,
        'location_filter': location_filter,
        'sort_option': sort_option,
    })



@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)  # Ensure only the recruiter can edit

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('list_jobs')  # Redirect after saving changes
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)  # Ensure only the recruiter can delete
    if request.method == 'POST':
        job.delete()
        return redirect('list_jobs')  # Redirect after deleting
    return render(request, 'jobs/confirm_delete.html', {'job': job})
