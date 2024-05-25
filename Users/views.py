from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from Company.models import CompanyProfile
from .serializers import JobApplicationSerializer, NotificationSerializer, UserProfileDataSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .models import JobApplication, Notification, UserProfile, SavedJobs
from rest_framework.generics import ListAPIView, CreateAPIView
from Company.serializers import JobSerializer
from Company.models import Job
from django.db.models import Q


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
        

class CreateJobApplication(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        job_id = request.data.get('job_id')
        user = request.user
        try:
            job = Job.objects.get(id=job_id)
            userProfile = UserProfile.objects.get(user=user)

            # Check if the user has already applied for this job
            if JobApplication.objects.filter(user_profile=userProfile, job=job).exists():
                return Response({"error": "You have already applied for this job"}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new job application
            JobApplication.objects.create(user_profile=userProfile, job=job)
            return Response({"success": "Job Application Submitted Successfully"}, status=status.HTTP_200_OK)

        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)



class UserJobApplicationsList(ListAPIView):
    serializer_class = JobApplicationSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        userProfile = UserProfile.objects.get(user=user)
        return JobApplication.objects.filter(user_profile=userProfile)


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')
    
class UserProfileDetailView(APIView):
    """
    Retrieve UserProfile data by user ID.
    """
    def get(self, request, user_id):
        # Retrieve the UserProfile instance using the user_id
        user_profile = get_object_or_404(UserProfile, user__id=user_id)
        serializer = UserProfileDataSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SaveJobView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user = request.user
        job_id = request.data.get('job_id')
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        if SavedJobs.objects.filter(user=user, job=job).exists():
            return Response({"error": "Job is already saved"}, status=status.HTTP_400_BAD_REQUEST)

        saved_job = SavedJobs.objects.create(user=user, job=job)
        serializer = JobSerializer(saved_job)
        return Response({"success":"Job Saved Successfully"}, status=status.HTTP_201_CREATED)



class JobSearchView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.data.get('query', '')
        if query:
            jobs = Job.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(location__icontains=query) |
                Q(experience__icontains=query) |
                Q(requirements__icontains=query) |
                Q(role__icontains=query)
            )
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Please provide a search term."})
