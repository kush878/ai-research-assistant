import faiss
import numpy as np


def create_faiss_index(embeddings):
    embeddings = np.asarray(embeddings, dtype="float32")

    if embeddings.ndim != 2 or embeddings.shape[0] == 0:
        raise ValueError("Embeddings must be a non-empty 2D array.")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)
    
    return index


def search_index(index, query_embedding, k=5):
    query_embedding = np.asarray(query_embedding, dtype="float32")
    k = min(k, index.ntotal)

    if k <= 0:
        return []

    _, I = index.search(query_embedding, k)
    return I[0]
