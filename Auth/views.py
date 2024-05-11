from Auth.models import UserVerification
from .serializers import SignupSerializer, VerificationSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Company.models import CompanyProfile
from Users.models import UserProfile
from django.core.mail import send_mail
import random
from rest_framework.authtoken.models import Token

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

            # Generate a random 6-digit number
            verification_code = random.randrange(100000, 999999)

            # Create the user object with not active status
            set_user_nonactive = User.objects.get(email=email)
            set_user_nonactive.is_active = False
            set_user_nonactive.save()
           

            # Send email with verification code
            send_mail(
                'Email Verification Code',
                f'Your verification code is: {verification_code}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
         

            user = User.objects.get(email=email)
            # Create UserVerification instance to store the verification code
            UserVerification.objects.create(user=user, verification_code=verification_code)

            if user_type == "Company":
                #Creating the profile for the Company
                companyProfile = CompanyProfile.objects.create(user=user)
                companyProfile.save()
            else:
                # Creating the profile for simple user
                userProfile = UserProfile.objects.create(user=user)
                userProfile.save()          


                # Generate a token for the newly created user
            user = User.objects.get(email=email)
            token, created = Token.objects.get_or_create(user=user)

            # Return the token in the response
            return Response({'token': token.key, "message": "Account created."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework import serializers

class VerifyCodeApi(APIView):
    def post(self, request):
        """
        Handles the HTTP POST request for verifying the code sent during signup.

        Args:
            request (HttpRequest): The HTTP request object containing the verification code.

        Returns:
            Response: The HTTP response object indicating the verification status.
        """
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = serializer.validated_data.get('verification_code')  # Corrected 'code' to 'verification_code'
            email = serializer.validated_data.get('email')

            try:
                current_user = User.objects.get(email=email)
                userVerification = UserVerification.objects.get(user=current_user)  # Get the UserVerification object

                if userVerification.verification_code == verification_code:
                    # Update user status to active
                    current_user.is_active = True
                    current_user.save()

                    # Delete the UserVerification object
                    userVerification.delete()

                    return Response({"success": "Verification successful. Your account is now active."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid verification code. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            except UserVerification.DoesNotExist:
                return Response({"error": "User verification not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)