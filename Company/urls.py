from django.urls import path
from .views import CompanyProfileUpdateView, JobApplicantsListView, JobListView, JobDetailView, JobCreateAPIView, MyAdsListView

urlpatterns = [
	path("profileUpdate",CompanyProfileUpdateView.as_view())  ,
    path('jobs', JobListView.as_view(), name='job-list'),
    path('jobs/<int:id>', JobDetailView.as_view(), name='job-detail'), 
    path('jobs/create', JobCreateAPIView.as_view(), name='job-create'),
    path('my-ads', MyAdsListView.as_view(), name='my-ads'),
    path('jobs/<int:job_id>/applicants/', JobApplicantsListView.as_view(), name='job-applicants-list')
]
