from sklearn.feature_extraction.text import TfidfVectorizer


vectorizer = TfidfVectorizer(stop_words="english")
_is_fitted = False


def get_embeddings(text_chunks):
    """Fit the vectorizer on document chunks and return dense embeddings."""
    global _is_fitted

    if not text_chunks:
        raise ValueError("Cannot create embeddings from an empty document.")

    embeddings = vectorizer.fit_transform(text_chunks).toarray()
    _is_fitted = True
    return embeddings


def get_query_embedding(query):
    """Return a query embedding using the already-fitted document vocabulary."""
    if not _is_fitted:
        raise ValueError("PDF context is not loaded yet.")

    return vectorizer.transform([query]).toarray()
