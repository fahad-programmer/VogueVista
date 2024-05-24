# serializers.py
import io
import PyPDF2
from rest_framework import serializers
from .models import JobApplication, Notification, UserProfile
from drf_extra_fields.fields import Base64ImageField, Base64FileField


class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfReader(io.BytesIO(decoded_file))
        except Exception as e:  # Adjusted exception handling
            print(e)
        else:
            return 'pdf'

class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = Base64ImageField(required=False)
    cv = PDFBase64File(required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_pic','birth_date', 'phone_number', 'gender', 'cv']


class UserProfileDataSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    name  = serializers.CharField(source='user.first_name', max_length=100)
    class Meta:
        model = UserProfile
        fields = ['name', 'profile_pic','birth_date', 'phone_number', 'gender', 'cv', 'email']

class JobApplicationSerializer(serializers.Serializer):
    job_id = serializers.CharField(max_length=50)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'read', 'created_at']