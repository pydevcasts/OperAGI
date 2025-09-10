
    # 📄 serializers.py

from rest_framework import serializers

class QuestionSerializer(serializers.Serializer):
    document_id = serializers.IntegerField(required=True, help_text="ID of the document to ask question about")
    question = serializers.CharField(required=True, help_text="The question text")