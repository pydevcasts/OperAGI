# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import logging
# import json
from transformers import AutoTokenizer, AutoModelForCausalLM






import os  # Importing the os module to interact with the operating system
# import wandb  # Importing Weights & Biases library for tracking experiments
# from huggingface_hub import login  # Importing the login function from the Hugging Face Hub library

# # Setting environment variables
# os.environ['HUGGING_FACE_TOKEN'] = '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'  # Setting the Hugging Face token as an environment variable
# os.environ['WANDB_TOKEN'] = 'ed870bd1c8aef77a8d6e551f70800aa3d529224a'  # Setting the Weights & Biases token as an environment variable

# # Accessing the tokens from environment variables
# hugging_face_token = os.environ['HUGGING_FACE_TOKEN']  # Retrieving the Hugging Face token
# wandb_token = os.environ['WANDB_TOKEN']  # Retrieving the Weights & Biases token




# Logging into Hugging Face account using the Hugging Face token
# login(hugging_face_token)  # Using the previously defined Hugging Face token to authenticate

# Logging into Weights & Biases with the provided API key
# wandb.login(key=wandb_token)  # Using the previously defined Weights & Biases token to authenticate

# logger = logging.getLogger(__name__)

# # بارگذاری مدل DeepSeek از Hugging Face
# try:
#     tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", trust_remote_code=True)
#     deepseek_model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", trust_remote_code=True)

#     # انتقال مدل به GPU اگر موجود باشد
#     if torch.cuda.is_available():
#         deepseek_model = model.to('cuda')
# except Exception as e:
#     logger.error(f"Error loading DeepSeek model: {e}")
#     tokenizer = None
#     deepseek_model = None

# class DeepSeekResponseView(APIView):
#     def post(self, request) -> Response:
#         try:
#             if deepseek_model is None or tokenizer is None:
#                 return Response(
#                     {'error': 'DeepSeek model is not loaded. Please check model files.'}, 
#                     status=status.HTTP_503_SERVICE_UNAVAILABLE
#                 )

#             # دریافت متن از درخواست
#             data = json.loads(request.body)
#             user_input = data.get('text')

#             if not user_input:
#                 return Response(
#                     {'error': 'No text provided'}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # ایجاد پرامپت با فرمت مناسب
#             prompt = f"""### Question:
# {user_input}

# ### Response:
# """

#             # تولید پاسخ با استفاده از مدل
#             inputs = tokenizer(prompt, return_tensors="pt").to(deepseek_model.device)
#             outputs = deepseek_model.generate(
#                 **inputs,
#                 max_length=1024,
#                 num_beams=5,
#                 temperature=0.7,
#                 top_k=50,
#                 top_p=0.95,
#                 do_sample=True,
#                 pad_token_id=tokenizer.eos_token_id
#             )

#             response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

#             # حذف پرامپت از پاسخ نهایی
#             final_response = response_text.split("### Response:")[-1].strip()

#             return Response(
#                 {'response': final_response},
#                 status=status.HTTP_200_OK
#             )

#         except Exception as e:
#             logger.error(f"Error generating response: {e}")
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
