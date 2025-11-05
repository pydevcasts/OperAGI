# accounts/tests/test_auth.py
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from unittest.mock import patch
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount

User = get_user_model()


class AuthenticationTestCase(TestCase):
    def setUp(self):
        """
        Set up test client and URLs for authentication endpoints.
        """
        self.client = APIClient()
        self.register_url = reverse('rest_register')           # /api/auth/registration/
        self.login_url = reverse('rest_login')                 # /api/auth/login/
        self.google_login_url = '/api/v1/auth/google/'         # Google OAuth endpoint

        # Test user data for registration
        self.user_data = {
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }

        # Clean up any existing social accounts to avoid conflicts
        SocialAccount.objects.all().delete()

    def test_register_user(self):
        """Test successful user registration via email and password."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_login_user(self):
        """Test successful login with email and password."""
        # First, register the user
        self.client.post(self.register_url, self.user_data, format='json')

        # Then attempt login
        login_data = {
            'email': 'test@example.com',
            'password': 'StrongPass123!'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    @patch('allauth.socialaccount.providers.google.views.GoogleOAuth2Adapter.complete_login')
    def test_google_login_invalid_token(self, mock_complete_login):
        """
        Test Google login with an invalid access token.
        Should return 400 Bad Request with error message.
        """
        # Simulate invalid token error from Google adapter
        mock_complete_login.side_effect = ValidationError(
            {"non_field_errors": ["Unable to log in with provided credentials."]}
        )

        # Send request with invalid token
        response = self.client.post(
            self.google_login_url,
            {'access_token': 'invalid-token'},
            format='json'
        )

        # Expect 400 response with validation error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)