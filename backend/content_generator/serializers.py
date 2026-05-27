from social_accounts.serializers import UserSocialAccountSerializer

from .models import GeneratedContent
from rest_framework import serializers
from .models import UserSocialAccount, Post


class PostSerializer(serializers.ModelSerializer):
    social_account_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSocialAccount.objects.all(),
        write_only=True 
    )
    user = serializers.StringRelatedField(read_only=True) # نمایش نام کاربری (بر اساس __str__ مدل User)
    social_account = UserSocialAccountSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'social_account',
            'social_account_id',
            'platform',
            'content',
            'visual_idea',
            'status',
            'created_at',
            'updated_at',
            'published_at',
        ]
        read_only_fields = ('user', 'social_account', 'status', 'created_at', 'updated_at', 'published_at')
    
    def validate_social_account_id(self, value):
        request = self.context.get('request')
        if request and value.user != request.user:
            raise serializers.ValidationError("Social account does not belong to the current user.")
        return value
    
    def create(self, validated_data):
        user_social_account = validated_data.pop('social_account_id')
        user = self.context['request'].user 
        post = Post.objects.create(user=user,\
                social_account=user_social_account, **validated_data)
        return post

    def update(self, instance, validated_data):
        validated_data.pop('social_account_id', None)
        return super().update(instance, validated_data)
    
    
class GeneratedContentSerializer(serializers.ModelSerializer):
    # نمایش post به صورت read-only (فقط نمایش ID)
    post = serializers.PrimaryKeyRelatedField(read_only=True) # یا StringRelatedField اگر بخواهید نام پست را نمایش دهید
    class Meta:
        model = GeneratedContent
        fields = [
            'id',
            'post',
            'content_type',
            'generated_text',
            'suggested_hashtags',
            'suggested_publish_time',
            'generated_at',
            'avatar_video_url',
            'audio_file_path',
        ]
        read_only_fields = ('post', 'generated_at') # این فیلدها فقط خواندنی هستند

    # --- اگر بخواهید هنگام ایجاد GeneratedContent، پست مربوطه را انتخاب کنید ---
    def create(self, validated_data):
        post_id = self.context['request'].data.get('post_id')
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post does not exist.")
        # اطمینان حاصل کنید که برای این پست قبلاً محتوایی تولید نشده است (به دلیل OneToOneField)
        if hasattr(post, 'generated_content'):
            raise serializers.ValidationError({"error":"Generated content already exists for this post."})
    
        generated_content = GeneratedContent.objects.create(post=post, **validated_data)
        return generated_content
    
   