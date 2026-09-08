from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AnalyticsSnapshotViewSet, DashboardView, GeneratedContentViewSet, PostViewSet, ScheduleViewSet


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('generate-post', PostViewSet, basename='post')
router.register('generated-content', GeneratedContentViewSet, basename='generatedcontent')
router.register('schedules', ScheduleViewSet, basename='schedules')
router.register('analytics', AnalyticsSnapshotViewSet, basename='analytics')

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include(router.urls)),
]
