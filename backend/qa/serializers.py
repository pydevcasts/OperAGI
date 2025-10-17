# 📄 qa/serializers.py

from rest_framework import serializers

class QuestionSerializer(serializers.Serializer):
    document_id = serializers.IntegerField(required=True, help_text="شناسه سند")
    question = serializers.CharField(required=True, help_text="سوال کاربر")
    profile = serializers.ChoiceField(
        choices=["quick", "balanced", "detailed", "creative"],
        default="balanced",  # ✅ پیش‌فرض
        help_text="سبک پاسخ: quick, balanced, detailed, creative"
    )
    language = serializers.ChoiceField(
        choices=["fa", "en", "es", "fr", "de", "zh", "ar", "ru", "ja", "ko"],
        default="fa",
        help_text="زبان پاسخ: fa=فارسی، en=انگلیسی، es=اسپانیایی، ..."
    )