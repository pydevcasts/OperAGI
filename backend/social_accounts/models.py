from django.db import models
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSocialAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connected_social_accounts')
    social_account = models.OneToOneField(SocialAccount, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.user.username} - {self.social_account.provider} ({self.social_account.uid})"

    @property
    def provider_data(self):
        return self.social_account.extra_data
    