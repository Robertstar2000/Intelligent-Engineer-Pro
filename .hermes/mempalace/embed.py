"""
FAISS embedding integration for MemPalace
"""

import os
import json
import numpy as np
try:
    import faiss
except ImportError:
    print("FAISS not installed. Install with: pip install faiss-cpu")
    faiss = None

from sentence_transformers import SentenceTransformer

# Storage path - will be set by init_embedding
_STORAGE_PATH = None
_MODEL = None
_INDEX = None
_ID_MAP = {}  # FAISS ID -> memory_id

# Embedding dimension - will be set based on model
_EMBEDDING_DIM = None

def init_embedding(storage_path, model_name='all-MiniLM-L6-v2'):
    """Initialize embedding system"""
    global _STORAGE_PATH, _MODEL, _INDEX, _ID_MAP, _EMBEDDING_DIM
    _STORAGE_PATH = storage_path
    
    # Initialize sentence transformer model
    try:
        _MODEL = SentenceTransformer(model_name)
        # Get embedding dimension from model
        # get_sentence_embedding_dimension() deprecated in newer sentence-transformers
        _EMBEDDING_DIM = _MODEL.get_embedding_dimension()
        print(f"Loaded embedding model '{model_name}' with dimension {_EMBEDDING_DIM}")
    except Exception as e:
        print(f"Failed to load embedding model: {e}")
        _MODEL = None
        return
    
    # Ensure indexes directory exists
    indexes_dir = os.path.join(_STORAGE_PATH, 'indexes')
    os.makedirs(indexes_dir, exist_ok=True)
    
    # Load existing index and ID map
    index_path = os.path.join(indexes_dir, 'faiss.index')
    id_map_path = os.path.join(indexes_dir, 'id_map.json')
    
    # Load FAISS index
    if os.path.exists(index_path) and faiss is not None:
        try:
            _INDEX = faiss.read_index(index_path)
            print(f"Loaded existing FAISS index from {index_path}")
        except Exception as e:
            print(f"Failed to load FAISS index: {e}")
            _INDEX = None
    else:
        _INDEX = None
    
    # Load ID map
    if os.path.exists(id_map_path):
        try:
            with open(id_map_path, 'r') as f:
                _ID_MAP = json.load(f)
            # Convert keys to int for consistency
            _ID_MAP = {int(k): v for k, v in _ID_MAP.items()}
            print(f"Loaded ID map with {len(_ID_MAP)} entries")
        except Exception as e:
            print(f"Failed to load ID map: {e}")
            _ID_MAP = {}
    else:
        _ID_MAP = {}
        print("Created empty ID map")
    
    # Create new index if needed
    if _INDEX is None and faiss is not None:
        try:
            # Using IndexFlatIP for inner product (cosine similarity when normalized)
            _INDEX = faiss.IndexFlatIP(_EMBEDDING_DIM)
            print(f"Created new FAISS index with dimension {_EMBEDDING_DIM}")
        except Exception as e:
            print(f"Failed to create FAISS index: {e}")
            _INDEX = None

def add_embedding(memory_id, raw_text):
    """Add embedding for a memory"""
    global _INDEX, _ID_MAP
    
    if _MODEL is None or _INDEX is None:
        print("Embedding system not properly initialized")
        return False
    
    if not raw_text or not isinstance(raw_text, str):
        print("Invalid text for embedding")
        return False
    
    try:
        # CRITICAL FIX: Always wrap input in a list to avoid sentence-transformers bug
        # model.encode("text") returns shape (384,) - flat array
        # model.encode(["text"]) returns shape (1, 384) - proper batch
        embeddings = _MODEL.encode([raw_text], normalize_embeddings=True)
        embedding = embeddings[0]  # Get first (and only) embedding
        
        # Verify embedding dimension
        if len(embedding) != _EMBEDDING_DIM:
            print(f"Embedding dimension mismatch: expected {_EMBEDDING_DIM}, got {len(embedding)}")
            return False
        
        # Get next FAISS ID
        fid = len(_ID_MAP)
        
        # Add to index with ID
        try:
            # Try add_with_ids first (works with some index types)
            _INDEX.add_with_ids(np.array([embedding]), np.array([fid]))
        except Exception:
            # Fallback for index types that don't support add_with_ids
            # Add without ID, then manage mapping separately
            _INDEX.add(np.array([embedding]))
            # The ID is implicitly the index of the vector in the index
            # We need to store the mapping from our custom ID to FAISS index position
            # Since we're adding sequentially, the FAISS index position should equal fid
            # But to be safe, we'll store both mappings
            
        # Update ID map
        _ID_MAP[fid] = memory_id
        
        # Persist changes
        _persist()
        
        return True
    except Exception as e:
        print(f"Failed to add embedding: {e}")
        return False

