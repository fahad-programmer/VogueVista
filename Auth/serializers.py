from rest_framework import serializers
from django.contrib.auth.models import User

class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class VerificationSerializer(serializers.Serializer):
    code = serializers.CharField()
    email = serializers.EmailField()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    type = serializers.CharField(write_only=True)  # Add the 'type' field here

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password', 'type')  # Include 'type' in the fields

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            password=validated_data['password']
        )
        # Set the 'type' field on the user object
        user.type = validated_data.get('type')
        user.save()
        
        return user
    
class SocialSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    account_type = serializers.ChoiceField(choices=['user', 'Company'])
    first_name = serializers.CharField()