from datetime import timedelta
from unittest.mock import patch

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from content_generator.models import AnalyticsSnapshot, Post, Schedule
from content_generator.services import generate_content
from social_accounts.models import UserSocialAccount

User = get_user_model()


class PhaseOneTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='phase1@example.com', password='strong-password')
        self.other = User.objects.create_user(email='other@example.com', password='strong-password')
        social = SocialAccount.objects.create(user=self.user, provider='instagram', uid='phase1-ig')
        self.connection = UserSocialAccount.objects.create(user=self.user, social_account=social)
        self.client.force_authenticate(self.user)

    def test_local_generator_is_deterministic_and_bilingual(self):
        first = generate_content(idea='launch a creator course', platform='instagram', language='en')
        second = generate_content(idea='launch a creator course', platform='instagram', language='en')
        persian = generate_content(idea='راه اندازی دوره تولید محتوا', platform='youtube', language='fa')
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(first.provider, 'local')
        self.assertTrue(persian.title)
        self.assertTrue(persian.hashtags)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_create_and_generate_post(self):
        response = self.client.post(reverse('posts-list'), {
            'social_account_id': self.connection.pk,
            'platform': 'instagram', 'language': 'fa', 'tone': 'friendly',
            'content': 'معرفی ابزار برنامه ریزی محتوا',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        generated = self.client.post(reverse('posts-generate', args=[response.data['id']]), {}, format='json')
        self.assertEqual(generated.status_code, status.HTTP_200_OK)
        post = Post.objects.get(pk=response.data['id'])
        self.assertEqual(post.status, Post.Status.GENERATED)
        self.assertEqual(post.generated_content.provider, 'local')

    @patch('content_generator.views.enqueue', return_value=('local-pending', True))
    def test_future_schedule_uses_safe_pending_fallback(self, _enqueue):
        post = Post.objects.create(user=self.user, social_account=self.connection, platform='instagram', content='idea')
        response = self.client.post(reverse('schedules-list'), {
            'post_id': post.pk,
            'scheduled_for': (timezone.now() + timedelta(days=1)).isoformat(),
            'timezone': 'Asia/Tehran',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], Schedule.Status.QUEUED)
        post.refresh_from_db()
        self.assertEqual(post.status, Post.Status.SCHEDULED)

    def test_dashboard_and_analytics_are_user_scoped(self):
        post = Post.objects.create(user=self.user, platform='youtube', content='idea')
        AnalyticsSnapshot.objects.create(user=self.user, post=post, platform='youtube', reach=100, likes=10, comments=2)
        other_post = Post.objects.create(user=self.other, platform='twitter', content='private')
        AnalyticsSnapshot.objects.create(user=self.other, post=other_post, platform='twitter', reach=999, likes=999)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['analytics']['reach'], 100)
        self.assertEqual(response.data['summary']['posts_total'], 1)

    def test_cannot_use_another_users_social_account(self):
        social = SocialAccount.objects.create(user=self.other, provider='instagram', uid='other-ig')
        connection = UserSocialAccount.objects.create(user=self.other, social_account=social)
        response = self.client.post(reverse('posts-list'), {
            'social_account_id': connection.pk, 'platform': 'instagram', 'content': 'no access'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
