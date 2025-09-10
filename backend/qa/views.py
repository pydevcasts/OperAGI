# 📄 qa/views.py — FINAL VERSION — با اصلاح خطای numpy.int64

from .qa import generate_answer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import QuestionSerializer
from documents.models import Document, DocumentChunk
from helper.embedding import get_embedding
import numpy as np
import faiss
import logging

logger = logging.getLogger(__name__)


class AskQuestionView(APIView):
    @swagger_auto_schema(
        request_body=QuestionSerializer,
        responses={
            200: openapi.Response(
                description='Successful Response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'answer': openapi.Schema(type=openapi.TYPE_STRING, description='The answer to the question')
                    }
                )
            ),
            400: openapi.Response(
                description='Bad Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            ),
            404: openapi.Response(
                description='Document Not Found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Document not found')
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        document_id = serializer.validated_data['document_id']
        question = serializer.validated_data['question']

        # ✅ ۱. چک کن سند وجود داره
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({"error": "سند یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ ۲. Embedding سوال رو بگیر
        try:
            logger.info(f"🔍 Generating embedding for question: {question[:50]}...")
            question_embedding = get_embedding(question)
            logger.info(f"✅ Question embedding length: {len(question_embedding)}")
            
            # تبدیل به NumPy array برای FAISS
            question_embedding = np.array(question_embedding).astype('float32').reshape(1, -1)
            logger.info(f"📊 Question embedding shape: {question_embedding.shape}")
        except Exception as e:
            logger.error(f"❌ Failed to generate embedding for question: {question} | Error: {str(e)}")
            return Response({"error": f"خطا در Embedding: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ✅ ۳. چانک‌های این سند رو بگیر — و به لیست تبدیل کن
        chunks_queryset = DocumentChunk.objects.filter(document=document).order_by('index')
        if not chunks_queryset.exists():
            return Response({"error": "این سند هنوز پردازش نشده یا چانکی ندارد."}, status=status.HTTP_400_BAD_REQUEST)
        
        # ✅ تبدیل QuerySet به لیست — برای جلوگیری از مشکلات numpy.int64
        chunks = list(chunks_queryset)

        # ✅ ۴. Embeddingهای چانک‌ها رو بارگذاری کن
        try:
            chunk_embeddings = np.array([chunk.embedding for chunk in chunks]).astype('float32')
            logger.info(f"🧠 Loaded {len(chunks)} chunk embeddings. Shape: {chunk_embeddings.shape}")
        except Exception as e:
            logger.error(f"❌ Failed to load chunk embeddings: {str(e)}")
            return Response({"error": f"خطا در بارگذاری Embedding چانک‌ها: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # ✅ ۵. FAISS رو راه‌اندازی کن
        dimension = chunk_embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(chunk_embeddings)

        # ✅ ۶. جستجوی k=3 چانک مرتبط
        D, I = index.search(question_embedding, k=3)
        logger.info(f"🔎 FAISS results — Indices: {I[0]} | Distances: {D[0]}")

        # ✅ اصلاح خطا: تبدیل numpy.int64 به int
        retrieved_chunks = [chunks[int(i)] for i in I[0]]  # ✅ int(i) — کلید اصلی رفع خطا

        # ✅ ۷. تبدیل به فرمت مورد نیاز generate_answer
        context_chunks = [{'content': chunk.content} for chunk in retrieved_chunks]
        logger.info(f"📚 Retrieved {len(context_chunks)} chunks for context.")

        # ✅ ۸. ارسال به مدل
        try:
            answer = generate_answer(question, context_chunks)
            return Response({"answer": answer}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"❌ Error in generate_answer: {str(e)}")
            return Response({"error": f"خطا در تولید پاسخ: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)