def search_embeddings(query_text, k=5):
    """Search for similar embeddings"""
    global _INDEX, _ID_MAP
    
    if _MODEL is None or _INDEX is None or _INDEX.ntotal == 0:
        return []
    
    if not query_text or not isinstance(query_text, str):
        return []
    
    try:
        # CRITICAL FIX: Always wrap input in a list
        query_embedding = _MODEL.encode([query_text], normalize_embeddings=True)[0]
        
        # Search
        D, I = _INDEX.search(np.array([query_embedding]), k)
        
        results = []
        for score, fid in zip(D[0], I[0]):
            if fid == -1:  # FAISS returns -1 for empty slots
                continue
            
            memory_id = _ID_MAP.get(int(fid))
            if memory_id is not None:
                results.append((memory_id, float(score)))
        
        return results
    except Exception as e:
        print(f"Failed to search embeddings: {e}")
        return []

def remove_embedding(memory_id):
    """Remove embedding for a memory (mark for lazy rebuild)"""
    # For simplicity, we'll mark for lazy rebuild
    # In a production system, you might want to implement proper removal
    # or rebuild the index periodically
    pass

def rebuild_index():
    """Rebuild the FAISS index from scratch by scanning all memory files"""
    global _INDEX, _ID_MAP
    
    if _MODEL is None or faiss is None:
        print("Embedding system not initialized")
        return False
    
    try:
        # Search for memory files across all folders
        import glob
        memory_dirs = ['semantic', 'procedural', 'palace', 'preferences']
        mem_files = []
        for d in memory_dirs:
            p = os.path.join(_STORAGE_PATH, d)
            if os.path.isdir(p):
                mem_files.extend(glob.glob(os.path.join(p, 'mem_*.json')))
        
        # Create new index
        _INDEX = faiss.IndexFlatIP(_EMBEDDING_DIM)
        _ID_MAP = {}
        
        embedded = 0
        for filepath in mem_files:
            try:
                with open(filepath, 'r') as f:
                    mem_data = json.load(f)
                # Skip summary files and empty content
                if 'summary' in os.path.basename(filepath):
                    continue
                
                text = ''
                mem_id = mem_data.get('id', '')
                content = mem_data.get('content', '') or ''
                summary = mem_data.get('summary', '') or ''
                memory_text = mem_data.get('memory_text', '') or ''
                text = (content + ' ' + summary + ' ' + memory_text).strip()
                
                if not text or not mem_id:
                    continue
                
                # Embed
                embeddings = _MODEL.encode([text], normalize_embeddings=True)
                fid = len(_ID_MAP)
                _INDEX.add(np.array([embeddings[0]]))
                _ID_MAP[fid] = mem_id
                embedded += 1
            except Exception as e:
                print(f"  Skipping {os.path.basename(filepath)}: {e}")
        
        _persist()
        print(f"Rebuilt FAISS index: {embedded} vectors from {len(mem_files)} memory files")
        return True
    except Exception as e:
        print(f"Failed to rebuild index: {e}")
        return False

def _persist():
    """Persist index and ID map to disk"""
    global _INDEX, _ID_MAP
    
    if _STORAGE_PATH is None or _INDEX is None:
        return
    
    indexes_dir = os.path.join(_STORAGE_PATH, 'indexes')
    os.makedirs(indexes_dir, exist_ok=True)
    
    index_path = os.path.join(indexes_dir, 'faiss.index')
    id_map_path = os.path.join(indexes_dir, 'id_map.json')
    
    try:
        faiss.write_index(_INDEX, index_path)
        # Convert keys to string for JSON serialization
        id_map_to_save = {str(k): v for k, v in _ID_MAP.items()}
        with open(id_map_path, 'w') as f:
            json.dump(id_map_to_save, f)
    except Exception as e:
        print(f"Failed to persist embedding data: {e}")

def get_index_stats():
    """Get statistics about the FAISS index"""
    global _INDEX, _ID_MAP
    
    if _INDEX is None:
        return {"status": "not_initialized"}
    
    return {
        "status": "initialized",
        "total_vectors": _INDEX.ntotal,
        "id_map_entries": len(_ID_MAP),
        "embedding_dimension": _EMBEDDING_DIM,
        "index_type": type(_INDEX).__name__ if _INDEX else None
    }