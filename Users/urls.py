# urls.py
from django.urls import path
from .views import UserProfileUpdateView, ProfileInfo

urlpatterns = [
    path("profileUpdate", UserProfileUpdateView.as_view(), name="UserProfileUpdate"),
    path("profileInfo", ProfileInfo.as_view(), name="profileInfo")
]