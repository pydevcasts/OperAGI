# social_accounts/serializers.py
from rest_framework import serializers
from .models import UserSocialAccount, SocialAccount
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('id', 'provider', 'uid', 'extra_data', 'user') # 'user' را هم برای نمایش بگذارید
        read_only_fields = ('id', 'user') # user باید به صورت سیستمی ست شود
        validators = [] # اگر unique_together در مدل SocialAccount دارید، اینجا غیرفعال کنید


class UserSocialAccountSerializer(serializers.ModelSerializer):
    # برای نمایش اطلاعات کاربر، نه برای دریافت در POST
    user = serializers.SerializerMethodField()
    # social_account فیلد ورودی برای POST است
    social_account = SocialAccountSerializer()

    class Meta:
        model = UserSocialAccount
        fields = ('id', 'user', 'social_account')
        read_only_fields = ('id', 'user') # id و user از سمت سرور تعیین می‌شوند

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'email': obj.user.email,
        }

    def create(self, validated_data):
        # کاربر درخواست‌کننده
        current_user = self.context['request'].user

        # استخراج داده‌های social_account از ورودی
        social_account_data = validated_data.pop('social_account', {})
        provider = social_account_data.get('provider')
        uid = social_account_data.get('uid')
        extra_data = social_account_data.get('extra_data', {})

        # اعتبارسنجی اولیه
        if not provider or not uid:
            raise serializers.ValidationError("Both 'provider' and 'uid' are required in 'social_account' data.")

        # 1. پیدا کردن SocialAccount موجود بر اساس provider و uid (بدون در نظر گرفتن user)
        social_account = SocialAccount.objects.filter(
            provider=provider,
            uid=uid
        ).first()

        # 2. اگر SocialAccount وجود ندارد، آن را بساز
        if not social_account:
            social_account = SocialAccount.objects.create(
                user=current_user, # مالکیت اولیه با کاربر فعلی
                provider=provider,
                uid=uid,
                extra_data=extra_data,
            )
        # 3. اگر SocialAccount وجود دارد:
        else:
            if social_account.user is None:
                 social_account.user = current_user
                 social_account.save()
 
        user_social_account, created = UserSocialAccount.objects.get_or_create(
            user=current_user,
            social_account=social_account,
        )
        return user_social_account
