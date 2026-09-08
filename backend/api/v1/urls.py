# api/v1/urls.py

from django.urls import path, include
from dj_rest_auth.views import PasswordResetConfirmView
from accounts.views import CurrentSubscriptionView, GoogleLogin, InstagramLogin, SubscriptionPlanList, TwitterLogin

urlpatterns = [
    path('plans/', SubscriptionPlanList.as_view(), name='subscription-plans'),
    path('subscription/', CurrentSubscriptionView.as_view(), name='current-subscription'),
    path('content_generator/', include('content_generator.urls')),
    path('social/', include('social_accounts.urls')), 
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # Override: JSON API for password reset confirm 
    path(
        'rest-auth/password/reset/confirm/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm_json'
    ),
    # Standard URL for email link
    path(
        'rest-auth/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/instagram/', InstagramLogin.as_view(), name='instagram_login'), # اگر نامگذاری اینطور باشد
    path('auth/twitter/', TwitterLogin.as_view(), name='twitter_login'), 
    path('auth/google/callback/', include('allauth.urls')),  
]
