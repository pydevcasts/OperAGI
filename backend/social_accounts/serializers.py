from allauth.socialaccount.models import SocialAccount
from rest_framework import serializers

from .models import UserSocialAccount


class SocialAccountSerializer(serializers.ModelSerializer):
    extra_data = serializers.SerializerMethodField()

    class Meta:
        model = SocialAccount
        fields = ('id', 'provider', 'uid', 'extra_data')
        read_only_fields = ('id',)
        validators = []

    def get_extra_data(self, obj):
        sensitive = {'access_token', 'refresh_token', 'token', 'secret'}
        return {key: value for key, value in (obj.extra_data or {}).items() if key.lower() not in sensitive}


class UserSocialAccountSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    social_account = SocialAccountSerializer()
    provider = serializers.CharField(read_only=True)

    class Meta:
        model = UserSocialAccount
        fields = (
            'id', 'user', 'provider', 'social_account', 'display_name', 'external_url',
            'is_active', 'connected_at', 'updated_at',
        )
        read_only_fields = ('id', 'user', 'provider', 'connected_at', 'updated_at')

    def get_user(self, obj):
        return {'id': obj.user_id, 'email': obj.user.email}

    def validate(self, attrs):
        social = attrs.get('social_account', {})
        if social.get('provider') not in {'instagram', 'twitter', 'youtube'}:
            raise serializers.ValidationError({'social_account': 'Provider must be instagram, twitter, or youtube.'})
        if not social.get('uid'):
            raise serializers.ValidationError({'social_account': 'uid is required.'})
        return attrs

    def create(self, validated_data):
        current_user = self.context['request'].user
        social_data = validated_data.pop('social_account')
        social_account = SocialAccount.objects.filter(
            provider=social_data['provider'], uid=social_data['uid']
        ).first()
        if social_account and social_account.user_id != current_user.id:
            raise serializers.ValidationError({'social_account': 'This social identity is already connected.'})
        if not social_account:
            social_account = SocialAccount.objects.create(
                user=current_user,
                provider=social_data['provider'],
                uid=social_data['uid'],
                extra_data=self.context['request'].data.get('social_account', {}).get('extra_data', {}),
            )
        connection, _ = UserSocialAccount.objects.update_or_create(
            social_account=social_account,
            defaults={'user': current_user, **validated_data},
        )
        return connection
