from rest_framework.views import APIView

from Company.models import CompanyProfile
from .serializers import UserProfileDataSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .models import UserProfile
from rest_framework.generics import ListAPIView
from Company.serializers import JobSerializer
from Company.models import Job

class UserProfileUpdateView(APIView):
    """
    API View to update the user profile.
    Requires TokenAuthentication for user authentication.
    """

    authentication_classes = [TokenAuthentication]

    def put(self, request):
        """
        Handle PUT request to update the user profile.

        Parameters:
        - request: Request object containing user data.

        Returns:
        - Response with updated user profile data or errors.

        Process:
        1. Retrieve the current authenticated user.
        2. Get the user profile associated with the current user.
        3. Initialize the UserProfileSerializer with the user profile data and request data.
        4. Check if the serializer data is valid.
        5. If valid, save the updated user profile data.
        6. Return a success response with the updated data.
        7. If not valid, return an error response with the serializer errors.
        """
        current_user = request.user
        user_profile = UserProfile.objects.get(user=current_user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Profile Updated"}, status=status.HTTP_200_OK)
        print(serializer.errors) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileInfo(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        current_user = request.user
        first_name = current_user.first_name
        
        # Check if the user has a CompanyProfile or UserProfile
        if CompanyProfile.objects.filter(user=current_user).exists():
            profile = CompanyProfile.objects.get(user=current_user)
            profile_pic_url = profile.logo.url
            return Response({"name": first_name, "profile_pic": profile_pic_url}, status=status.HTTP_200_OK)
        else:
            profile = UserProfile.objects.get(user=current_user)
            profile_pic_url = profile.profile_pic.url
            return Response({"name": first_name, "profile_pic": profile_pic_url}, status=status.HTTP_200_OK)
        
class SavedJobsListView(ListAPIView):
    serializer_class = JobSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Job.objects.filter(savedjobs__user=user)
    
class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileDataSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile does not exist'}, status=404)