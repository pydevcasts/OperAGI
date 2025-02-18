import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import os

# Load the fine-tuned model and processor from the specified directory
MODEL_PATH = os.path.join(os.getcwd(), "wav2vec2_finetuned/checkpoint-116")
processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)  # Load the processor for feature extraction
model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)  # Load the Wav2Vec2 model for automatic speech recognition (ASR)

# Load the audio file
waveform, sample_rate = torchaudio.load("./wav/001-A.wav")  # Load the audio file and get the waveform and sample rate

# Resample the audio to 16 kHz if the sample rate is different
if sample_rate != 16000:
    from torchaudio.transforms import Resample  # Import the Resample transformation
    resample = Resample(orig_freq=sample_rate, new_freq=16000)  # Create a resampling object
    waveform = resample(waveform)  # Resample the audio waveform to 16 kHz

# Process the input audio for the model
try:
    # Convert the waveform to the correct format for the model
    inputs = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt", padding=True)
    # Use no_grad to disable gradient calculation for inference
    with torch.no_grad():
        logits = model(inputs.input_values).logits  # Get the model's output logits
    predicted_ids = torch.argmax(logits, dim=-1)  # Get the predicted token IDs by taking the argmax
    transcription = processor.batch_decode(predicted_ids)  # Decode the predicted IDs into text
    print("Transcription:", transcription[0])  # Print the transcription of the audio
except Exception as e:
    print("Error during transcription:", e)  # Print any errors that occur during the transcription process