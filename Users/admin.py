from django.contrib import admin
from .models import UserProfile, SavedJobs, JobApplication

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(SavedJobs)
admin.site.register(JobApplication)