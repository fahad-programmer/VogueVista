from rest_framework.views import APIView
from .serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .models import UserProfile


class UserProfileUpdateView(APIView):

    authentication_classes = [TokenAuthentication]

    def put(self, request):
        current_user = request.user
        user_profile = UserProfile.objects.get(user=current_user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)