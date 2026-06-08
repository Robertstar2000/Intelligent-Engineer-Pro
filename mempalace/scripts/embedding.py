"""
Embedding generation module for MemPalace
"""
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = None
model_name = "sentence-transformers/all-MiniLM-L6-v2"
dimension = 384


def init_embedding_model():
    """Initialize the embedding model."""
    global model
    if model is None:
        print(f"Loading embedding model: {model_name}")
        model = SentenceTransformer(model_name)
    return model

def generate_embedding(texts):
    """Generate embeddings for one or more texts."""
    if model is None:
        init_embedding_model()
    
    # Always pass list to model.encode to get consistent (N, 384) shape
    if isinstance(texts, str):
        texts = [texts]
    
    # Encode the texts
    embeddings = model.encode(texts, normalize_embeddings=True)
    
    # Return as list if input was list, or single array if single text
    if len(embeddings.shape) == 1:
        return embeddings.tolist()
    else:
        return [emb.tolist() for emb in embeddings]

def get_dimension():
    """Get the embedding dimension."""
    return dimension
