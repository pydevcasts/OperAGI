import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import os
# بارگذاری مدل و پردازشگر
MODEL_PATH = os.path.join(os.getcwd(),"wav2vec2_finetuned/checkpoint-145")
processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)

# بارگذاری فایل صوتی
waveform, sample_rate = torchaudio.load("./wav/001-A.wav")

# تغییر نرخ نمونه به 16 کیلوهرتز اگر لازم باشد
if sample_rate != 16000:
    from torchaudio.transforms import Resample
    resample = Resample(orig_freq=sample_rate, new_freq=16000)
    waveform = resample(waveform)

# پردازش ورودی
try:
    # Convert waveform to the correct format
    inputs = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    print("Transcription:", transcription[0])
except Exception as e:
    print("Error during transcription:", e)