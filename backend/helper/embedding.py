# import openai
# import os


# def get_embedding(question, model="text-embedding-3-small"):
#     response = openai.Embedding.create(
#         input=question,
#         model=model
#     )
#     return response.data[0].embedding




# ! pip install -U FlagEmbedding

# from FlagEmbedding import BGEM3FlagModel


# # بارگذاری مدل
# model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

# def get_embedding(question):
#     # استفاده از مدل برای تولید embedding
#     output = model.encode("what is capital of america", return_dense=True, return_sparse=True, return_colbert_vecs=True)
#     return output['dense_vecs'][0]  # بازگشت embedding





# from sentence_transformers import SentenceTransformer
# embedding.py
from FlagEmbedding import BGEM3FlagModel

# بارگذاری مدل
# model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)


# def get_embedding(question):
#     """Use the model to generate an embedding for the dynamic question."""
#     output = model.encode(question, return_dense=True, return_sparse=True, return_colbert_vecs=True)
#     return output

    # return output['dense_vecs'][0]  # بازگشت embedding
    # return output['colbert_vecs'][0]  # بازگش
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('BAAI/bge-m3')

def get_embedding(text):
    """Generate embedding for the text using BAAI/bge-m3."""
    if not text.strip():
        raise ValueError("Input text is empty")
    embedding = embedding_model.encode(text, normalize_embeddings=True)
    return embedding  # Should return a NumPy array