from django.urls import path
from .views import SignupApi, VerifyCodeApi, CheckUserActive, ResendVerificationEmail, LoginApi, SocialSignupView

urlpatterns = [
    path("signup", SignupApi.as_view(), name="Signup"),
    path("verify-email", VerifyCodeApi.as_view(), name="verify email"),
    path("check-token", CheckUserActive.as_view(), name="Check Token"),
    path("resend-email", ResendVerificationEmail.as_view(), name="resend-email"),
    path("login", LoginApi.as_view(), name="login"),
    path("social-auth", SocialSignupView.as_view(), name="Social Auth")
]