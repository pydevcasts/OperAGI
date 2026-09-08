from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserSocialAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connected_social_accounts')
    social_account = models.OneToOneField(SocialAccount, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=255, blank=True, default='')
    external_url = models.URLField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    connected_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('social_account__provider', 'id')

    def __str__(self):
        return f'{self.user.email} - {self.social_account.provider} ({self.social_account.uid})'

    @property
    def provider(self):
        return self.social_account.provider

    @property
    def provider_data(self):
        return self.social_account.extra_data
