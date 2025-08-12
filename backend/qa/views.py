from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from embeddings.embedding import get_embedding
from .search import retrieve_relevant_chunks
from .qa import generate_answer

class AskQuestionView(APIView):
    def post(self, request):
        question = request.data.get("question")
        query_embedding = get_embedding(question)
        relevant_chunks = retrieve_relevant_chunks(query_embedding)
        answer = generate_answer(question, relevant_chunks)

        return Response({"answer": answer})
