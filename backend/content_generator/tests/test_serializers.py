# backend/content_generator/tests/test_serializers.py
from .base import BaseTest
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ValidationError
from ..serializers import PostSerializer, GeneratedContentSerializer
from ..models import Post, GeneratedContent

class PostSerializerTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.request = self.factory.post("/content_generator/generate-posts/")
        self.request.user = self.user
        self.context = {"request": self.request}
    
    def test_create_post_success(self):
        data = {
            "social_account_id": self.user_social_account.id,
            "platform": "instagram",
            "content": "Test post content",
            "visual_idea": "Creative visual idea"
        }

        serializer = PostSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        post = serializer.save()
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.social_account, self.user_social_account)
        self.assertEqual(post.platform, "instagram")
        self.assertEqual(post.content, "Test post content")
    
    def test_validate_social_account_id_wrong_user(self):
        data = {
            "social_account_id": self.other_user_social_account.id,  # Wrong user's account
            "platform": "twitter",
            "content": "Another test",
            "visual_idea": "Different idea"
        }
        serializer = PostSerializer(data=data, context=self.context)
        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)
        self.assertIn("Social account does not belong to the current user.", str(ctx.exception))

    def test_update_post_success(self):
        post = Post.objects.create(
            user=self.user,
            social_account=self.user_social_account,
            platform="instagram",
            content="Old content",
            visual_idea="Old idea"
        )

        update_data = {
            "content": "Updated content",
            "visual_idea": "Updated visual"
        }

        serializer = PostSerializer(post, data=update_data, context=self.context, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_post = serializer.save()

        self.assertEqual(updated_post.content, "Updated content")
        self.assertEqual(updated_post.visual_idea, "Updated visual")

# tests/test_serializers.py
class GeneratedContentSerializerTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.request = self.factory.post("/content_generator/generated-content/")
        self.request.user = self.user # کاربر احراز هویت شده
        self.context = {"request": self.request}

    def test_create_generated_content_success(self):
        self.assertFalse(hasattr(self.post, 'generated_content'))  # ✅ این بار پاس می‌شود
       
        data = {
            "content_type": "text_and_hashtags",
            "generated_text": "This is a new generated caption.",
            "suggested_hashtags": "#new #content",
            # 'suggested_publish_time': '2023-10-27T10:00:00Z', # optional
            # 'avatar_video_url': 'http://example.com/video.mp4', # optional
            # 'audio_file_path': '/path/to/audio.mp3', # optional
        }
        self.request.data = {'post_id': self.post.id}
        self.request.data.update(data) # ترکیب داده‌های اصلی با post_id
        serializer = GeneratedContentSerializer(data=self.request.data, context=self.context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        generated_content = serializer.save()
        self.assertIsNotNone(generated_content.id)
        self.assertEqual(generated_content.post.id, self.post.id)
        self.assertEqual(generated_content.content_type, "text_and_hashtags")
        self.assertEqual(generated_content.generated_text, "This is a new generated caption.")
        self.assertEqual(generated_content.suggested_hashtags, "#new #content")
        self.assertIsNotNone(generated_content.generated_at)
        self.post.refresh_from_db()
        # # اطمینان از اینکه حالا پست ما محتوای تولید شده دارد
        self.assertTrue(hasattr(self.post, 'generated_content'))
        self.assertEqual(self.post.generated_content, generated_content)

    def test_create_generated_content_already_exists(self):
        GeneratedContent.objects.create(
            post=self.post,
            content_type="text_and_hashtags",
            generated_text="Existing generated caption",
            suggested_hashtags="#exists #already",
        )
        self.post.refresh_from_db()
        self.assertTrue(hasattr(self.post, 'generated_content'))  
        data = {
            'post_id': self.post.id,
            "content_type": "text",
            "generated_text": "Another try",
            "suggested_hashtags": "#new #try"
        }
        self.request.data = {'post_id': self.post.id}
        self.request.data.update(data)
        serializer = GeneratedContentSerializer(data=self.request.data, context=self.context)
        self.assertTrue(serializer.is_valid(), serializer.errors) 
        with self.assertRaises(ValidationError):
            serializer.save()


    def test_create_generated_content_post_does_not_exist(self):
        non_existent_post_id = 99999  
        data = {
            "post_id": non_existent_post_id,
            "content_type": "text",
            "generated_text": "Trying with fake post",
        }
        self.request.data = data
        serializer = GeneratedContentSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidationError) as cm:
                serializer.save()
        self.assertEqual(cm.exception.detail, ["Post does not exist."])


    def test_generated_content_fields_read_only(self):
        generated_content = GeneratedContent.objects.create(
            post=self.post,
            content_type="text",
            generated_text="Initial text",
            generated_at=None # اجازه می‌دهیم در create تنظیم شود
        )
        
        # داده‌های آپدیت که شامل فیلدهای read_only است
        update_data = {
            "post": 123,  # post باید read-only باشد
            "generated_at": "2023-01-01T00:00:00Z", # generated_at هم باید read-only باشد
            "generated_text": "Updated text", # این فیلد قابل تغییر است
            "content_type": "image_description", # این فیلد هم قابل تغییر است
        }
        serializer = GeneratedContentSerializer(generated_content, data=update_data, partial=True, context=self.context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_instance = serializer.save()
    #     # اطمینان از اینکه فیلدهای read_only تغییر نکرده‌اند
        self.assertEqual(updated_instance.post.id, self.post.id) # باید همان پست قبلی باشد
        self.assertIsNotNone(updated_instance.generated_at) # باید تاریخ اولیه خودش را داشته باشد یا تنظیم شده باشد
    #     # اطمینان از اینکه فیلدهای قابل تغییر، آپدیت شده‌اند
        self.assertEqual(updated_instance.generated_text, "Updated text")
        self.assertEqual(updated_instance.content_type, "image_description")
