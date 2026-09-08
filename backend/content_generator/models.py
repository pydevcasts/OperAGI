from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from social_accounts.models import UserSocialAccount


class Post(models.Model):
    class Platform(models.TextChoices):
        INSTAGRAM = 'instagram', 'Instagram'
        TWITTER = 'twitter', 'Twitter/X'
        YOUTUBE = 'youtube', 'YouTube'

    class Language(models.TextChoices):
        ENGLISH = 'en', 'English'
        PERSIAN = 'fa', 'Persian'

    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        GENERATING = 'generating_content', _('Generating Content')
        GENERATED = 'content_generated', _('Content Generated')
        READY = 'ready_to_publish', _('Ready to Publish')
        SCHEDULED = 'scheduled', _('Scheduled')
        PUBLISHED = 'published', _('Published')
        FAILED = 'failed', _('Failed')

    STATUS_CHOICES = Status.choices
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    social_account = models.ForeignKey(
        UserSocialAccount, on_delete=models.SET_NULL, related_name='posts', blank=True, null=True
    )
    platform = models.CharField(_('Platform'), max_length=20, choices=Platform.choices)
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.ENGLISH)
    tone = models.CharField(max_length=50, default='professional')
    content = models.TextField(_('Initial Content Idea / Input'))
    visual_idea = models.TextField(_('Visual Idea / Prompt'), blank=True, default='')
    status = models.CharField(_('Status'), max_length=24, choices=Status.choices, default=Status.DRAFT)
    generation_error = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    published_at = models.DateTimeField(_('Published At'), blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = [models.Index(fields=('user', 'status')), models.Index(fields=('platform', 'created_at'))]

    def __str__(self):
        return f'{self.get_platform_display()} post by {self.user.email}'


class GeneratedContent(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('text_and_hashtags', 'Text and hashtags'),
        ('text', 'Text'),
        ('image_description', 'Image description'),
        ('caption', 'Caption'),
        ('thread', 'Thread'),
        ('youtube_metadata', 'YouTube metadata'),
    )
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='generated_content')
    content_type = models.CharField(
        _('Content Type'), max_length=100, choices=CONTENT_TYPE_CHOICES, default='text_and_hashtags'
    )
    generated_text = models.TextField(_('Generated Text / Caption'))
    title = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    suggested_hashtags = models.TextField(_('Suggested Hashtags'), blank=True, default='')
    hashtags = models.JSONField(default=list, blank=True)
    suggested_publish_time = models.DateTimeField(_('Suggested Publish Time'), blank=True, null=True)
    provider = models.CharField(max_length=40, default='local')
    provider_metadata = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(_('Generated At'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar_video_url = models.URLField(_('Avatar Video URL'), blank=True, null=True)
    audio_file_path = models.CharField(_('Audio File Path'), max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Generated content for Post ID: {self.post_id}'


class Schedule(models.Model):
    class Status(models.TextChoices):
        QUEUED = 'queued', 'Queued'
        PROCESSING = 'processing', 'Processing'
        PUBLISHED = 'published', 'Published'
        CANCELLED = 'cancelled', 'Cancelled'
        FAILED = 'failed', 'Failed'

    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='schedule')
    scheduled_for = models.DateTimeField(db_index=True)
    timezone = models.CharField(max_length=64, default='UTC')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.QUEUED, db_index=True)
    task_id = models.CharField(max_length=255, blank=True, default='')
    last_error = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('scheduled_for',)

    def __str__(self):
        return f'Post {self.post_id} at {self.scheduled_for.isoformat()}'

    @property
    def is_due(self):
        return self.scheduled_for <= timezone.now()


class AnalyticsSnapshot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analytics_snapshots')
    social_account = models.ForeignKey(
        UserSocialAccount, on_delete=models.SET_NULL, related_name='analytics_snapshots', null=True, blank=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='analytics_snapshots', null=True, blank=True)
    platform = models.CharField(max_length=20, choices=Post.Platform.choices)
    impressions = models.PositiveBigIntegerField(default=0)
    reach = models.PositiveBigIntegerField(default=0)
    likes = models.PositiveBigIntegerField(default=0)
    comments = models.PositiveBigIntegerField(default=0)
    shares = models.PositiveBigIntegerField(default=0)
    clicks = models.PositiveBigIntegerField(default=0)
    views = models.PositiveBigIntegerField(default=0)
    followers = models.PositiveBigIntegerField(default=0)
    captured_at = models.DateTimeField(default=timezone.now, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ('-captured_at',)
        indexes = [models.Index(fields=('user', 'platform', 'captured_at'))]

    @property
    def engagement_rate(self):
        denominator = self.reach or self.impressions
        if not denominator:
            return 0.0
        return round(((self.likes + self.comments + self.shares + self.clicks) / denominator) * 100, 2)

    def __str__(self):
        return f'{self.platform} analytics at {self.captured_at.isoformat()}'
