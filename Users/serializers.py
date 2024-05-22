# serializers.py
import io
import PyPDF2
from rest_framework import serializers
from .models import UserProfile
from drf_extra_fields.fields import Base64ImageField, Base64FileField


class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ['pdf']

    def get_file_extension(self, filename, decoded_file):
        try:
            PyPDF2.PdfReader(io.BytesIO(decoded_file))
        except Exception as e:  
            print(e)
        else:
            return 'pdf'

class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = Base64ImageField(required=False)
    cv = PDFBase64File(required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_pic','birth_date', 'phone_number', 'gender', 'cv']


