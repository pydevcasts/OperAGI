# accounts/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GoogleLoginSerializer
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter

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
    



# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter

class InstagramLogin(SocialLoginView):
    adapter_class = InstagramOAuth2Adapter

class TwitterLogin(SocialLoginView):
    adapter_class = TwitterOAuthAdapter
