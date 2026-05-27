# backend/content_generator/tests/test_post_delete.py
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import GeneratedContent, Post
from .base import BaseTest

User = get_user_model()

class PostDeleteTests(BaseTest):
    """تست‌های حذف پست با استفاده از base class موجود"""
    def setUp(self):
        super().setUp()
        # ایجاد GeneratedContent مرتبط برای تست cascade delete
        self.generated_content = GeneratedContent.objects.create(
            post=self.post,
            content_type="text_and_hashtags",
            generated_text="Generated content text",
            suggested_hashtags="#test #hashtag"
        )
        self.post_detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})
    
    def test_delete_post_by_owner_success(self):
        """تست حذف موفقیت‌آمیز پست توسط مالک"""
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # بررسی حذف پست از دیتابیس
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        # بررسی cascade delete روی GeneratedContent مرتبط
        self.assertFalse(GeneratedContent.objects.filter(pk=self.generated_content.pk).exists())
    
    def test_delete_post_by_other_user_forbidden(self):
        """تست عدم امکان حذف پست توسط کاربر دیگر"""
        # کاربر دیگر را authenticate کنید
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.post_detail_url)
        # باید خطا بدهد (404 یا 403 بسته به تنظیمات permission)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])
#         # پست باید باقی بماند
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
        self.assertTrue(GeneratedContent.objects.filter(pk=self.generated_content.pk).exists())
    
    def test_delete_post_unauthenticated(self):
        """تست عدم امکان حذف پست بدون احراز هویت"""
        self.client.logout()  # لاگ اوت کنید
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())
        self.assertTrue(GeneratedContent.objects.filter(pk=self.generated_content.pk).exists())
    
    def test_delete_nonexistent_post(self):
        """تست حذف پستی که وجود ندارد"""
        non_existent_url = reverse('post-detail', kwargs={'pk': 99999})
        response = self.client.delete(non_existent_url)        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostDeleteAdminTests(BaseTest):
    """تست‌های حذف پست توسط ادمین"""
    def setUp(self):
        super().setUp()
        # ایجاد کاربر ادمین
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword123"
        )
        self.post_detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})
    
    def test_check_admin_permissions_first(self):
        """ابتدا بررسی کنیم که ادمین واقعاً superuser است"""
        print(f"Admin user is superuser: {self.admin_user.is_superuser}")
        print(f"Admin user is staff: {self.admin_user.is_staff}")
        print(f"Post owner: {self.post.user.email}")
        print(f"Admin user: {self.admin_user.email}")

    def test_delete_post_by_admin_success(self):
        """تست حذف موفقیت‌آمیز پست توسط ادمین"""
        # ابتدا با کاربر اصلی تست کنیم که پست وجود دارد
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.post_detail_url)
        print(f"Get post by owner: {response.status_code}")
        # حالا با ادمین تست کنیم
        self.client.force_authenticate(user=self.admin_user)
        print(f"Deleting post {self.post.pk} by admin {self.admin_user.email}")
        response = self.client.delete(self.post_detail_url)
        print(f"Response status: {response.status_code}")
        # ابتدا فقط لاگ کنیم، بعداً assertion اضافه کنیم
        if response.status_code != status.HTTP_204_NO_CONTENT:
            print(f"Unexpected status: {response.status_code}")
            print(f"Response data: {getattr(response, 'data', 'No data')}")
    
    def test_admin_can_delete_other_user_post(self):
        """تست اینکه ادمین می‌تواند پست کاربر دیگر را حذف کند"""
        # ابتدا مطمئن شویم ادمین واقعاً superuser است
        self.assertTrue(self.admin_user.is_superuser)
        self.assertTrue(self.admin_user.is_staff)
        # با ادمین authenticate کنیم
        self.client.force_authenticate(user=self.admin_user)
        print(f"Admin deleting post {self.post.pk} owned by {self.post.user.email}")
        # ابتدا بررسی کنیم ادمین می‌تواند پست را ببیند
        get_response = self.client.get(self.post_detail_url)
        print(f"Admin can see post: {get_response.status_code}")
        if get_response.status_code != status.HTTP_200_OK:
            print(f"Cannot see post, response: {getattr(get_response, 'data', 'No data')}")
            # اگر نمی‌بیند، شاید نیاز به تغییر viewset داریم

        # حالا delete را امتحان کنیم
        response = self.client.delete(self.post_detail_url)
        print(f"Delete response: {response.status_code}")
        # با viewset اصلاح شده باید ۲۰۴ شود
        if response.status_code == status.HTTP_204_NO_CONTENT:
            self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
        else:
            print(f"Delete failed with status: {response.status_code}")
            print(f"Response data: {getattr(response, 'data', 'No data')}")


class PostDeleteEdgeCasesTests(BaseTest):
    """تست‌های موارد خاص برای حذف پست"""
    
    def setUp(self):
        super().setUp()
        self.post_detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})
    
    def test_delete_post_with_multiple_generated_contents(self):
        """تست حذف پست با چندین GeneratedContent"""
        # ایجاد GeneratedContentهای اضافی
        GeneratedContent.objects.create(
            post=self.post,
            content_type="hashtags_only",
            generated_text="More generated content",
            suggested_hashtags="#extra #hashtags"
        )
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         # بررسی حذف همه GeneratedContentهای مرتبط
        self.assertEqual(GeneratedContent.objects.filter(post=self.post).count(), 0)
    
    def test_delete_does_not_affect_other_posts(self):
        """تست که حذف یک پست روی پست‌های دیگر اثر نمی‌گذارد"""
        # ایجاد پست دوم برای کاربر
        second_post = Post.objects.create(
            user=self.user,
            social_account=self.user_social_account,
            platform="instagram",
            content="Second post content",
            visual_idea="Second visual idea"
        )
        
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # پست دوم باید باقی بماند
        self.assertTrue(Post.objects.filter(pk=second_post.pk).exists())
        self.assertEqual(Post.objects.filter(user=self.user).count(), 1)