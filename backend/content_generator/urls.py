# backend/content_generator/urls.py
from .views import PostViewSet, GeneratedContentViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'generate-post', PostViewSet, basename='post')
router.register(r'generated-content', GeneratedContentViewSet, basename='generatedcontent')

urlpatterns = [
    path('', include(router.urls)),
]

