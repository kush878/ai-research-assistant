from pdf_loader import load_pdf
from embeddings import get_embeddings, model
from vector_store import create_faiss_index, search_index
import re


# ---------------- SMART TEXT SPLITTER ----------------
def split_text(text, chunk_size=1500, overlap=250):
    # Clean text
    text = text.replace("\n", " ")
    text = re.sub(r'\s+', ' ', text)

    # Split by sentence
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "

        else:
            chunks.append(current_chunk.strip())

            # overlap keeps last words for context
            current_chunk = current_chunk[-overlap:] + sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# ---------------- PROCESS PDF ----------------
def process_pdf(file):
    text = load_pdf(file)

    # Bigger smarter chunks
    chunks = split_text(text, chunk_size=1500, overlap=250)

    embeddings = get_embeddings(chunks)

    index = create_faiss_index(embeddings)

    return index, chunks


# ---------------- SEARCH BEST CHUNKS ----------------
def get_relevant_chunks(query, index, chunks):
    query_embedding = model.encode([query])

    indices = search_index(index, query_embedding)

    return [chunks[i] for i in indices if i < len(chunks)]