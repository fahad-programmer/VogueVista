from django.contrib import admin
from .models import CompanyProfile, Job

# Register your models here.
admin.site.register(CompanyProfile)
admin.site.register(Job)