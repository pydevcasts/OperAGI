# accounts/views.py
import os
import traceback
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# (در صورت نیاز برای برخی محیط‌ها) سِت کردن endpoint certs به v3:
google_id_token._GOOGLE_OAUTH2_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        id_token_value = request.data.get('id_token')
        if not id_token_value:
            return Response({'error': 'id_token is required'}, status=status.HTTP_400_BAD_REQUEST)

        client_id = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
        if not client_id:
            return Response({'error': 'SERVER_MISCONFIGURED'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # verify token
            request_obj = google_requests.Request()
            idinfo = google_id_token.verify_oauth2_token(id_token_value, request_obj, client_id)

            # idinfo contains e.g. 'email', 'email_verified', 'name'
            email = idinfo.get('email')
            verified = idinfo.get('email_verified', False)
            name = idinfo.get('name') or ''
            first_name = idinfo.get('given_name') or ''
            last_name = idinfo.get('family_name') or ''

            if not email:
                return Response({'error': 'Google token did not contain email'}, status=status.HTTP_400_BAD_REQUEST)

            # get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first_name or name,
                    'is_active': True,
                }
            )

            # optionally: attach SocialAccount entry if you want full allauth social flow
            # but for basic use, we just create/find the user.

            # produce JWT tokens
            refresh = RefreshToken.for_user(user)
            data = {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'user': {
                    'email': user.email,
                    'name': user.first_name,
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
