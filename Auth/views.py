from django.shortcuts import render
from .serializers import SignupSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Company.models import CompanyProfile
from Users.models import UserProfile

# Create your views here.
class SignupApi(APIView):
    def post(self, request):
        """
        Handles the HTTP POST request for user signup.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object.

        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user_type = serializer.validated_data.get("type")

            # Checking if the email exists if not then create the user object
            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            user = User.objects.get(email=email)

            if user_type == "Company":
                #Creating the profile for the Company
                companyProfile = CompanyProfile.objects.create(user=user)
                companyProfile.save()
            else:
                # Creating the profile for simple user
                userProfile = UserProfile.objects.create(user=user)
                userProfile.save()          


            return Response({"success": "Congrats Your Registered Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)