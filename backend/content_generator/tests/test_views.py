# backend/content_generator/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from .base import BaseTest
from ..models import GeneratedContent, Post # Import the model you are testing
from ..serializers import GeneratedContentSerializer # Import the serializer
# tests.py
class GenerateContentViewSetTests(BaseTest):

    def setUp(self):
        super().setUp()
        # مطمئن شوید که نام URL صحیح است
        self.generate_content_url = reverse('generatedcontent-list') 
        
        self.valid_data = {
            'post_id': self.post.id,
            'generated_text': 'This is a generated caption for testing.',
            'suggested_hashtags': '#test #generated #django',
            'content_type': 'text_and_hashtags'
        }

    def test_generate_content_success(self):
        """
        Test generating content for a post successfully.
        """
        self.assertIsNone(GeneratedContent.objects.filter(post=self.post).first())
        response = self.client.post(self.generate_content_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GeneratedContent.objects.filter(post=self.post).exists())
        self.post.refresh_from_db()
        self.assertEqual(self.post.status, 'content_generated')
        self.assertEqual(GeneratedContent.objects.count(), 1)
        generated_content = GeneratedContent.objects.get(post=self.post)
        self.assertEqual(generated_content.post, self.post) 
        self.assertIn('id', response.data)
        self.assertIn('post', response.data)
        self.assertIn('generated_at', response.data)  # فیلد read-only از Serializer
        self.assertEqual(response.data['post'], self.post.id)
    