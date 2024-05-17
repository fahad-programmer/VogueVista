from django.urls import path
from .views import CompanyProfileUpdateView, JobListView

urlpatterns = [
	path("profileUpdate",CompanyProfileUpdateView.as_view())  ,
    path('jobs', JobListView.as_view(), name='job-list'),  
]
