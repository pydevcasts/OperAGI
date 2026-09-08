from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from social_accounts.models import UserSocialAccount

from .models import AnalyticsSnapshot, GeneratedContent, Post, Schedule
from .serializers import AnalyticsSnapshotSerializer, GeneratedContentSerializer, PostSerializer, ScheduleSerializer
from .tasks import enqueue, generate_post_content, publish_scheduled_post


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Post.objects.none()
        queryset = Post.objects.filter(user=self.request.user).select_related(
            'social_account', 'social_account__social_account', 'generated_content'
        )
        if self.request.query_params.get('platform'):
            queryset = queryset.filter(platform=self.request.query_params['platform'])
        if self.request.query_params.get('status'):
            queryset = queryset.filter(status=self.request.query_params['status'])
        return queryset

    @action(detail=True, methods=('post',), url_path='generate')
    def generate(self, request, pk=None):
        post = self.get_object()
        if post.status == Post.Status.GENERATING:
            return Response({'detail': 'Generation is already in progress.'}, status=status.HTTP_409_CONFLICT)
        task_id, synchronous = enqueue(generate_post_content, post.pk)
        post.refresh_from_db()
        return Response(
            {'task_id': task_id, 'synchronous': synchronous, 'post': self.get_serializer(post).data},
            status=status.HTTP_200_OK if synchronous else status.HTTP_202_ACCEPTED,
        )

    @action(detail=True, methods=('post',), url_path='generate_content')
    def generate_content_legacy(self, request, pk=None):
        post = self.get_object()
        if request.data.get('generated_text'):
            serializer = GeneratedContentSerializer(data=request.data, context={'request': request, 'post_id': post.pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            post.status = Post.Status.GENERATED
            post.save(update_fields=('status', 'updated_at'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return self.generate(request, pk=pk)

    @action(detail=True, methods=('post',), url_path='publish')
    def publish(self, request, pk=None):
        post = self.get_object()
        schedule, _ = Schedule.objects.update_or_create(
            post=post, defaults={'scheduled_for': timezone.now(), 'timezone': 'UTC', 'status': Schedule.Status.QUEUED}
        )
        try:
            publish_scheduled_post(schedule.pk)
        except RuntimeError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        post.refresh_from_db()
        return Response(self.get_serializer(post).data)


class GeneratedContentViewSet(viewsets.ModelViewSet):
    serializer_class = GeneratedContentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return GeneratedContent.objects.none()
        return GeneratedContent.objects.filter(post__user=self.request.user).select_related('post')

    def create(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        if post_id and GeneratedContent.objects.filter(post_id=post_id, post__user=request.user).exists():
            return Response(
                {'error': 'Generated content already exists for this post'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.post.status = Post.Status.GENERATED
        instance.post.save(update_fields=('status', 'updated_at'))
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return Schedule.objects.none()
        queryset = Schedule.objects.filter(post__user=self.request.user).select_related(
            'post', 'post__generated_content', 'post__social_account', 'post__social_account__social_account'
        )
        if self.request.query_params.get('start'):
            queryset = queryset.filter(scheduled_for__gte=self.request.query_params['start'])
        if self.request.query_params.get('end'):
            queryset = queryset.filter(scheduled_for__lte=self.request.query_params['end'])
        return queryset

    def perform_create(self, serializer):
        schedule = serializer.save(status=Schedule.Status.QUEUED)
        schedule.post.status = Post.Status.SCHEDULED
        schedule.post.save(update_fields=('status', 'updated_at'))
        task_id, _ = enqueue(publish_scheduled_post, schedule.pk, eta=schedule.scheduled_for)
        schedule.task_id = task_id
        schedule.save(update_fields=('task_id', 'updated_at'))

    def perform_update(self, serializer):
        schedule = serializer.save(status=Schedule.Status.QUEUED, last_error='')
        task_id, _ = enqueue(publish_scheduled_post, schedule.pk, eta=schedule.scheduled_for)
        schedule.task_id = task_id
        schedule.save(update_fields=('task_id', 'updated_at'))

    @action(detail=True, methods=('post',))
    def cancel(self, request, pk=None):
        schedule = self.get_object()
        if schedule.status == Schedule.Status.PUBLISHED:
            return Response({'detail': 'Published schedules cannot be cancelled.'}, status=status.HTTP_409_CONFLICT)
        schedule.status = Schedule.Status.CANCELLED
        schedule.save(update_fields=('status', 'updated_at'))
        schedule.post.status = Post.Status.GENERATED if hasattr(schedule.post, 'generated_content') else Post.Status.DRAFT
        schedule.post.save(update_fields=('status', 'updated_at'))
        return Response(self.get_serializer(schedule).data)


class AnalyticsSnapshotViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyticsSnapshotSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False) or not self.request.user.is_authenticated:
            return AnalyticsSnapshot.objects.none()
        queryset = AnalyticsSnapshot.objects.filter(user=self.request.user)
        if self.request.query_params.get('platform'):
            queryset = queryset.filter(platform=self.request.query_params['platform'])
        return queryset


class DashboardView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        posts = Post.objects.filter(user=request.user)
        schedules = Schedule.objects.filter(post__user=request.user)
        snapshots = AnalyticsSnapshot.objects.filter(user=request.user)
        totals = snapshots.aggregate(
            impressions=Coalesce(Sum('impressions'), 0), reach=Coalesce(Sum('reach'), 0),
            likes=Coalesce(Sum('likes'), 0), comments=Coalesce(Sum('comments'), 0),
            shares=Coalesce(Sum('shares'), 0), clicks=Coalesce(Sum('clicks'), 0), views=Coalesce(Sum('views'), 0),
        )
        return Response({
            'summary': {
                'connected_accounts': UserSocialAccount.objects.filter(user=request.user, is_active=True).count(),
                'posts_total': posts.count(),
                'posts_generated': posts.filter(status=Post.Status.GENERATED).count(),
                'posts_scheduled': posts.filter(status=Post.Status.SCHEDULED).count(),
                'posts_published': posts.filter(status=Post.Status.PUBLISHED).count(),
                'upcoming_schedules': schedules.filter(status=Schedule.Status.QUEUED, scheduled_for__gte=timezone.now()).count(),
            },
            'analytics': totals,
            'platforms': list(posts.values('platform').annotate(posts=Count('id')).order_by('platform')),
            'recent_posts': PostSerializer(posts[:5], many=True, context={'request': request}).data,
            'upcoming': ScheduleSerializer(
                schedules.filter(status=Schedule.Status.QUEUED, scheduled_for__gte=timezone.now())[:5],
                many=True, context={'request': request},
            ).data,
        })
