# urls.py
from django.urls import path
from .views import UserProfileUpdateView, ProfileInfo, SavedJobsListView, UserProfileView

urlpatterns = [
    path("profileUpdate", UserProfileUpdateView.as_view(), name="UserProfileUpdate"),
    path("profileInfo", ProfileInfo.as_view(), name="profileInfo"),
    path('saved-jobs', SavedJobsListView.as_view(), name='saved-jobs'),
    path('user-profile', UserProfileView.as_view(), name='user-profile')
]