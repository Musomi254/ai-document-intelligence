from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):

    embeddings = model.encode(chunks)

    return np.array(embeddings)