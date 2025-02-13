# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import torchaudio
# from torchaudio.transforms import Resample
# from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
# import torch
# import logging

# # Load the HuBERT model and processor
# processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
# model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# logger = logging.getLogger(__name__)

# class TranscribeAudioView(APIView):
#     def post(self, request):
#         if 'audio' not in request.FILES:
#             return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)

#         audio_file = request.FILES['audio']
        
#         # Validate file type and size
#         if audio_file.content_type not in ['audio/wav', 'audio/mpeg']:
#             return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)
#         if audio_file.size > 10 * 1024 * 1024:  # 10 MB limit
#             return Response({'error': 'File size exceeds limit'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             waveform, sample_rate = torchaudio.load(audio_file)
#         except Exception as e:
#             logger.error(f"Error loading audio file: {e}")
#             return Response({'error': 'Failed to load audio file'}, status=status.HTTP_400_BAD_REQUEST)

#         # Resample if necessary
#         if sample_rate != 16000:
#             logger.warning(f"Input sample rate is {sample_rate}. Converting to 16000 Hz.")
#             resample = Resample(orig_freq=sample_rate, new_freq=16000)
#             waveform = resample(waveform)

#         # Process input
#         try:
#             inputs = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt", padding=True)
#             with torch.no_grad():
#                 logits = model(inputs.input_values).logits
#             predicted_ids = torch.argmax(logits, dim=-1)
#             transcription = processor.batch_decode(predicted_ids)
#         except Exception as e:
#             logger.error(f"Error during transcription: {e}")
#             return Response({'error': 'Transcription failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Log and return the transcription
#         logger.info(f"Transcription: {transcription[0]}")
#         return Response({'transcription': transcription[0]})