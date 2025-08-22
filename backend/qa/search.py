from documents.models import DocumentChunk
import numpy as np


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve_relevant_chunks(query_embedding, top_k=3):
    """Retrieve top_k most relevant chunks based on cosine similarity."""
    all_chunks = DocumentChunk.objects.all()
    scored_chunks = []

    for chunk in all_chunks:
        score = cosine_similarity(query_embedding, chunk.embedding)
        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    return [chunk for _, chunk in scored_chunks[:top_k]]