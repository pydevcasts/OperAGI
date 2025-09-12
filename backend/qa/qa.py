# # 📄 helper/llm.py — TEST VERSION — NO POST-PROCESSING — RAW OUTPUT

# import requests
# import json
# import logging
# import time

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def generate_answer(question, context_chunks):
#     """
#     Generate answer using Ollama's qwen3:0.6b — RAW OUTPUT for testing.
#     NO regex, NO cleaning — return exactly what model returns.
#     """
#     start_time = time.time()
#     logger.info(f"🔄 [START] Generating answer for: {question[:50]}...")

#     # === Step 1: Validate & Format Context ===
#     context_text = ""
#     try:
#         if isinstance(context_chunks, list) and len(context_chunks) > 0:
#             if isinstance(context_chunks[0], dict) and 'content' in context_chunks[0]:
#                 context_text = "\n\n".join(chunk['content'] for chunk in context_chunks if chunk.get('content', '').strip())
#             else:
#                 context_text = "\n\n".join(str(chunk) for chunk in context_chunks if str(chunk).strip())
#         logger.info(f"✅ Context length: {len(context_text)} chars | {len(context_chunks)} chunks")
#     except Exception as e:
#         logger.error(f"❌ Error formatting context: {e}")
#         return "خطا: پردازش متن اسناد با مشکل مواجه شد."

#     # === Step 2: Build Simple Prompt ===
#     prompt = f"""
# You are pydevcasts, a helpful assistant.
# Answer based ONLY on the context below.
# Be clear and concise.

# Context:
# {context_text}

# Question:
# {question}

# Answer:
# """

#     # === Step 3: Call Ollama ===
#     url = "http://localhost:11434/api/generate"
#     payload = {
#         "model": "qwen3:0.6b",
#         "prompt": prompt,
#         "stream": False,
#         "options": {
#             "temperature": 0.7,
#             "top_p": 0.9,
#             "num_predict": 256,
#             "num_ctx": 2048,
#             "stop": ["Question:", "Context:", "Answer:"],
#             "repeat_penalty": 1.1
#         }
#     }

#     try:
#         logger.info("📡 Sending request to Ollama...")
#         response = requests.post(url, json=payload, timeout=60)
#         response.raise_for_status()
#         result = response.json()
#         raw_answer = result.get("response", "").strip()

#         # === 🚫 NO POST-PROCESSING — RETURN RAW ANSWER ===
#         duration = time.time() - start_time
#         logger.info(f"✅ [SUCCESS] Answer generated in {duration:.2f} seconds.")
#         logger.info(f"📝 RAW ANSWER:\n{raw_answer}\n")

#         # فقط اگر خالی بود — fallback
#         if not raw_answer:
#             return "پاسخی از مدل دریافت نشد."

#         return raw_answer  # ✅ بدون هیچ تغییری — خام برمی‌گرده

#     except requests.exceptions.Timeout:
#         logger.error("❌ Ollama request timed out.")
#         return "خطا: زمان پاسخ مدل به پایان رسید."

#     except Exception as e:
#         logger.error(f"❌ Unexpected error: {str(e)}")
#         return f"خطا در ارتباط با مدل: {str(e)}"

# ================================
# 📄 helper/llm.py — Ollama Integration with qwen3:0.6b for RAG

import requests
import json
import logging

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_answer(question, context_chunks):
    """
    Generate a detailed and accurate answer using Ollama's qwen3:0.6b model based on retrieved context chunks.

    Args:
        question (str): The user's question.
        context_chunks (list): List of context chunks (either dict with 'content' key or plain strings).

    Returns:
        str: Generated answer from the model, or error message if failed.
    """
    
    # Validate and format context text
    context_text = ""
    try:
        if isinstance(context_chunks, list) and len(context_chunks) > 0:
            if isinstance(context_chunks[0], dict) and 'content' in context_chunks[0]:
                # Extract 'content' from each chunk dictionary
                context_text = "\n\n".join(chunk['content'] for chunk in context_chunks if chunk.get('content'))
            else:
                # Assume list of strings
                context_text = "\n\n".join(str(chunk) for chunk in context_chunks if str(chunk).strip())
        logger.info(f"✅ Context length: {len(context_text)} chars | {len(context_chunks)} chunks")
    except Exception as e:
        logger.error(f"Error formatting context chunks: {e}")
        return "Error: Could not process context chunks."

    # If no context is available, inform the model explicitly
    if not context_text.strip():
        context_text = "No relevant context found."

    # Optimized prompt for qwen3:0.6b to encourage detailed, accurate, and long-form answers
    # Using clear instructions and structured format to guide the model
    prompt = f"""You are a helpful, precise, and thorough AI assistant.
                    Your task is to answer the user's question based ONLY on the provided context below.
                    If the context does not contain enough information, say "I cannot answer based on the given context."
                    Otherwise, provide a comprehensive, well-structured, and detailed response.

                    === CONTEXT ===
                    {context_text}
                    === END CONTEXT ===

                    === QUESTION ===
                    {question}
                    === END QUESTION ===

                    === INSTRUCTIONS ===
                    - Answer in Persian:.
                    - Be detailed and thorough — aim for at least 8-24 sentences if possible.
                    - Use bullet points or paragraphs for clarity.
                    - Do NOT make up information — stick strictly to the context.
                    - If context is irrelevant, say so clearly.
                    === ANSWER ===
            """

    # Ollama API endpoint
    url = "http://localhost:11434/api/generate"
    
    # Model parameters optimized for longer, higher-quality responses
    payload = {
        "model": "gemma3:latest",  # ← این مدل رو دارید؟ (نکته مهم بعداً)
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,        # پایین = دقیق‌تر، کم‌تخیل
            "top_p": 0.9,
            "num_predict": 2048,       # ✅ افزایش شدید! (از 256 → 2048)
            "num_ctx": 4096,           # ✅ مناسب برای context بلند
            "repeat_penalty": 1.1,
            "stop": []                 # ✅ ترجیحاً خالی بذارید — اگر stop باشه ممکن است زود قطع کنه
        }
    }

    try:
        # Send request to Ollama
        logger.info(f"Sending request to Ollama for question: {question[:50]}...")
        response = requests.post(url, json=payload, timeout=180)  # Increased timeout for longer generation
        response.raise_for_status()
        
        result = response.json()
        answer = result.get("response", "").strip()
        
        # Fallback if model returns empty or refuses to answer
        if not answer:
            answer = "متاسفانه نمی‌توانم بر اساس اطلاعات موجود پاسخ دقیقی ارائه دهم."
        
        logger.info("Successfully received answer from Ollama.")
        return answer

    except requests.exceptions.Timeout:
        error_msg = "Error: Request to Ollama timed out. Try again or check if Ollama service is running."
        logger.error(error_msg)
        return error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"Error: Failed to connect to Ollama. Details: {str(e)}"
        logger.error(error_msg)
        return error_msg

    except Exception as e:
        error_msg = f"Unexpected error in generate_answer: {str(e)}"
        logger.error(error_msg)
        return error_msg