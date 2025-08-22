import io
import torch
import logging
import torchaudio
from conf import settings
from pydub import AudioSegment
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from transformers import WhisperProcessor, WhisperForConditionalGeneration



ffmpeg_path = '/usr/bin/ffmpeg'
AudioSegment.converter = ffmpeg_path

logger = logging.getLogger(__name__)

processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3-turbo")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3-turbo")

class TranscribeAudioView(APIView):
    def post(self, request):
        audio_file = request.FILES.get('audio')
        logger.debug(f"Received file: {audio_file}, Content-Type: {audio_file}")

        if not audio_file:
            return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            audio_segment = AudioSegment.from_file(audio_file)
            audio_segment = audio_segment.set_frame_rate(16000)
        except Exception as e:
            logger.error(f"Error converting audio file: {e}")
            return Response({'error': 'Error converting audio file'}, status=status.HTTP_400_BAD_REQUEST)

        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        waveform, sample_rate = torchaudio.load(wav_io)
        inputs = processor(waveform.squeeze(), sampling_rate=sample_rate, return_tensors="pt")
        with torch.no_grad():
            predicted_ids = model.generate(
                **inputs,
                max_length=448,  # حداکثر طول خروجی
                num_beams=5,     # تعداد پرتوها برای جستجوی بهتر
                temperature=0.7, # کنترل تنوع
                top_k=50,        # تنظیم توزیع احتمالی
                top_p=0.95       # تنظیم توزیع احتمالی
            )
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return Response({'transcription': transcription}, status=status.HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai

# Set OpenAI API key and base URL
openai.api_key = settings.OPENAI_API_KEY
openai.api_base = 'https://api.gapgpt.app/v1'

class ChatCompletionView(APIView):
    def post(self, request):
        # Accept either 'message' or 'prompt' parameter for flexibility
        user_message = request.data.get('message') or request.data.get('prompt')

        if not user_message:
            return Response({'error': 'No message provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Using the older OpenAI API style (pre-v1.0.0)
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            # Extract the answer from the response
            answer = response['choices'][0]['message']['content']
            
            # Return both 'answer' and 'response' fields for compatibility
            return Response({'answer': answer, 'response': answer})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def health_check(request):
    health_status = {
        "status": "healthy",
        "models": {
            "whisper": "loaded" if 'processor' in globals() and 'model' in globals() else "not_loaded"
        }
    }
    return Response(health_status, status=status.HTTP_200_OK)