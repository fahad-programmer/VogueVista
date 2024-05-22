from django.contrib import admin
from .models import UserProfile, SavedJobs

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(SavedJobs)