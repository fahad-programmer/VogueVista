from rest_framework import serializers
from .models import CompanyProfile
from drf_extra_fields.fields import Base64ImageField
from .models import Job
from Users.models import JobApplication, UserProfile


class CompanyProfileSerializer(serializers.ModelSerializer):

    logo = Base64ImageField(required=False)
    class Meta:
        model = CompanyProfile
        fields = ["company_name", "location", "phone_number", "about_company", "logo"]

class JobSerializer(serializers.ModelSerializer):
    days_since_posted = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ["id", "title", "description", "job_type", "location", "experience", "requirements", "salary", "card_color", "company_name", "logo_url", "role", "days_since_posted"]

    def get_days_since_posted(self, obj):
        """Serializer method field to access the days_since_posted method of the Job model."""
        return obj.days_since_posted()

    def get_company_name(self, obj):
        """Serializer method field to access the company name from the CompanyProfile model."""
        return obj.company.company_name if obj.company else None

    def get_logo_url(self, obj):
        """Serializer method field to access the logo URL from the CompanyProfile model."""
        if obj.company and obj.company.logo:
            request = self.context.get('request')
            logo_url = obj.company.logo.url
            return logo_url
        return None
    


class JobDataSerializer(serializers.ModelSerializer):
    days_since_posted = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"

    def get_days_since_posted(self, obj):
        """Serializer method field to access the days_since_posted method of the Job model."""
        return obj.days_since_posted()

    def get_company_name(self, obj):
        """Serializer method field to access the company name from the CompanyProfile model."""
        return obj.company.company_name if obj.company else None

    def get_logo_url(self, obj):
        """Serializer method field to access the logo URL from the CompanyProfile model."""
        if obj.company and obj.company.logo:
            request = self.context.get('request')
            logo_url = obj.company.logo.url
            return logo_url
        return None
    

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ('company',)  # Exclude company from being required in the request

class JobApplicationSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source='user_profile.user.id')
    username = serializers.CharField(source='user_profile.user.first_name')  # Adjust the source to match your user model
    profile_pic = serializers.CharField(source='user_profile.profile_pic')


    class Meta:
        model = JobApplication
        fields = ['id','user_id', 'username', 'status', 'profile_pic']  # Directly include 'username' and 'status'

