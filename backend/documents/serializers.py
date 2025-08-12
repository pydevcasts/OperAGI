from rest_framework import serializers
from .models import Document

class UploadedDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'pdf_file', 'uploaded_at']
        read_only_fields = ['uploaded_at']
