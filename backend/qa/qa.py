# import numpy as np
# from huggingface_hub import InferenceApi
# import json

# # Initialize the Hugging Face Inference API
# client = InferenceApi(repo_id="meta-llama/Meta-Llama-3-8B-Instruct", token="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")

# def generate_answer(question, context_chunks):
#     """Generate an answer based on the question and context chunks."""
#     # Convert context_chunks to list if it's a NumPy array
#     context_chunk_list = context_chunks.tolist() if isinstance(context_chunks, np.ndarray) else context_chunks

#     # Validate that context_chunk_list is a list
#     if not isinstance(context_chunk_list, list):
#         raise ValueError("context_chunk_list must be a list")

#     # Validate that each chunk is a dictionary with 'content' key
#     for chunk in context_chunk_list:
#         if not isinstance(chunk, dict) or 'content' not in chunk:
#             print("Invalid chunk:", chunk)  # For debugging
#             raise ValueError("Each chunk must be a dictionary with a 'content' key")

#     # Create context text by joining the content of each chunk
#     context_text = "\n\n".join(chunk['content'] for chunk in context_chunk_list)

#     # Prepare the prompt for the model
#     prompt = f"Question: {question}\n\nAnswer based on the following information:\n\n{context_text}"

#     # Debugging: Print the prompt and context
#     print("Sending request to the model with the prompt:")
#     print(prompt)
#     print("Context text:", context_text)

#     try:
#         # Call the Hugging Face Inference API with raw_response=True
#         response = client(prompt, raw_response=True)

#         # Check the status code
#         if response.status_code != 200:
#             print(f"Error: Received status code {response.status_code}")
#             print("Response content:", response.text)
#             return "An error occurred while receiving the response from the server."

#         # Try to parse the response as text or JSON
#         content_type = response.headers.get('content-type', '')
#         if 'application/json' in content_type:
#             response_json = response.json()
#             if isinstance(response_json, list) and len(response_json) > 0:
#                 return response_json[0].get('generated_text', '').strip()
#             else:
#                 return "No response found for your question."
#         elif 'text/plain' in content_type:
#             # Handle plain text response
#             return response.text.strip()
#         else:
#             print(f"Unsupported content type: {content_type}")
#             return "Unsupported response format from the server."

#     except Exception as e:
#         print("An error occurred:", e)
#         return "An error occurred while processing the response."


# ================================
# import numpy as np
# from huggingface_hub import InferenceClient

# # Initialize the Hugging Face Inference Client
# client = InferenceClient(
#     model="distilgpt2",
#     token="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"  # توکن API خود را وارد کنید
# )
# def generate_answer(question, context_chunks):
#     """Generate an answer based on the question and context chunks."""
#     context_chunk_list = context_chunks.tolist() if isinstance(context_chunks, np.ndarray) else context_chunks

#     # Validate that context_chunk_list is a list
#     if not isinstance(context_chunk_list, list):
#         raise ValueError("context_chunk_list must be a list")

#     # Validate that each chunk is a dictionary with 'content' key
#     for chunk in context_chunk_list:
#         if not isinstance(chunk, dict) or 'content' not in chunk:
#             print("Invalid chunk:", chunk)
#             raise ValueError("Each chunk must be a dictionary with a 'content' key")

#     # Create context text by joining the content of each chunk
#     context_text = "\n\n".join(chunk['content'] for chunk in context_chunk_list)

#     # Prepare the prompt for the model
#     prompt = f"Question: {question}\n\nAnswer based on the following information:\n\n{context_text}\n\nAnswer:"

#     # Debugging: Print the prompt and context
#     print("Sending request to the model with the prompt:")
#     print(prompt)
#     print("Context text:", context_text)

#     try:
#         # Call the Hugging Face Inference Client
#         response = client.text_generation(prompt, max_new_tokens=100, return_full_text=False)
#         print("Response:", response)
#         return response.strip()
#     except Exception as e:
#         print("An error occurred:", e)

import numpy as np
from openai import OpenAI
from django.conf import settings

# Initialize the OpenAI client
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    base_url="https://api.gapgpt.app/v1"
)

def generate_answer(question, context_chunks):
    """Generate an answer based on the question and context chunks."""
    context_chunk_list = context_chunks.tolist() if isinstance(context_chunks, np.ndarray) else context_chunks

    # Validate that context_chunk_list is a list
    if not isinstance(context_chunk_list, list):
        raise ValueError("context_chunk_list must be a list")

    # Validate that each chunk is a dictionary with 'content' key
    for chunk in context_chunk_list:
        if not isinstance(chunk, dict) or 'content' not in chunk:
            print("Invalid chunk:", chunk)
            raise ValueError("Each chunk must be a dictionary with a 'content' key")

    # Create context text by joining the content of each chunk
    context_text = "\n\n".join(chunk['content'] for chunk in context_chunk_list)

    # Prepare the prompt for the model
    prompt = f"Question: {question}\n\nAnswer based on the following information:\n\n{context_text}\n\nAnswer:"

    # Debugging: Print the prompt and context
    print("Sending request to the model with the prompt:")
    print(prompt)
    print("Context text:", context_text)

    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.6,
            top_p=0.9
        )
        
        # Extract the answer
        answer = response.choices[0].message.content.strip()
        print("Response:", answer)
        return answer

    except Exception as e:
        print("An error occurred:", e)
        # Fallback to direct answer from context if available
    