from rest_framework import serializers
from .models import CompanyProfile
from drf_extra_fields.fields import Base64ImageField

class CompanyProfileSerializer(serializers.ModelSerializer):

    logo = Base64ImageField(required=False)
    class Meta:
        model = CompanyProfile
        fields = ["company_name", "location", "phone_number", "about_company", "logo"]
