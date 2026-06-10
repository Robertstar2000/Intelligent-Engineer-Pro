#!/usr/bin/env python3
"""
Comprehensive FAISS index rebuild for MemPalace
Handles both .json and .jsonl files in the raw directory
"""

import json
import os
import sys
import faiss
import numpy as np
import glob
from datetime import datetime

# Add MemPalace to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from embed import init_embedding, generate_embedding  # We'll need to adapt this

MEMPALACE_BASE = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace")
RAW_DIR = os.path.join(MEMPALACE_BASE, "raw")
INDEX_DIR = os.path.join(MEMPALACE_BASE, "indexes")

def init_embedding_model():
    """Initialize the sentence-transformers model"""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print(f"Loaded sentence-transformers model: all-MiniLM-L6-v2")
        return model
    except Exception as e:
        print(f"Failed to load sentence-transformers model: {e}")
        return None

def get_embedding_dimension(model):
    """Get embedding dimension by encoding a test string"""
    try:
        test_emb = model.encode(["test"], normalize_embeddings=True)
        return test_emb.shape[1]
    except Exception as e:
        print(f"Failed to get embedding dimension: {e}")
        return 384  # Default fallback

def generate_embedding(model, texts):
    """Generate embeddings for a list of texts"""
    try:
        # CRITICAL: Always pass as list to avoid sentence-transformers bug
        embeddings = model.encode(texts, normalize_embeddings=True)
        return embeddings
    except Exception as e:
        print(f"Failed to generate embeddings: {e}")
        return None

def extract_text_from_json(file_path):
    """Extract searchable text from a JSON memory file."""
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

def extract_text_from_jsonl_line(line):
    """Extract text from a single line in a JSONL file."""
    try:
        event = json.loads(line.strip())
        if isinstance(event, dict):
            # Extract content from the event data
            data = event.get('data', {})
            if isinstance(data, dict):
                content = data.get('content', '')
                if content and isinstance(content, str) and len(content.strip()) > 10:
                    return content.strip()
            # Fallback: try to get content directly from event
            content = event.get('content', '')
            if content and isinstance(content, str) and len(content.strip()) > 10:
                return content.strip()
        return ""
    except json.JSONDecodeError:
        return ""
    except Exception:
        return ""

def extract_id_from_jsonl_line(line):
    """Extract memory ID from a single line in a JSONL file."""
    try:
        event = json.loads(line.strip())
        if isinstance(event, dict):
            return event.get('id', '')
        return ""
    except json.JSONDecodeError:
        return ""
    except Exception:
        return ""

def main():
    start = datetime.now()
    print(f"[{start.strftime('%H:%M:%S')}] Starting comprehensive FAISS index rebuild...")
    
    # Initialize model
    print("Loading sentence-transformers model...")
    model = init_embedding_model()
    if model is None:
        print("ERROR: Failed to initialize embedding model")
        return 1
    
    dim = get_embedding_dimension(model)
    print(f"Model loaded. Embedding dimension: {dim}")
    
    # Get all raw files (both .json and .jsonl, excluding archive)
    json_files = glob.glob(os.path.join(RAW_DIR, "*.json"))
    jsonl_files = [f for f in glob.glob(os.path.join(RAW_DIR, "*.jsonl")) 
                   if not f.endswith('.jsonl') or '/archive/' not in f]
    
    # Filter out empty files
    json_files = [f for f in json_files if os.path.getsize(f) > 0]
    jsonl_files = [f for f in jsonl_files if os.path.getsize(f) > 0]
    
    print(f"Found {len(json_files)} JSON memory files")
    print(f"Found {len(jsonl_files)} JSONL memory files (excluding empty and archive)")
    
    # Extract texts and IDs
    texts = []
    ids = []  # To keep track of which text belongs to which ID
    skipped = 0
    
    # Process JSON files
    print("Processing JSON files...")
    for f in json_files:
        fname = os.path.basename(f)
        text = extract_text_from_json(f)
        if text:
            texts.append(text)
            # Use filename as ID for JSON files (or extract from content if possible)
            ids.append(fname)
        else:
            skipped += 1
    
    # Process JSONL files
    print("Processing JSONL files...")
    for f in jsonl_files:
        try:
            with open(f, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                    text = extract_text_from_jsonl_line(line)
                    mem_id = extract_id_from_jsonl_line(line)
                    if text and mem_id:
                        texts.append(text)
                        ids.append(mem_id)
                    elif text:  # Have text but no ID - use filename+line as fallback
                        texts.append(text)
                        ids.append(f"{os.path.basename(f)}:{line_num}")
                    else:
                        skipped += 1
        except Exception as e:
            print(f"Warning: Error processing {f}: {e}")
            skipped += 1  # Rough estimate
    
    print(f"Extracted text from {len(texts)} total entries, skipped {skipped}")
    
    if len(texts) == 0:
        print("ERROR: No text extracted from any files")
        return 1
    
    # Generate embeddings in batches for efficiency
    batch_size = 128
    all_embeddings = []
    
    print(f"Generating embeddings in batches of {batch_size}...")
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        embeddings = generate_embedding(model, batch)
        if embeddings is None:
            print(f"ERROR: Failed to generate embeddings for batch starting at {i}")
            return 1
        all_embeddings.extend(embeddings)
        if (i // batch_size + 1) % 10 == 0 or i + batch_size >= len(texts):
            pct = min(i + batch_size, len(texts)) / len(texts) * 100
            print(f"  Processed {min(i + batch_size, len(texts))}/{len(texts)} ({pct:.1f}%)")
    
    # Convert to numpy
    all_embeddings_np = np.array(all_embeddings, dtype=np.float32)
    print(f"Generated {len(all_embeddings_np)} embeddings, shape: {all_embeddings_np.shape}")
    
    # Build new FAISS index (Inner Product for cosine similarity with normalized vectors)
    print("Building FAISS index...")
    index = faiss.IndexFlatIP(dim)  # Inner Product (cosine similarity with normalized vectors)
    index.add(all_embeddings_np)
    print(f"Index built: {index.ntotal} vectors")
    
    # Build ID map (position -> memory_id)
    id_map = {}
    for i, mem_id in enumerate(ids):
        id_map[i] = mem_id
    
    # Save index and map
    os.makedirs(INDEX_DIR, exist_ok=True)
    index_path = os.path.join(INDEX_DIR, "faiss.index")
    faiss.write_index(index, index_path)
    print(f"Saved index to {index_path}")
    
    map_path = os.path.join(INDEX_DIR, "id_map.json")
    # Convert keys to strings for JSON serialization
    id_map_to_save = {str(k): v for k, v in id_map.items()}
    with open(map_path, "w") as f:
        json.dump(id_map_to_save, f, indent=2)
    print(f"Saved ID map to {map_path}")
    
    elapsed = (datetime.now() - start).total_seconds()
    print(f"\nDone in {elapsed:.1f}s. {index.ntotal} vectors indexed.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())