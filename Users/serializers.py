# serializers.py
import io
import PyPDF2
from rest_framework import serializers
from .models import JobApplication, Notification, UserProfile
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from Company.serializers import JobSerializer

# Serializer for handling PDF files in Base64 format
class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    # Method to get file extension
    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfReader(io.BytesIO(decoded_file))
        except Exception as e:  # Adjusted exception handling
            print(e)
        else:
            return 'pdf'

# Serializer for UserProfile model
class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = Base64ImageField(required=False)
    cv = PDFBase64File(required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_pic','birth_date', 'phone_number', 'gender', 'cv']

# Serializer for UserProfile data
class UserProfileDataSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    name  = serializers.CharField(source='user.first_name', max_length=100)
    class Meta:
        model = UserProfile
        fields = ['name', 'profile_pic','birth_date', 'phone_number', 'gender', 'cv', 'email']

# Serializer for JobApplication model
class JobApplicationSerializer(serializers.Serializer):
    job_id = serializers.CharField(max_length=50)

# Serializer for Notification model
class NotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at']

    # Method to get formatted date
    def get_created_at(self, obj):
        return obj.formatted_date()

# Serializer for AppliedJob model
class AppliedJobSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)  # Nested serialization

    class Meta:
        model = JobApplication
        fields = ['job']  # Include 'job' to serialize job details

    # Method to represent the 'job' field directly
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        job = representation.pop('job', None)  # Remove the 'job' key and get its value
        return job if job else {}
