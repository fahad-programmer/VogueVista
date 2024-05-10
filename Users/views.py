# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSignupSerializer
from .models import UserProfile

class UserSignupView(APIView):
    def post(self, request):
        """
        Handles the HTTP POST request for user signup.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object.

        """
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            # Checking if the email exists if not then create the user object
            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            #Creating the profile for the user
            user = User.objects.get(email=email)
            userProfile = UserProfile.objects.create(user=user)
            userProfile.save()


            return Response({"success": "Congrats Your Registered Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
