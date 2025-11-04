from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi

from dj_rest_auth.views import PasswordResetConfirmView
from accounts.views import GoogleLogin

schema_view = get_schema_view(
    openapi.Info(
        title="Speech Recognition API",
        default_version='v1',
        description="API documentation for Speech Recognition project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@speechrecognition.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.v1.urls')),

    
    # path('auth/', include('drf_social_oauth2.urls', namespace='drf')),

    # REST Auth (شامل POST /password/reset/confirm/)
    path('api/v1/rest-auth/', include('dj_rest_auth.urls')),

    # Registration
    path('api/v1/rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # Override: JSON API for password reset confirm
    path(
        'api/v1/rest-auth/password/reset/confirm/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm_json'
    ),

    # Standard URL for email link
    path(
        'api/v1/rest-auth/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('api/v1/auth/google/', GoogleLogin.as_view(), name='google_login'),

    # مهم: callback باید وجود داشته باشه
    path('api/v1/auth/google/callback/', include('allauth.urls')),  # یا dj_rest_auth
    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




