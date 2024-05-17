from rest_framework import serializers
from .models import CompanyProfile
from drf_extra_fields.fields import Base64ImageField
from .models import Job

class CompanyProfileSerializer(serializers.ModelSerializer):

    logo = Base64ImageField(required=False)
    class Meta:
        model = CompanyProfile
        fields = ["company_name", "location", "phone_number", "about_company", "logo"]

class JobSerializer(serializers.ModelSerializer):
    days_since_posted = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'  # Includes all fields from the Job model plus the days_since_posted

    def get_days_since_posted(self, obj):
        """Serializer method field to access the days_since_posted method of the Job model."""
        return obj.days_since_posted()