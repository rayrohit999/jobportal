from django.urls import path
from .views import post_job,list_jobs,edit_job,delete_job

urlpatterns = [
    path('post/', post_job, name='post_job'),
    path('', list_jobs, name='list_jobs'),
    path('<int:job_id>/edit/', edit_job, name='edit_job'),
    path('<int:job_id>/delete/', delete_job, name='delete_job'),
]
