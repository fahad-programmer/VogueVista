from django.urls import path
from .views import CompanyProfileUpdateView, JobApplicantsListView, JobListView, JobDetailView, JobCreateAPIView, MyAdsListView, UpdateJobApplicationStatus

urlpatterns = [
    # URL for updating company profile
    path("profileUpdate",CompanyProfileUpdateView.as_view()),

    # URL for listing all jobs
    path('jobs', JobListView.as_view(), name='job-list'),

    # URL for viewing details of a specific job by its ID
    path('jobs/<int:id>', JobDetailView.as_view(), name='job-detail'), 

    # URL for creating a new job
    path('jobs/create', JobCreateAPIView.as_view(), name='job-create'),

    # URL for viewing all of my ads
    path('my-ads', MyAdsListView.as_view(), name='my-ads'),

    # URL for listing all applicants of a specific job by its ID
    path('jobs/<int:job_id>/applicants', JobApplicantsListView.as_view(), name='job-applicants-list'),

    # URL for updating the status of a specific application by its ID
    path('applications/<int:application_id>/status', UpdateJobApplicationStatus.as_view(), name='update_application_status'),
]
