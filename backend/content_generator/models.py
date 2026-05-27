#backend\content_generator\models.py
from django.db import models
from social_accounts.models import UserSocialAccount
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('generating_content', _('Generating Content')), # وضعیت جدید پیشنهادی
        ('content_generated', _('Content Generated')),   # وضعیت جدید پیشنهادی
        ('ready_to_publish', _('Ready to Publish')),     # وضعیت جدید پیشنهادی
        ('published', _('Published')),
        ('failed', _('Failed')), # برای مدیریت خطاها
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # فرض می‌کنیم مدل User وجود دارد
    social_account = models.ForeignKey(UserSocialAccount, on_delete=models.CASCADE, related_name='posts') # نام related_name را به صورت دلخواه تنظیم کنید
    platform = models.CharField(_('Platform'), max_length=50, choices=[('instagram', 'Instagram'), ('twitter', 'Twitter/X'), ('youtube', 'YouTube')], blank=True, null=True)
    content = models.TextField(_('Initial Content Idea / Input')) # ورودی اصلی کاربر، شامل ایده اولیه متن، تصویر یا ویدئو
    # فیلد جدید برای ایده بصری (تصویر/ویدئو) - با توجه به اینکه فاز ۱ شامل ایده بصری است
    visual_idea = models.TextField(_('Visual Idea / Prompt'), blank=True, null=True)
    # فیلدهای پیشنهادی قبلی
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    published_at = models.DateTimeField(_('Published At'), blank=True, null=True)

    def __str__(self):
        return f"Post for {self.platform} by {self.user.email} on  {self.social_account.social_account.provider}"


class GeneratedContent(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='generated_content')
    content_type = models.CharField(_('Content Type'), max_length=50, default='text_and_hashtags') # برای تفکیک فاز ۱ (متن و هشتگ) و فاز ۲ (ویدئو)
    generated_text = models.TextField(_('Generated Text / Caption')) # نام جدید برای caption_text
    suggested_hashtags = models.TextField(_('Suggested Hashtags'), blank=True, null=True)
    suggested_publish_time = models.DateTimeField(_('Suggested Publish Time'), blank=True, null=True)
    generated_at = models.DateTimeField(_('Generated At'), auto_now_add=True)
    # فیلدهایی که طبق مستندات مربوط به فاز ۲ هستند و فعلا خالی می‌مانند:
    avatar_video_url = models.URLField(_('Avatar Video URL'), blank=True, null=True)
    audio_file_path = models.CharField(_('Audio File Path'), max_length=255, blank=True, null=True)

 
    def __str__(self):
        return f"Generated content for Post ID: {self.post.id}"
