from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)

        # ✅ بررسی دستی وجود ایمیل (جایگزین email_address_exists)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self, request):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            password=self.validated_data['password1']
        )
        return user


class GoogleLoginSerializer(serializers.Serializer):
    google_id = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(allow_blank=True)
    picture = serializers.URLField(allow_blank=True)
    email_verified = serializers.BooleanField(default=False)
    last_login = serializers.DateTimeField()

    def create_or_update_user(self, validated_data):
        email = validated_data['email']
        google_id = validated_data['google_id']

        # فقط فیلدهای واقعی مدل رو در defaults بگذارید
        defaults = {
            'google_id': google_id,
            'profile_picture': validated_data.get('picture'),
            'is_email_verified': validated_data.get('email_verified', False),
            'last_login': validated_data['last_login'],
        }

        # اگر name دارید، اول و آخر نام رو جدا کنید (اختیاری)
        full_name = validated_data.get('name', '')
        if full_name:
            names = full_name.split(' ', 1)
            defaults['first_name'] = names[0]
            defaults['last_name'] = names[1] if len(names) > 1 else ''

        # اگر username لازم بود (اگر مدل دارید)، اضافه کنید
        # defaults['username'] = email.split('@')[0]  # اگر فعال باشه

        user, created = User.objects.update_or_create(
            email=email,  # lookup با email
            defaults=defaults
        )

        if created:
            user.set_unusable_password()  # چون با گوگل لاگین می‌کنه
            user.save()

        return user
    
