# urls.py
from django.urls import path
from .views import NotificationListView, UserProfileDetailView, UserProfileUpdateView, ProfileInfo, SavedJobsListView, UserProfileView, CreateJobApplication, UserJobApplicationsList

urlpatterns = [
    path("profileUpdate", UserProfileUpdateView.as_view(), name="UserProfileUpdate"),
    path("profileInfo", ProfileInfo.as_view(), name="profileInfo"),
    path('saved-jobs', SavedJobsListView.as_view(), name='saved-jobs'),
    path('user-profile', UserProfileView.as_view(), name='user-profile'),
    path("apply-job", CreateJobApplication.as_view(), name="createJobApplication"),
    path("my-jobs-application", UserJobApplicationsList.as_view(), name="jobs-list"),
    path('notifications', NotificationListView.as_view(), name='notification_list'),
    path('user-profile/<int:user_id>', UserProfileDetailView.as_view(), name='user-profile-detail')
]