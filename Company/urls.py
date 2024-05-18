from django.urls import path
from .views import CompanyProfileUpdateView, JobListView, JobDetailView, JobCreateAPIView

urlpatterns = [
	path("profileUpdate",CompanyProfileUpdateView.as_view())  ,
    path('jobs', JobListView.as_view(), name='job-list'),
    path('jobs/<int:id>', JobDetailView.as_view(), name='job-detail'), 
    path('jobs/create', JobCreateAPIView.as_view(), name='job-create')
]
