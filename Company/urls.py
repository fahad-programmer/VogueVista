from django.urls import path
from .views import CompanySignupView

urlpatterns = [
   path("auth/signup", CompanySignupView.as_view(), name="companyView")
]
