from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("Auth.urls")),
    path("user/", include("Users.urls")),
    path("company/", include("Company.urls"))
]
