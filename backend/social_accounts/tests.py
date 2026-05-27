from django.urls import reverse
from rest_framework import status
from .models import UserSocialAccount
from rest_framework.test import APIClient
from allauth.socialaccount.models import SocialAccount, SocialToken
from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()


class SocialAccountTests(TestCase):
    """
    Tests for SocialAccount and UserSocialAccount models and API endpoints.
    """
    def setUp(self):
        """
        Set up two users and their initial social accounts for testing.
        """
        self.user1 = User.objects.create_user(email="user1@gmail.com", password="password1")
        self.user2 = User.objects.create_user(email="user2@gmail.com", password="password2")

        # Initial SocialAccount for user1 (Instagram)
        self.social_account_user1_insta = SocialAccount.objects.create(
            user=self.user1,
            provider='instagram',
            uid='insta-uid-user1',
            extra_data={'username': 'user1_insta_existing', 'access_token': 'abc123'}
        )
        # Associated Token and UserSocialAccount
        SocialToken.objects.create(
            account=self.social_account_user1_insta,
            token='abc123_token'
        )
        UserSocialAccount.objects.create(
            user=self.user1,
            social_account=self.social_account_user1_insta
        )

        # Initial SocialAccount for user2 (Twitter)
        self.social_account_user2_twitter = SocialAccount.objects.create(
            user=self.user2,
            provider='twitter',
            uid='twitter-uid-user2',
            extra_data={'username': 'user2_twitter_existing'}
        )
        # Associated Token and UserSocialAccount
        SocialToken.objects.create(
            account=self.social_account_user2_twitter,
            token='xyz789_token'
        )
        UserSocialAccount.objects.create(
            user=self.user2,
            social_account=self.social_account_user2_twitter
        )
        # Initialize API client and authenticate user1 for most tests
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        # For tests that need user2's context, authenticate user2
        self.client_user2 = APIClient()
        self.client_user2.force_authenticate(user=self.user2)
        print(f"\n--- Initial SocialAccount count in setUp: {SocialAccount.objects.count()} ---")
        for account in SocialAccount.objects.all():
            print(f" - Initial: ID={account.id}, User={account.user.email}, Provider={account.provider}, UID={account.uid}")
        print("-----------------------------------------------------\n")

    def test_create_social_account_instagram_for_user1(self):
        """
        Test creating a NEW Instagram social account for user1.
        Expects: 2 initial + 1 new = 3 SocialAccounts.
        """
        print("\n--- Running test_create_social_account_instagram_for_user1 ---")
        initial_count = SocialAccount.objects.count() # Should be 2

        data = {
            'social_account': {
                'provider': 'instagram',
                'uid': 'new-insta-uid-user1', # A UID that does not exist yet
                'extra_data': {'username': 'new_instagram_user1', 'access_token': 'xyz456'}
            }
        }
        # Assuming 'user-social-accounts-list' is the correct URL name for POST
        response = self.client.post(reverse('user-social-accounts-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify count: Initial 2 + 1 new = 3
        expected_count = initial_count + 1
        actual_count = SocialAccount.objects.count()
        print(f"Expected SocialAccount count: {expected_count}, Actual count: {actual_count}")
        self.assertEqual(actual_count, expected_count)
        # Verify details of the created account
        created_account = SocialAccount.objects.get(uid='new-insta-uid-user1')
        self.assertEqual(created_account.extra_data['username'], 'new_instagram_user1')
        self.assertEqual(created_account.user, self.user1)
        print("--- Finished test_create_social_account_instagram_for_user1 ---")

    def test_create_social_account_twitter_for_user2(self):
        """
        Test creating a NEW Twitter social account for user2.
        Expects: 2 initial + 1 new = 3 SocialAccounts.
        """
        print("\n--- Running test_create_social_account_twitter_for_user2 ---")
        initial_count = SocialAccount.objects.count() # Should be 2 (or 3 if previous test ran)
        data = {
            'social_account': {
                'provider': 'twitter',
                'uid': 'new-twitter-uid-user2', # A UID that does not exist yet
                'extra_data': {'username': 'new_twitter_user2'}
            }
        }
        # Use client authenticated as user2 for this operation
        response = self.client_user2.post(reverse('user-social-accounts-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # then after creating one new one, the count should be 3.
        expected_count_after_this_test = initial_count + 1 
        print(f"Expected SocialAccount count after this test: {expected_count_after_this_test}, Actual count: {SocialAccount.objects.count()}")
        # Re-evaluate the assertion: If setUp creates 2, and this test adds 1, count should be 3.
        self.assertEqual(SocialAccount.objects.count(), 3) 
        # Verify details of the created account
        created_account = SocialAccount.objects.get(uid='new-twitter-uid-user2')
        self.assertEqual(created_account.extra_data['username'], 'new_twitter_user2')
        self.assertEqual(created_account.user, self.user2)
        print("--- Finished test_create_social_account_twitter_for_user2 ---")

    def test_create_social_account_instagram_duplicate_uid_for_user1(self):
        """
        Test creating an Instagram social account for user1 with an EXISTING UID.
        Expects: No new SocialAccount should be created. Count remains 2 (from setUp).
        """
        print("\n--- Running test_create_social_account_instagram_duplicate_uid_for_user1 ---")
        initial_count = SocialAccount.objects.count() # Should be 2

        data = {
            'social_account': {
                'provider': 'instagram',
                'uid': 'insta-uid-user1', # This UID already exists for user1
                'extra_data': {'username': 'another_instagram_user1', 'access_token': 'def789'}
            }
        }
        
        response = self.client.post(reverse('user-social-accounts-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # Should still succeed if it links to existing
        
    def test_list_social_accounts_for_user1(self):
        """
        Test retrieving social accounts associated ONLY with the authenticated user (user1).
        """
        print("\n--- Running test_list_social_accounts_for_user1 ---")
        response = self.client.get(reverse('user-social-accounts-list'), format='json')
        accounts = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User1 has one Instagram account created in setUp.
        self.assertEqual(len(accounts), 1) 
        self.assertEqual(accounts[0]["social_account"]['provider'], 'instagram')
        self.assertEqual(accounts[0]["social_account"]['uid'], 'insta-uid-user1')
        print("--- Finished test_list_social_accounts_for_user1 ---")


    def test_list_social_accounts_for_user2(self):
        """
        Test retrieving social accounts associated ONLY with user2.
        """
        print("\n--- Running test_list_social_accounts_for_user2 ---")
        response = self.client_user2.get(reverse('user-social-accounts-list'), format='json')
        accounts = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User2 has one Twitter account created in setUp.
        self.assertEqual(len(accounts), 1) 
        self.assertEqual(accounts[0]["social_account"]['provider'], 'twitter')
        self.assertEqual(accounts[0]["social_account"]['uid'], 'twitter-uid-user2')
        print("--- Finished test_list_social_accounts_for_user2 ---")


    def test_delete_social_account(self):
        """Test deleting a social account."""
        response = self.client.delete(reverse('user-social-accounts-detail', kwargs={'pk': self.social_account_user1_insta.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SocialAccount.objects.count(), 2)  # one account should be left
