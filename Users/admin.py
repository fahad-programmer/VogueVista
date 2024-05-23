from django.contrib import admin
from .models import UserProfile, SavedJobs, JobApplication, Notification

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(SavedJobs)
admin.site.register(JobApplication)
admin.site.register(Notification)