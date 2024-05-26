# urls.py
from django.urls import path
from .views import NotificationListView, UserProfileDetailView, UserProfileUpdateView, ProfileInfo, SavedJobsListView, UserProfileView, CreateJobApplication, UserJobApplicationsList, SaveJobView, JobSearchView

urlpatterns = [
    # Route for updating user profile
    path("profileUpdate", UserProfileUpdateView.as_view(), name="UserProfileUpdate"),
    
    # Route for getting profile information
    path("profileInfo", ProfileInfo.as_view(), name="profileInfo"),
    
    # Route for listing saved jobs
    path('saved-jobs', SavedJobsListView.as_view(), name='saved-jobs'),
    
    # Route for viewing user profile
    path('user-profile', UserProfileView.as_view(), name='user-profile'),
    
    # Route for applying to a job
    path("apply-job", CreateJobApplication.as_view(), name="createJobApplication"),
    
    # Route for listing user's job applications
    path("my-jobs-application", UserJobApplicationsList.as_view(), name="jobs-list"),
    
    # Route for listing notifications
    path('notifications', NotificationListView.as_view(), name='notification_list'),
    
    # Route for viewing user profile details
    path('user-profile/<int:user_id>', UserProfileDetailView.as_view(), name='user-profile-detail'),
    
    # Route for saving jobs
    path("save-jobs", SaveJobView.as_view(), name="Saved Job"),
    
    # Route for job search
    path('search', JobSearchView.as_view(), name='job_search'),
]
