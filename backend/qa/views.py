# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from embeddings.embedding import get_embedding
# from .search import retrieve_relevant_chunks
# from .qa import generate_answer

# class AskQuestionView(APIView):
#     def post(self, request):
#         question = request.data.get("question")
#         query_embedding = get_embedding(question)
#         relevant_chunks = retrieve_relevant_chunks(query_embedding)
#         answer = generate_answer(question, relevant_chunks)

#         return Response({"answer": answer})




from django.shortcuts import render
from qa.serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from helper.embedding import get_embedding
from .search import retrieve_relevant_chunks
from .qa import generate_answer
from rest_framework import status
# class AskQuestionView(APIView):
#     def post(self, request):
#         print("Request data:", request.data)  # For debugging
#         question = request.data.get("question")
        
#         if not question:  # Check if question is None or empty
#             return Response({"error": "سوال نمی‌تواند خالی باشد."}, status=400)

#         query_embedding = get_embedding(question)
#         relevant_chunks = retrieve_relevant_chunks(query_embedding)
#         answer = generate_answer(question, relevant_chunks)

#         return Response({"answer": answer})
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuestionSerializer  # فرض بر این است که این serializer شماست
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



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
                        'question': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description='List of errors')
                    }
                )
            )
        }
    )
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            question = serializer.validated_data.get('question')
            embedding = get_embedding(question)
            
            # Retrieve relevant chunks from the database
            relevant_chunks = retrieve_relevant_chunks(embedding, top_k=3)
            
            # Convert chunks to list of dictionaries with 'content' key
            context_chunks = [{'content': chunk.content} for chunk in relevant_chunks]
            
            # Generate the answer
            answer = generate_answer(question, context_chunks)
            return Response({"answer": answer}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)