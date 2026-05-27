from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Post, GeneratedContent
from .serializers import PostSerializer, GeneratedContentSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Post.objects.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            return Post.objects.none()

        return Post.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        post = self.get_object()

        if post.status in ['content_generated', 'ready_to_publish', 'draft']:
            post.status = 'published'
            post.save(update_fields=['status'])
            return Response({'status': 'post published successfully'})

        return Response(
            {'error': 'Post is not in a publishable status'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'], url_path='generate_content')
    def generate_content(self, request, pk=None):
        post = self.get_object()

        if hasattr(post, 'generated_content'):
            return Response(
                {'error': 'Generated content already exists for this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = GeneratedContentSerializer(
            data=request.data,
            context={'request': request, 'post_id': post.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        post.status = 'content_generated'
        post.save(update_fields=['status'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# views.py
class GeneratedContentViewSet(viewsets.ModelViewSet):
    serializer_class = GeneratedContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return GeneratedContent.objects.none()

        user = self.request.user
        if not user or not user.is_authenticated:
            return GeneratedContent.objects.none()
        return GeneratedContent.objects.filter(post__user=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        post_id = request.data.get('post_id')
        
        if not post_id:
            return Response(
                {"error": "post_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            post = Post.objects.get(id=post_id, user=user)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found or you don't have permission"},
                status=status.HTTP_404_NOT_FOUND
            )

        if hasattr(post, 'generated_content'):
            return Response(
                {"error": "Generated content already exists for this post"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # اضافه کردن post به داده‌های serializer
        data = request.data.copy()
        data['post'] = post.id
        data['content_type'] = 'text_and_hashtags'  # مقدار پیش‌فرض

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # بروزرسانی وضعیت پست
        post.status = 'content_generated'
        post.save(update_fields=['status'])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)