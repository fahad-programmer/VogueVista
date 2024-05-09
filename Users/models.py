from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# If you're using a custom user model, replace 'User' with your custom model.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_data/user_{0}/cv/{1}'.format(instance.user.id, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    cv = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return self.user.username

    # Additional methods can be added here. For example, calculating the user's age.
    def age(self):
        return int((timezone.now().date() - self.birth_date).days / 365.25)