# signals.py
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added, social_account_updated
from social_accounts.models import UserSocialAccount


@receiver([social_account_added, social_account_updated])
def sync_user_social_account(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    social_account = sociallogin.account

    UserSocialAccount.objects.get_or_create(user=user, social_account=social_account)
