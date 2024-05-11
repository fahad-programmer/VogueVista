from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=10)  # Adjust the max length as needed