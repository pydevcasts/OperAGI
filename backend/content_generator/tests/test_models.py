# backend/content_generator/tests/test_models.py
from content_generator.models import GeneratedContent
from .base import BaseTest

class PostModelTests(BaseTest):
    def test_post_creation(self):
        self.assertEqual(self.post.user.email, "test@example.com")
        self.assertEqual(self.post.social_account, self.user_social_account)
        self.assertEqual(self.post.platform, 'instagram')
        self.assertEqual(self.post.content, 'Test post content')
        self.assertEqual(self.post.visual_idea, 'Visual idea here')
        self.assertEqual(self.post.status, 'draft')  # assuming default='draft'


class GeneratedContentModelTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.generated_content = GeneratedContent.objects.create(
            post=self.post,
            content_type="text_and_hashtags",
            generated_text="This is generated caption text.",
            suggested_hashtags="#test #django",
        )
    def test_generated_content_creation(self):
        self.assertEqual(self.generated_content.post, self.post)
        self.assertEqual(self.generated_content.content_type, "text_and_hashtags")
        self.assertEqual(self.generated_content.generated_text, "This is generated caption text.")
        self.assertEqual(self.generated_content.suggested_hashtags, "#test #django")
        self.assertIsNotNone(self.generated_content.generated_at)

    def test_generated_content_str(self):
        expected_str = f"Generated content for Post ID: {self.post.id}"
        self.assertEqual(str(self.generated_content), expected_str)
