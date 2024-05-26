# Importing necessary modules
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Company.models import Job
from model_utils import FieldTracker
from django.utils import timezone

# Function to get the directory path for user's CV
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_data/user_{0}/cv/{1}'.format(instance.user.id, filename)

# Function to get the directory path for user's profile picture
def user_profile_pic_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_data/user_{0}/profile_image/{1}'.format(instance.user.id, filename)

# UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(null=True, blank=True, upload_to=user_profile_pic_directory_path)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('other', 'Other')), blank=True, null=True)
    cv = models.FileField(upload_to=user_directory_path, blank=True, null=True)

    # String representation of the model
    def __str__(self):
        return self.user.username

    # Method to calculate user's age
    def age(self):
        return int((timezone.now().date() - self.birth_date).days / 365.25)

# JobApplication model
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
    tracker = FieldTracker(fields=['status'])
    date_applied = models.DateTimeField(default=timezone.now)

    # String representation of the model
    def __str__(self):
        return f'{self.user_profile.user.username} - {self.job.title}'

# SavedJobs model
class SavedJobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    # String representation of the model
    def __str__(self) -> str:
        return f"{self.user.first_name} has stored job of{self.job.title}"

# Notification model
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Method to format the date
    def formatted_date(self):
        return self.created_at.strftime('%d %b, %Y | %H:%M %p')

    # String representation of the model
    def __str__(self):
        return f'Notification for {self.recipient.username}'
