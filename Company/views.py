# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from Users.models import JobApplication
from .serializers import CompanyProfileSerializer, JobApplicationSerializer, JobDataSerializer, JobSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .models import CompanyProfile, Job
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView, CreateAPIView

class CompanyProfileUpdateView(APIView):
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
        2. Get the company profile associated with the current user.
        3. Initialize the UserProfileSerializer with the user profile data and request data.
        4. Check if the serializer data is valid.
        5. If valid, save the updated user profile data.
        6. Return a success response with the updated data.
        7. If not valid, return an error response with the serializer errors.
        """
        current_user = request.user
        company_profile = CompanyProfile.objects.get(user=current_user)
        serializer = CompanyProfileSerializer(company_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Profile Updated"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JobListView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobDetailView(RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobDataSerializer
    lookup_field = 'id'

class JobCreateAPIView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        """
        Perform create operation for a new object.

        Args:
        serializer: Serializer instance for the object to be created.

        Returns:
        None
        """
        user = self.request.user
        companyProfile = CompanyProfile.objects.get(user=user)
        try:
            serializer.save(company=companyProfile)
        except Exception as e:
            print(serializer.errors)

    def create(self, request, *args, **kwargs):
        """
        Create a new object instance and return a custom response.

        Args:
        request: The HTTP request instance.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

        Returns:
        Response: A DRF Response instance with a custom success message.
        """
        response = super().create(request, *args, **kwargs)
        return Response({"success": "Job posted successfully"}, status=status.HTTP_200_OK)


class MyAdsListView(ListAPIView):
    serializer_class = JobSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """
        This view should return a list of all the jobs
        posted by the company of the currently authenticated user.
        """
        user = self.request.user
        if hasattr(user, 'company_profile'):
            return Job.objects.filter(company=user.company_profile)
        else:
            return Job.objects.none()  # Return an empty queryset if the user has no company profile
        
class JobApplicantsListView(ListAPIView):
    serializer_class = JobApplicationSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        job = Job.objects.get(id=job_id)

        # Check if the current user is associated with the company that posted the job
        return JobApplication.objects.filter(job=job).select_related('user_profile__user')


class UpdateJobApplicationStatus(APIView):
    authentication_classes = [TokenAuthentication]

    def patch(self, request, application_id):
        application = get_object_or_404(JobApplication, id=application_id)
        job_status = request.data.get('status')
        if job_status not in ['accepted', 'rejected']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        if application.status == job_status:
            return Response({"error":"Already Changed The Status Of The Job"}, status=status.HTTP_400_BAD_REQUEST)

        application.status = job_status
        application.save()
        return Response({"Success": "Job application status updated"}, status=status.HTTP_200_OK)
