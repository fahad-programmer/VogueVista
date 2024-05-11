from django.urls import path
from .views import SignupApi, VerifyCodeApi

urlpatterns = [
    path("signup", SignupApi.as_view(), name="Signup"),
    path("verify-email", VerifyCodeApi.as_view(), name="verify email")

]