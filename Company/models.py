from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_data/user_{0}/profile_image/{1}'.format(instance.user.id, filename)

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    about_company = models.TextField()
    logo = models.ImageField(upload_to=user_directory_path)

    def __str__(self):
        return self.company_name
    
    @receiver(post_save, sender=User)
    def CreateCompanyProfile(sender, instance, created, **kwargs):
            """Automatically creates an instance if a object is created"""
            if created:
                CompanyProfile.objects.create(user=instance)

class Job(models.Model):
    # Job types can be defined as a tuple of tuples, where the first value in each tuple is the value to be stored in the database and the second value is the human-readable name
    JOB_TYPES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    )

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    job_type = models.CharField(max_length=50, choices=JOB_TYPES)
    location = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)  
    salary = models.CharField(max_length=255)  
    requirements = models.TextField()  
    role = models.CharField(max_length=255) 
    card_color = models.CharField(max_length=7) 
    website_link = models.URLField(max_length=200, blank=True, null=True)  
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def days_since_posted(self):
        """Returns a message indicating when the job was posted."""
        now = timezone.now()
        delta = now - self.date_posted

        if delta.days == 0:
            return "Posted today"
        else:
            return f"Posted {delta.days} days ago"