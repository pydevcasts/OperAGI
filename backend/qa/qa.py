
# 📄 helper/llm.py — Ollama Integration with qwen3:0.6b for RAG

import requests
import logging

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 🌍 Language mapping — for instruction in prompt
LANGUAGE_MAP = {
    "fa": "Persian (Farsi)",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean"
}
# 📦 Predefined profiles for user selection
MODEL_PROFILES = {
    "quick": {
        "model": "phi3:mini",
        "num_predict": 128,
        "temperature": 0.4,
        "top_p": 0.9,
        "description": "Fast, short answers — ideal for quick queries."
    },
    "balanced": {
        "model": "gemma3:latest",
        "num_predict": 512,
        "temperature": 0.6,
        "top_p": 0.9,
        "description": "Good balance of speed and detail — recommended for most use cases."
    },
    "detailed": {
        "model": "gemma3:latest",  # یا gemma:7b / llama3:8b
        "num_predict": 2048,
        "temperature": 0.3,
        "top_p": 0.95,
        "description": "Long, thorough, precise answers — best for research, documentation, or RAG."
    },
    "creative": {
        "model": "llama3:8b",
        "num_predict": 1536,
        "temperature": 0.8,
        "top_p": 0.95,
        "description": "More imaginative responses — useful for brainstorming or storytelling."
    }
}
def generate_answer(question, context_chunks, profile="balanced",language="fa"):
    """
    Generate answer using Ollama with dynamic profile selection.

    Args:
        question (str): User's question.
        context_chunks (list): List of retrieved context chunks.
        profile (str): One of: "quick", "balanced", "detailed", "creative"
    """

    # Validate profile
    if profile not in MODEL_PROFILES:
        profile = "balanced"
    if language not in LANGUAGE_MAP:
        language = "fa"


    profile_config = MODEL_PROFILES[profile]
    model_name = profile_config["model"]
    num_predict = profile_config["num_predict"]
    temperature = profile_config["temperature"]
    top_p = profile_config["top_p"]
    target_language = LANGUAGE_MAP[language]

    # --- Format Context ---
    context_text = ""
    try:
        if isinstance(context_chunks, list) and len(context_chunks) > 0:
            if isinstance(context_chunks[0], dict) and 'content' in context_chunks[0]:
                context_text = "\n\n".join(chunk['content'] for chunk in context_chunks if chunk.get('content', '').strip())
            else:
                context_text = "\n\n".join(str(chunk) for chunk in context_chunks if str(chunk).strip())
    except Exception as e:
        logger.error(f"❌ Error formatting context: {e}")
        return "خطا: پردازش متن اسناد با مشکل مواجه شد."

    if not context_text.strip():
        context_text = "هیچ اطلاعات مرتبطی یافت نشد."

    # --- Prompt (همون قبلی، بدون تغییر) ---
    prompt = f"""
You are a helpful, precise, and thorough AI assistant.
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
- Answer in {target_language} .
- Be detailed and thorough — aim for at least 8–24 sentences.
- Use bullet points or paragraphs for clarity.
- Do NOT make up information — stick strictly to the context.
- If context is irrelevant, say so clearly.
=== ANSWER ===
"""

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "top_p": top_p,
            "num_predict": num_predict,
            "num_ctx": 4096,
            "repeat_penalty": 1.1,
            "stop": []
        }
    }

    try:
        logger.info(f"📡 Sending request with profile '{profile}' | Model: {model_name} | Lang={language} | Predict: {num_predict} tokens")
        response = requests.post(url, json=payload, timeout=180)
        response.raise_for_status()
        result = response.json()
        answer = result.get("response", "").strip()

        if not answer:
            fallback = {
                "fa": "متاسفانه نمی‌توانم پاسخ دهم.",
                "en": "Unfortunately, I cannot answer.",
                "es": "Lamentablemente, no puedo responder.",
                "fr": "Malheureusement, je ne peux pas répondre.",
                "de": "Leider kann ich nicht antworten.",
                "zh": "很遗憾，我无法回答。",
                "ar": "للأسف، لا يمكنني الإجابة.",
                "ru": "К сожалению, я не могу ответить.",
                "ja": "残念ながら、答えられません。",
                "ko": "죄송합니다, 답변할 수 없습니다."
            }
            answer = fallback.get(language, "Unable to respond.")

        logger.info(f"✅ Answer generated ({len(answer)} chars)")
        return answer

        logger.info(f"✅ Answer generated successfully ({len(answer)} chars)")
        return answer

    except requests.exceptions.Timeout:
        logger.error("❌ Request timed out.")
        return "خطا: زمان پاسخ مدل به پایان رسید."
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to connect to Ollama: {e}")
        return f"خطا در ارتباط با مدل: {str(e)}"
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return f"خطای ناشناخته: {str(e)}"
    

