# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GoogleLoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class GoogleLogin(APIView):
    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create_or_update_user(serializer.validated_data)
            return Response({
                'message': 'User synced successfully',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)