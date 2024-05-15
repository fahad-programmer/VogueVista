# urls.py
from django.urls import path
from .views import UserProfileUpdateView

urlpatterns = [
    path("profileUpdate", UserProfileUpdateView.as_view(), name="UserProfileUpdate")
]