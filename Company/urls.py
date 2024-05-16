from django.urls import path
from .views import CompanyProfileUpdateView

urlpatterns = [
	path("profileUpdate",CompanyProfileUpdateView.as_view())    
]
