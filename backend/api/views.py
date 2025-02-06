import io
import speech_recognition as sr
from pydub import AudioSegment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from transformers import pipeline
from rest_framework import serializers
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the NLP model for question answering
qa_pipeline = pipeline("question-answering")

@swagger_auto_schema(method='post', responses={200: 'Success', 400: 'Bad Request'})
@api_view(['POST'])
def transcribe_audio(request):
    if 'audio' not in request.FILES:
        return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)

    audio_file = request.FILES['audio']
    
    # Convert file to WAV
    try:
        audio_segment = AudioSegment.from_file(audio_file)
    except Exception as e:
        return Response({'error': 'Unsupported audio format or error processing audio file.'}, status=status.HTTP_400_BAD_REQUEST)

    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format='wav')
    wav_io.seek(0)

    # Use SpeechRecognition to process audio
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)  # Read the entire audio file
            transcription = recognizer.recognize_google(audio_data)  # Use Google Web Speech API
    except sr.UnknownValueError:
        return Response({'error': 'Google Web Speech API could not understand audio.'}, status=status.HTTP_400_BAD_REQUEST)
    except sr.RequestError as e:
        return Response({'error': f'Could not request results from Google Web Speech API; {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'transcription': transcription})

# Define a serializer for the question input
class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField()
@swagger_auto_schema(method='post', request_body=QuestionSerializer, responses={200: 'Success', 400: 'Bad Request'})
@api_view(['POST'])
def get_answer(request):
    logging.debug(f"Received request data: {request.data}")
    
    question = request.data.get('question')
    
    # Provide a detailed context about Docker
    context = """
    Docker is an open-source platform used for developing, shipping, and running applications inside containers. 
    Containers allow a developer to package up an application with all parts it needs, such as libraries and other dependencies, 
    and ship it all out as one package. This guarantees that the application will run on any other Linux machine regardless of any 
    customized settings that machine might have that could differ from the machine used for writing and testing the code.

    Docker provides a standardized unit of software, packaging up code and all its dependencies so the application runs quickly 
    and reliably from one computing environment to another. It is widely used in microservices architecture, allowing developers 
    to deploy applications in isolated environments, making them easy to manage and scale.
    """

    if not question:
        logging.error("No question provided in the request.")
        return Response({'error': 'No question provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        answer = qa_pipeline(question=question, context=context)
        logging.debug(f"Full answer generated: {answer}")  # Log the entire answer object
        if answer and 'answer' in answer:
            return Response({'answer': answer['answer'], 'score': answer['score'], 'context': context})
        else:
            return Response({'error': 'No answer found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logging.error(f"Error during question answering: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)