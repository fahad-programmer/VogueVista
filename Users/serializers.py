# serializers.py
from rest_framework import serializers
from .models import UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_pic','birth_date', 'phone_number', 'gender', 'cv']