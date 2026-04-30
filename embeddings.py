from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()

def get_embeddings(texts):
    return vectorizer.fit_transform(texts).toarray()

model = None
def get_embeddings(text_chunks):
    return model.encode(text_chunks)