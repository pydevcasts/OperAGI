from documents.models import Document, DocumentChunk
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UploadedDocumentSerializer
from helper.utils import extract_text_from_file, chunk_text
from helper.embedding import get_embedding
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import numpy as np

class UploadDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Upload a file (TXT or PDF) to process and store its content.",
        manual_parameters=[
            openapi.Parameter(
                'title',
                openapi.IN_FORM,
                description="Title of the document",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'file',
                openapi.IN_FORM,
                description="File to upload (TXT or PDF)",
                type=openapi.TYPE_FILE,
                required=True
            ),
        ],
        responses={
            201: openapi.Response(
                description='File processed successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
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
            500: openapi.Response(
                description='Internal Server Error',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = UploadedDocumentSerializer(data=request.data)
        if serializer.is_valid():
            # Save the document without user if not authenticated
            document = serializer.save(user=request.user if request.user.is_authenticated else None)
            try:
                # Extract text from the saved file
                text = extract_text_from_file(document.file.path)
                # Split text into chunks
                chunks = chunk_text(text, max_chunk_size=500)
                # Generate and store embeddings for each chunk
                for idx, chunk in enumerate(chunks):
                    embedding = get_embedding(chunk)
                    # Handle different embedding formats
                    if isinstance(embedding, np.ndarray):
                        embedding_list = embedding.tolist()
                    elif isinstance(embedding, dict) and 'embedding' in embedding:
                        embedding_list = embedding['embedding']
                    elif isinstance(embedding, list):
                        embedding_list = embedding  # Already a list
                    else:
                        raise ValueError(f"Unexpected embedding format: {type(embedding)}")
                    DocumentChunk.objects.create(
                        document=document,
                        content=chunk,
                        embedding=embedding_list,
                        index=idx
                    )
                # Mark document as processed
                document.processed = True
                document.save()
                return Response({'message': 'File processed and chunks stored successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Delete document if processing fails
                document.delete()
                return Response({'error': f"Failed to process file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)