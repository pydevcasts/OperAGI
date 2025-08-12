from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UploadedDocumentSerializer
from embeddings.models import  DocumentChunk
from helper.utils import extract_text_from_pdf, chunk_text
from embeddings.embedding import get_embedding



class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UploadedDocumentSerializer(data=request.data)
        if serializer.is_valid():
            # 1. ذخیره فایل در مدل Document
            document = serializer.save(user=request.user)

            # 2. استخراج متن از فایل ذخیره شده
            text = extract_text_from_pdf(document.pdf_file.path)

            # 3. تقسیم متن به بخش‌های کوچک
            chunks = chunk_text(text, max_length=500)

            # 4. ساخت Embedding برای هر بخش و ذخیره در DocumentChunk
            for idx, chunk in enumerate(chunks):
                embedding = get_embedding(chunk)
                DocumentChunk.objects.create(
                    document=document,
                    content=chunk,
                    embedding=embedding,
                    index=idx
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)