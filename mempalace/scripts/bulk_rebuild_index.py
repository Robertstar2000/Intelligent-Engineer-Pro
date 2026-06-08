#!/usr/bin/env python3
"""
Bulk rebuild FAISS index for all MemPalace raw memory files.
Reads all .json files from raw/, extracts text, generates embeddings, and rebuilds the index.
"""
import json
import os
import sys
import faiss
import numpy as np
import glob
from datetime import datetime

# Add MemPalace to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "mempalace", "scripts"))
from embedding import init_embedding_model, generate_embedding, get_dimension

MEMPALACE_BASE = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace")
RAW_DIR = os.path.join(MEMPALACE_BASE, "raw")
INDEX_DIR = os.path.join(MEMPALACE_BASE, "indexes")

def extract_text(file_path):
    """Extract searchable text from a raw memory JSON file."""
    try:
        with open(file_path) as f:
            data = json.load(f)
        # Priority: raw_text field, then text, then content, then full JSON
        for key in ["raw_text", "text", "content", "value"]:
            if key in data and data[key]:
                text = data[key]
                if isinstance(text, str) and len(text.strip()) > 10:
                    return text.strip()
        # Fall back to concatenating key parts
        return json.dumps(data)[:500]
    except Exception:
        return ""

def main():
    start = datetime.now()
    print(f"[{start.strftime('%H:%M:%S')}] Starting FAISS index rebuild...")
    
    # Initialize model
    print("Loading sentence-transformers model...")
    model = init_embedding_model()
    dim = get_dimension()
    print(f"Model loaded. Embedding dimension: {dim}")
    
    # Get all raw files
    raw_files = glob.glob(os.path.join(RAW_DIR, "*.json"))
    print(f"Found {len(raw_files)} raw memory files")
    
    # Extract texts
    texts = []
    filenames = []
    skipped = 0
    for f in raw_files:
        fname = os.path.basename(f)
        text = extract_text(f)
        if text:
            texts.append(text)
            filenames.append(fname)
        else:
            skipped += 1
    
    print(f"Extracted text from {len(texts)} files, skipped {skipped}")
    
    # Generate embeddings in batches for efficiency
    batch_size = 128
    all_embeddings = []
    
    print(f"Generating embeddings in batches of {batch_size}...")
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        embeddings = generate_embedding(batch)
        all_embeddings.extend(embeddings)
        if (i // batch_size + 1) % 10 == 0 or i + batch_size >= len(texts):
            pct = min(i + batch_size, len(texts)) / len(texts) * 100
            print(f"  Processed {min(i + batch_size, len(texts))}/{len(texts)} ({pct:.1f}%)")
    
    # Convert to numpy
    all_embeddings_np = np.array(all_embeddings, dtype=np.float32)
    print(f"Generated {len(all_embeddings_np)} embeddings, shape: {all_embeddings_np.shape}")
    
    # Build new FAISS index (L2 distance for inner product search)
    print("Building FAISS index...")
    index = faiss.IndexFlatIP(dim)  # Inner Product (cosine similarity with normalized vectors)
    index.add(all_embeddings_np)
    print(f"Index built: {index.ntotal} vectors")
    
    # Build ID map
    id_map = {}
    for i, fname in enumerate(filenames):
        id_map[i] = fname
    
    # Save index and map
    os.makedirs(INDEX_DIR, exist_ok=True)
    index_path = os.path.join(INDEX_DIR, "faiss.index")
    faiss.write_index(index, index_path)
    print(f"Saved index to {index_path}")
    
    map_path = os.path.join(INDEX_DIR, "id_map.json")
    with open(map_path, "w") as f:
        json.dump(id_map, f)
    print(f"Saved ID map to {map_path}")
    
    elapsed = (datetime.now() - start).total_seconds()
    print(f"\nDone in {elapsed:.1f}s. {index.ntotal} vectors indexed.")

if __name__ == "__main__":
    main()
