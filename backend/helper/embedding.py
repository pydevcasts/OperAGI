import logging
import numpy as np
from sentence_transformers import SentenceTransformer

# تنظیم لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# مدل Embedding — یک بار لود می‌شه
embedding_model = SentenceTransformer('BAAI/bge-m3')

def get_embedding(text):
    """
    Generate embedding for the given text.
    Returns a Python list of floats.
    Raises ValueError if text is empty or invalid.
    """
    try:
        # حذف فضاهای اضافی
        text = str(text).strip()
        
        if not text:
            raise ValueError("متن ورودی خالی است.")
        
        # تولید Embedding
        embedding = embedding_model.encode(text, normalize_embeddings=True)
        
        # تبدیل به لیست پایتون
        if isinstance(embedding, np.ndarray):
            embedding_list = embedding.tolist()
        else:
            embedding_list = list(embedding)
        
        # اعتبارسنجی خروجی
        if not isinstance(embedding_list, list) or len(embedding_list) == 0:
            raise ValueError("Embedding تولید شده نامعتبر است.")
        
        if not all(isinstance(x, (int, float)) for x in embedding_list):
            raise ValueError("Embedding حاوی مقادیر غیرعددی است.")
        
        logger.info(f"✅ Embedding generated successfully. Length: {len(embedding_list)}")
        return embedding_list

    except Exception as e:
        logger.error(f"❌ Error in get_embedding: {str(e)} | Input: '{text}'")
        raise ValueError(f"خطا در تولید Embedding: {str(e)}")