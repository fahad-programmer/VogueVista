from django.contrib import admin
from django.urls import path, include
# Import settings and static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("Auth.urls")),
    path("user/", include("Users.urls")),
    path("company/", include("Company.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
