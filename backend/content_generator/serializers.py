from rest_framework import serializers

from social_accounts.models import UserSocialAccount
from social_accounts.serializers import UserSocialAccountSerializer

from .models import AnalyticsSnapshot, GeneratedContent, Post, Schedule


class GeneratedContentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GeneratedContent
        fields = (
            'id', 'post', 'content_type', 'generated_text', 'title', 'description',
            'suggested_hashtags', 'hashtags', 'suggested_publish_time', 'provider',
            'provider_metadata', 'generated_at', 'updated_at', 'avatar_video_url', 'audio_file_path',
        )
        read_only_fields = ('post', 'provider', 'provider_metadata', 'generated_at', 'updated_at')

    def create(self, validated_data):
        request = self.context['request']
        post_id = request.data.get('post_id') or self.context.get('post_id')
        try:
            post = Post.objects.get(pk=post_id, user=request.user)
        except Post.DoesNotExist as exc:
            raise serializers.ValidationError(['Post does not exist.']) from exc
        if hasattr(post, 'generated_content'):
            raise serializers.ValidationError({'post_id': 'Generated content already exists for this post.'})
        return GeneratedContent.objects.create(post=post, **validated_data)


class PostSerializer(serializers.ModelSerializer):
    social_account_id = serializers.PrimaryKeyRelatedField(
        source='social_account', queryset=UserSocialAccount.objects.all(), write_only=True,
        required=False, allow_null=True
    )
    user = serializers.StringRelatedField(read_only=True)
    social_account = UserSocialAccountSerializer(read_only=True)
    generated_content = GeneratedContentSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'social_account', 'social_account_id', 'platform', 'language', 'tone',
            'content', 'visual_idea', 'status', 'generation_error', 'generated_content',
            'created_at', 'updated_at', 'published_at',
        )
        read_only_fields = ('user', 'status', 'generation_error', 'created_at', 'updated_at', 'published_at')

    def validate_social_account_id(self, value):
        request = self.context.get('request')
        if value and request and value.user_id != request.user.id:
            raise serializers.ValidationError('Social account does not belong to the current user.')
        return value

    def validate(self, attrs):
        account = attrs.get('social_account')
        platform = attrs.get('platform', getattr(self.instance, 'platform', None))
        if account and account.provider != platform:
            raise serializers.ValidationError({'social_account_id': 'Connected account platform does not match the post.'})
        return attrs

    def create(self, validated_data):
        return Post.objects.create(user=self.context['request'].user, **validated_data)


class ScheduleSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post', queryset=Post.objects.all(), write_only=True)
    is_due = serializers.BooleanField(read_only=True)

    class Meta:
        model = Schedule
        fields = (
            'id', 'post', 'post_id', 'scheduled_for', 'timezone', 'status', 'task_id',
            'last_error', 'is_due', 'created_at', 'updated_at', 'processed_at',
        )
        read_only_fields = ('status', 'task_id', 'last_error', 'created_at', 'updated_at', 'processed_at')

    def validate_post_id(self, post):
        if post.user_id != self.context['request'].user.id:
            raise serializers.ValidationError('Post does not belong to the current user.')
        return post

    def validate(self, attrs):
        post = attrs.get('post', getattr(self.instance, 'post', None))
        if post and post.status == Post.Status.PUBLISHED:
            raise serializers.ValidationError({'post_id': 'Published posts cannot be scheduled again.'})
        return attrs


class AnalyticsSnapshotSerializer(serializers.ModelSerializer):
    engagement_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = AnalyticsSnapshot
        fields = (
            'id', 'social_account', 'post', 'platform', 'impressions', 'reach', 'likes',
            'comments', 'shares', 'clicks', 'views', 'followers', 'engagement_rate',
            'captured_at', 'metadata',
        )
        read_only_fields = ('id', 'engagement_rate')

    def validate_social_account(self, account):
        if account and account.user_id != self.context['request'].user.id:
            raise serializers.ValidationError('Social account does not belong to the current user.')
        return account

    def validate_post(self, post):
        if post and post.user_id != self.context['request'].user.id:
            raise serializers.ValidationError('Post does not belong to the current user.')
        return post

    def create(self, validated_data):
        return AnalyticsSnapshot.objects.create(user=self.context['request'].user, **validated_data)
