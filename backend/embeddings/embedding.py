# import openai
# import os

# openai.api_key = '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'

# def get_embedding(question, model="text-embedding-3-small"):
#     response = openai.Embedding.create(
#         input=question,
#         model=model
#     )
#     return response.data[0].embedding




# ! pip install -U FlagEmbedding

from FlagEmbedding import BGEM3FlagModel


# بارگذاری مدل
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

def get_embedding(question):
    # استفاده از مدل برای تولید embedding
    output = model.encode([question], return_dense=True, return_sparse=True, return_colbert_vecs=True)
    return output['colbert_vecs'][0]  # بازگشت embedding
