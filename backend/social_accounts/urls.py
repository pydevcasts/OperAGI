# backend\social_accounts\urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserSocialAccountViewSet 

router = DefaultRouter()
router.register(r'user-social-accounts', UserSocialAccountViewSet, basename='user-social-accounts')

urlpatterns = [
    path('', include(router.urls)), 
]
urlpatterns = router.urls