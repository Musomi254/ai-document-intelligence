import faiss
import numpy as np
import pickle
from pathlib import Path

VECTOR_DIR = Path("storage/vectorstore")
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = VECTOR_DIR / "faiss.index"
CHUNKS_PATH = VECTOR_DIR / "chunks.pkl"

dimension = 384

index = faiss.IndexFlatL2(dimension)

document_chunks = []


def store_embeddings(chunks, embeddings):

    global document_chunks

    index.add(embeddings.astype(np.float32))

    document_chunks.extend(chunks)

    faiss.write_index(index, str(INDEX_PATH))

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(document_chunks, f)


def search_similar_chunks(query_embedding, top_k=3):

    distances, indices = index.search(
        query_embedding.astype(np.float32),
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(document_chunks):
            results.append(document_chunks[idx])

    return results