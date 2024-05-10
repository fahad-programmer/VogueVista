from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from Company.models import Job
from django.db.models.signals import post_save, post_delete


# If you're using a custom user model, replace 'User' with your custom model.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_data/user_{0}/cv/{1}'.format(instance.user.id, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), blank=True, null=True)
    cv = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def CreateCompanyProfile(sender, instance, created, **kwargs):
            """Automatically creates an instance if a object is created"""
            if created:
                UserProfile.objects.create(user=instance)

    # Additional methods can be added here. For example, calculating the user's age.
    def age(self):
        return int((timezone.now().date() - self.birth_date).days / 365.25)

class JobApplication(models.Model):
    # Define the possible statuses of a job application
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('reviewing', 'Reviewing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    date_applied = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user_profile.user.username} - {self.job.title}'

    # Additional methods can be added here. For example, a method to update the application status.