from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import torchaudio
from torchaudio.transforms import Resample
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import logging
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse



# Load the HuBERT model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

logger = logging.getLogger(__name__)

class TranscribeAudioView(APIView):
    def post(self, request):
        if 'audio' not in request.FILES:
            return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)

        audio_file = request.FILES['audio']
        
        # Validate file type and size
        if audio_file.content_type not in ['audio/wav', 'audio/mpeg']:
            return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)
        if audio_file.size > 10 * 1024 * 1024:  # 10 MB limit
            return Response({'error': 'File size exceeds limit'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            waveform, sample_rate = torchaudio.load(audio_file)
        except Exception as e:
            logger.error(f"Error loading audio file: {e}")
            return Response({'error': 'Failed to load audio file'}, status=status.HTTP_400_BAD_REQUEST)

        # Resample if necessary
        if sample_rate != 16000:
            logger.warning(f"Input sample rate is {sample_rate}. Converting to 16000 Hz.")
            resample = Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resample(waveform)

        # Process input
        try:
            inputs = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt", padding=True)
            with torch.no_grad():
                logits = model(inputs.input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = processor.batch_decode(predicted_ids)
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return Response({'error': 'Transcription failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Log and return the transcription
        logger.info(f"Transcription: {transcription[0]}")
        return Response({'transcription': transcription[0]})
        pass
def health_check(request):
    return HttpResponse("Healthy", status=200)



def deepseek(request):
    return render(request, 'home.html')

#######@#########################

# import requests

# # Replace with your OpenRouter API key
# API_KEY = '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'
# API_URL = 'https://openrouter.ai/api/v1/chat/completions'

# # Define the headers for the API request
# headers = {
#     'Authorization': f'Bearer {API_KEY}',
#     'Content-Type': 'application/json'
# }

# # Define the request payload (data)
# data = {
#     "model": "deepseek/deepseek-chat:free",
#     "messages": [{"role": "user", "content": "What is the meaning of life?"}]
# }

# # Send the POST request to the DeepSeek API
# response = requests.post(API_URL, json=data, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     print("API Response:", response.json())
# else:
#     print("Failed to fetch data from API. Status Code:", response.status_code)
# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

def chat_view(request):
    return render(request, 'home.html')

@csrf_exempt  # Disable CSRF for simplicity; use with caution in production
def chat_with_deepseek(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            # Replace with your OpenRouter API key
            API_KEY = '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'
            API_URL = 'https://openrouter.ai/api/v1/chat/completions'

            # Define the headers for the API request
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }

            # Define the request payload (data)
            payload = {
                "model": "deepseek/deepseek-chat:free",
                "messages": [{"role": "user", "content": user_message}]
            }

            # Send the POST request to the DeepSeek API
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                return JsonResponse(response.json())
            else:
                return JsonResponse({'error': 'Failed to fetch data from API'}, status=response.status_code)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
