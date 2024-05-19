# views.py
from rest_framework.views import APIView
from .serializers import CompanyProfileSerializer, JobDataSerializer, JobSerializer
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


from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, CompanyProfile
from .serializers import JobSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

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