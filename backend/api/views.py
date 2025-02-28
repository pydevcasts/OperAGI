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

# # views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import requests

# @csrf_exempt 
# def chat_completion(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_input = data.get('messages')[0].get('content')

#             # Call the external API
#             url = 'https://openrouter.ai/api/v1/chat/completions'
#             headers = {
#                 'Authorization': 'Bearer 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',  # Keep this secure
#                 'Content-Type': 'application/json',
#             }
#             body = {
#                 'model': 'deepseek/deepseek-r1:free',
#                 'messages': [{'role': 'user', 'content': user_input}],
#             }

#             response = requests.post(url, headers=headers, json=body)
#             response.raise_for_status()  # Raise an error for bad responses
#             response_data = response.json()
#             return JsonResponse(response_data)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
#         except requests.exceptions.HTTPError as http_err:
#             return JsonResponse({'error': str(http_err)}, status=response.status_code)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)  # Use 405 for method not allowed


### new ###


# # %%capture: This line hides the outputs of the next cell in Jupyter Notebook.
# # This allows you to prevent unnecessary outputs.

# # Install required packages
# # !pip install unsloth  # Install the unsloth package
# # !pip install --force-reinstall --no-cache-dir --no-deps git+https://github.com/unslothai/unsloth.git  # Reinstall unsloth from GitHub
# # !pip install --upgrade jupyter  # Upgrade Jupyter Notebook
# # !pip install --upgrade ipywidgets  # Upgrade ipywidgets
# # !pip install wandb  # Install wandb for project management and tracking
# # !pip install --upgrade torch  # Upgrade PyTorch

# import os  # Import the os library for environment variable management

# # Set environment variables for access tokens
# os.environ['HUGGING_FACE_TOKEN'] = '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'  # Hugging Face token
# os.environ['WANDB_TOKEN'] = 'ed870bd1c8aef77a8d6e551f70800aa3d529224a'  # Weights & Biases token

# # Access tokens from environment variables
# hugging_face_token = os.environ['HUGGING_FACE_TOKEN']  # Hugging Face token
# wandb_token = os.environ['WANDB_TOKEN']  # Weights & Biases token

# # Print tokens (to ensure they have been loaded correctly)
# print(hugging_face_token)
# print(wandb_token)
# import unsloth
# import torch  # Import PyTorch library
# from unsloth import FastLanguageModel  # Import FastLanguageModel from unsloth
# from trl import SFTTrainer  # Import SFTTrainer from the trl library
# from unsloth import is_bfloat16_supported  # Check for bfloat16 support
# from huggingface_hub import login  # Import the login function from huggingface_hub
# from transformers import TrainingArguments  # Import TrainingArguments class from transformers
# from datasets import load_dataset  # Import load_dataset function from datasets
# import wandb  # Import wandb for project management
# from huggingface_hub import login  # Import login function again

# # Log in to Hugging Face account using the token
# login(hugging_face_token)

# # Log in to Weights & Biases account using the token
# wandb.login(key=wandb_token)

# # Start a new run in wandb for tracking the project
# run = wandb.init(
#     project='Fine_tune_DeepSeeek_Llama_80 on Medical COT Dataset',  # Project name
#     job_type="training",  # Job type
#     anonymous="allow"  # Allow anonymous usage
# )

# # Model settings
# max_seq_length = 2048  # Maximum input sequence length
# dtype = None  # Data type (can be None to default automatically)
# load_in_4bit = True  # Load model in 4-bit mode

# # Load the model and tokenizer
# model, tokenizer = FastLanguageModel.from_pretrained(
#     model_name="unsloth/DeepSeek-R1-Distill-Llama-8B",  # Model name
#     max_seq_length=max_seq_length,  # Maximum sequence length
#     dtype=dtype,  # Data type
#     load_in_4bit=load_in_4bit,  # Load in 4-bit mode
#     token=hugging_face_token  # Token for access
# )

# # Prompt template for model responses
# prompt_template = """### Role:
# You are a medical expert specializing in clinical reasoning, diagnostics, and treatment planning. Your responses should:
# - Be evidence-based and clinically relevant
# - Include differential diagnoses when appropriate
# - Consider patient safety and standard of care
# - Note any important limitations or uncertainties

# ### Question:
# {}


# ### Response:
# <think>{}

# """

# # Define the question
# question = """Can you tell me which city is the capital of Iran and what its features are?”"""

# # Call the model for inference
# FastLanguageModel.for_inference(model)  # Prepare the model for inference

# # Prepare inputs for the model
# inputs = tokenizer([prompt_template.format(question, "")], return_tensors="pt").to("cuda")  # Tokenize input and move to GPU

# # Generate response using the model
# outputs = model.generate(
#     input_ids=inputs.input_ids,  # Input IDs
#     attention_mask=inputs.attention_mask,  # Attention mask
#     max_new_tokens=1200,  # Maximum number of new tokens to generate
#     use_cache=True,  # Use cache to speed up the process
# )

# # Decode the outputs into readable text
# response = tokenizer.batch_decode(outputs)  # Decode the outputs
# print(response[0].split("### Response:")[1])  # Print the final response by splitting the response section




#################3
# Import necessary libraries
import unsloth 
import os
import torch
import wandb
from unsloth import FastLanguageModel
from huggingface_hub import login
from transformers import TrainingArguments
from datasets import load_dataset

# Set environment variables for access tokens
os.environ['HUGGING_FACE_TOKEN'] = 'your_hugging_face_token'
os.environ['WANDB_TOKEN'] = 'your_wandb_token'

# Log in to Hugging Face and Weights & Biases
login(os.environ['HUGGING_FACE_TOKEN'])
wandb.login(key=os.environ['WANDB_TOKEN'])

# Check for GPU availability
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Model settings
max_seq_length = 2048
dtype = None  # Consider specifying dtype as torch.float16 if you're using mixed precision
load_in_4bit = True

# Load the model and tokenizer
try:
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/DeepSeek-R1-Distill-Llama-8B",
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=load_in_4bit,
        token=os.environ['HUGGING_FACE_TOKEN']
    )
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# Start a new run in wandb
run = wandb.init(project='Fine_tune_DeepSeek_Llama_80 on Medical COT Dataset', job_type="training", anonymous="allow")

# Prepare the prompt
prompt_template = """### Role:
You are a medical expert specializing in clinical reasoning, diagnostics, and treatment planning. Your responses should:
- Be evidence-based and clinically relevant
- Include differential diagnoses when appropriate
- Consider patient safety and standard of care
- Note any important limitations or uncertainties

### Question:
{}

### Response:
<think>{}
"""

# Define the question
question = "Can you tell me which city is the capital of Iran and what its features are?"

# Prepare inputs for the model
FastLanguageModel.for_inference(model)
inputs = tokenizer([prompt_template.format(question, "")], return_tensors="pt").to(device)  # Use the selected device

# Generate response using the model
try:
    outputs = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_new_tokens=1200,
        use_cache=True,
    )
    
    # Decode and print the response
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)  # Skip special tokens
    final_response = response[0].split("### Response:")[1].strip()  # Stripping any extra whitespace
    print(final_response)
    
except Exception as e:
    print(f"Error during model inference: {e}")