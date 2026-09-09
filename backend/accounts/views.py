# accounts/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import GoogleLoginSerializer, SubscriptionPlanSerializer, UserSubscriptionSerializer
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()
from .models import SubscriptionPlan, UserSubscription


class GoogleLogin(SocialLoginView):
    """Complete the standard allauth OAuth flow for the frontend access token."""
    adapter_class = GoogleOAuth2Adapter

class InstagramLogin(SocialLoginView):
    adapter_class = InstagramOAuth2Adapter

class TwitterLogin(SocialLoginView):
    adapter_class = TwitterOAuthAdapter


class SubscriptionPlanList(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True)
        return Response(SubscriptionPlanSerializer(plans, many=True).data)


class CurrentSubscriptionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            subscription = request.user.subscription
        except UserSubscription.DoesNotExist:
            return Response({'subscription': None})
        return Response({'subscription': UserSubscriptionSerializer(subscription).data})

    def post(self, request):
        try:
            plan = SubscriptionPlan.objects.get(slug=request.data.get('plan'), is_active=True)
        except SubscriptionPlan.DoesNotExist:
            return Response({'plan': 'Unknown plan.'}, status=status.HTTP_400_BAD_REQUEST)
        subscription, _ = UserSubscription.objects.update_or_create(
            user=request.user,
            defaults={
                'plan': plan,
                'status': UserSubscription.Status.TRIAL,
                'current_period_end': timezone.now() + timedelta(days=14),
            },
        )
        return Response({'subscription': UserSubscriptionSerializer(subscription).data})
