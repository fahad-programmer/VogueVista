from Auth.models import SocialAccount, UserVerification
from .serializers import ResendEmailSerializer, SignupSerializer, SocialSignupSerializer, UserLoginSerializer, VerificationSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Company.models import CompanyProfile
from Users.models import UserProfile
from django.core.mail import send_mail
import random
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

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

            # Generate a random 4-digit number
            verification_code = random.randrange(1000, 9999)

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
            verification_code = serializer.validated_data.get('code')  # Corrected 'code' to 'verification_code'
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
    

class CheckUserActive(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        if user.is_active:
            return Response({"success": "User is active"}, status=status.HTTP_200_OK)
   


class ResendVerificationEmail(APIView):
    def post(self, request):

        serializer = ResendEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            if user.is_active:
                return Response({"error": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a new verification code
            verification_code = random.randint(1000, 9999)

            # Update the verification code for the user
            user_verification, created = UserVerification.objects.get_or_create(user=user)
            user_verification.verification_code = verification_code
            user_verification.save()

            # Send the email with the new verification code
            send_mail(
                'Email Verification Code',
                f'Your new verification code is: {verification_code}',
                'vogue-vista@gmail.com',
                [email],
                fail_silently=False,
            )
        return Response({"Success": "Verification email resent successfully"}, status=status.HTTP_200_OK)

class LoginApi(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            if not user.check_password(password):
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

            token, created = Token.objects.get_or_create(user=user)

            # Check if UserProfile exists for the user
            if hasattr(user, 'profile'):
                return Response({"type": "user", "token": token.key}, status=status.HTTP_200_OK)
            # Check if CompanyProfile exists for the user
            elif hasattr(user, 'company_profile'):
                return Response({"type": "Company", "token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User profile not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SocialSignupView(APIView):
    def post(self, request):
        serializer = SocialSignupSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            account_type = user_data['account_type']
            email = user_data['email']

            # Check if user already exists
            try:
                user = User.objects.get(email=email)
                token, created = Token.objects.get_or_create(user=user)
                # Check if UserProfile or CompanyProfile exists for the user
                if UserProfile.objects.filter(user=user).exists():
                    return Response({"type": "user", "token": token.key}, status=status.HTTP_200_OK)
                elif CompanyProfile.objects.filter(user=user).exists():
                    return Response({"type": "Company", "token": token.key}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                # Create User
                user = User.objects.create_user(
                    username=email,  # Using email as username
                    email=email,
                    first_name=user_data['first_name'],
                    password=''  # You can set a default password or generate one
                )
                user.save()


                # Create UserProfile based on account type
                if account_type == 'user':
                    UserProfile.objects.create(user=user)
                else:
                    CompanyProfile.objects.create(user=user)

                token, created = Token.objects.get_or_create(user=user)

                return Response({"type": account_type, "token": token.key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
