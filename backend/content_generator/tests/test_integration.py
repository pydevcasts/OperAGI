# backend/content_generator/tests/test_view_serializer_integration.py
from django.urls import reverse
from rest_framework import status
from ..models import GeneratedContent, Post
from .base import BaseTest

class GeneratedContentViewSerializerIntegrationTest(BaseTest):
    
    def setUp(self):
        super().setUp()
        self.list_url = reverse('generatedcontent-list')
        self.detail_url = reverse('generatedcontent-detail', kwargs={'pk': self.generated_content.id}) \
            if hasattr(self, 'generated_content') else None
    
    def test_create_generated_content_integration(self):
        """تست یکپارچگی کامل بین View و Serializer در ایجاد محتوای تولید شده"""
        # داده‌های ورودی
        data = {
            'post_id': self.post.id,
            'content_type': 'text_and_hashtags',
            'generated_text': 'این یک متن تستی است',
            'suggested_hashtags': '#تست #اینستاگرام',
            'suggested_publish_time': '2023-12-01T10:00:00Z',
            'avatar_video_url': 'https://example.com/video.mp4',
            'audio_file_path': '/path/to/audio.mp3'
        }
        # درخواست ایجاد از طریق View
        response = self.client.post(self.list_url, data, format='json')
        # بررسی پاسخ View
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # بررسی داده‌های برگشتی مطابق با Serializer
        self.assertIn('id', response.data)
        self.assertIn('post', response.data)
        self.assertIn('content_type', response.data)
        self.assertIn('generated_text', response.data)
        self.assertIn('generated_at', response.data)
        # بررسی اینکه post به صورت read-only برگردانده شده (مطابق Serializer)
        self.assertEqual(response.data['post'], self.post.id)
        generated_content = GeneratedContent.objects.get(id=response.data['id'])
        self.assertEqual(generated_content.generated_text, 'این یک متن تستی است')
        self.assertEqual(generated_content.post.id, self.post.id)
        self.post.refresh_from_db()
        self.assertEqual(self.post.status, 'content_generated')
    
    def test_validation_error_handling(self):
        """تست مدیریت خطاهای validation بین View و Serializer"""
        # داده‌های کاملاً نامعتبر
        invalid_data = {
            'post_id': self.post.id,
            'content_type': 'totally_invalid_type_that_does_not_exist_in_choices',
            'generated_text': ''  # متن خالی
        }
        
        response = self.client.post(self.list_url, invalid_data, format='json')
        # View باید خطای validation از Serializer را به درستی مدیریت کند
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # بررسی ساختار خطا
        print(f"Response data: {response.data}")  # برای دیباگ
        self.assertIsNotNone(response.data)
        # بررسی فیلدهای دارای خطا - ممکن است هر دو یا یکی خطا داشته باشند
        error_fields = response.data.keys() if isinstance(response.data, dict) else []
        if 'generated_text' in error_fields:
            self.assertIn('This field may not be blank', str(response.data['generated_text']))
        if 'content_type' in error_fields:
            self.assertIn('not a valid choice', str(response.data['content_type']))
        # حداقل یکی باید خطا داشته باشد
        self.assertTrue(len(error_fields) > 0, "Should have at least one validation error")
    
    def test_retrieve_uses_serializer_correctly(self):
        """تست نمایش داده با استفاده از Serializer در View"""
        # ایجاد یک GeneratedContent برای تست
        generated_content = GeneratedContent.objects.create(
            post=self.post,
            content_type='text_and_hashtags',
            generated_text='متن تستی برای بازیابی',
            suggested_hashtags='#تست #بازیابی'
        )
        
        detail_url = reverse('generatedcontent-detail', kwargs={'pk': generated_content.id})
        response = self.client.get(detail_url)
        # بررسی ساختار داده مطابق Serializer
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], generated_content.id)
        self.assertEqual(response.data['post'], self.post.id)  # post به صورت ID نمایش داده می‌شود
        self.assertEqual(response.data['generated_text'], 'متن تستی برای بازیابی')
        self.assertIn('generated_at', response.data)  # فیلد read-only وجود دارد
    
    def test_permissions_integration(self):
        """تست یکپارچگی permissions بین View و Serializer"""
        # ایجاد پست و محتوای تولید شده توسط کاربر دیگر
        other_post = Post.objects.create(
            user=self.other_user,
            social_account=self.other_user_social_account,
            platform="instagram",
            content="پست کاربر دیگر",
            visual_idea="ایده بصری"
        )
        other_generated_content = GeneratedContent.objects.create(
            post=other_post,
            content_type='text_and_hashtags',
            generated_text='متن کاربر دیگر'
        )
        
        # تلاش برای دسترسی به محتوای کاربر دیگر
        detail_url = reverse('generatedcontent-detail', kwargs={'pk': other_generated_content.id})
        response = self.client.get(detail_url)
        
        # View باید بر اساس get_queryset دسترسی را محدود کند
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_duplicate_content_prevention(self):
        """تست جلوگیری از ایجاد محتوای تکراری (یکپارچگی View-Serializer)"""
        # ایجاد اولین محتوا
        data = {
            'post_id': self.post.id,
            'content_type': 'text_and_hashtags',
            'generated_text': 'متن اول'
        }
        response1 = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # تلاش برای ایجاد محتوای دوم برای همان پست
        response2 = self.client.post(self.list_url, data, format='json')
        
        # View و Serializer باید با همکاری هم از ایجاد تکراری جلوگیری کنند
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response2.data)
        self.assertEqual(response2.data['error'], 'Generated content already exists for this post')