from django.urls import path
from .views import SignupApi

urlpatterns = [
    path("signup", SignupApi.as_view(), name="Signup"),

]