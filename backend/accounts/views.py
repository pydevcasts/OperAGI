# accounts/views.py
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from dj_rest_auth.registration.views import RegisterView
from accounts.serializers import RegisterSerializer


RegisterView.serializer_class = RegisterSerializer



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL or "http://127.0.0.1:8000/api/v1/auth/google/callback/"
    client_class = OAuth2Client