# backend/content_generator/tests/base.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from social_accounts.models import UserSocialAccount, SocialAccount
from ..models import Post

User = get_user_model()

class BaseTest(TestCase):
    def setUp(self):
        # Users
        self.user = User.objects.create_user(email="test@example.com", password="testpassword123")
        self.other_user = User.objects.create_user(email="other_user@gmail.com", password="password123")

        # Social Accounts
        self.social_account = SocialAccount.objects.create(
            user=self.user,
            provider="instagram",
            uid="9876543210"
        )
        self.other_social_account = SocialAccount.objects.create(
            user=self.other_user,
            provider="instagram",
            uid="2222"
        )

        # UserSocialAccounts
        self.user_social_account = UserSocialAccount.objects.create(
            user=self.user,
            social_account=self.social_account
        )
        self.other_user_social_account = UserSocialAccount.objects.create(
            user=self.other_user,
            social_account=self.other_social_account
        )

        # Post + Generated content
        self.post = Post.objects.create(
            user=self.user,
            social_account=self.user_social_account,
            platform="instagram",
            content="Test post content",
            visual_idea="Visual idea here"
        )

        # Auth client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
