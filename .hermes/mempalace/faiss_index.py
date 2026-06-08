"""
FAISS index management for MemPalace embedding integration.
Handles embedding generation, storage, and similarity search.
"""
import json
import os
import numpy as np

# Try to import faiss, handle if not available
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("Warning: FAISS not available. Embedding search will be disabled.")

# Try to import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available. Embedding search will be disabled.")

# Global variables for FAISS index and ID mapping
_index = None
_id_map = {}
_model = None
_storage_path = None

def _get_storage_path():
    """Get the MemPalace storage path."""
    global _storage_path
    if _storage_path is None:
        _storage_path = os.path.expanduser('~/.hermes/mempalace')
    return _storage_path

def init_faiss():
    """Initialize FAISS index and load existing data if available."""
    global _index, _id_map, _model, _storage_path
    
    if not FAISS_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("FAISS or sentence-transformers not available. Skipping FAISS initialization.")
        return
    
    _storage_path = _get_storage_path()
    index_path = os.path.join(_storage_path, 'indexes', 'faiss.index')
    id_map_path = os.path.join(_storage_path, 'indexes', 'id_map.json')
    
    # Initialize the sentence transformer model
    try:
        _model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimension
        print(f"Loaded sentence-transformers model: all-MiniLM-L6-v2")
    except Exception as e:
        print(f"Failed to load sentence-transformers model: {e}")
        _model = None
        return
    
    # Load existing FAISS index if available
    if os.path.exists(index_path):
        try:
            _index = faiss.read_index(index_path)
            print(f"Loaded existing FAISS index from {index_path}")
        except Exception as e:
            print(f"Failed to load FAISS index: {e}")
            _index = None
    else:
        # Create new index - get dimension from the embedding model
        if _model is not None:
            # Get embedding dimension by encoding a test string
            test_emb = _model.encode(["test"], normalize_embeddings=True)
            dimension = test_emb.shape[1]
            print(f"Embedding dimension: {dimension}")
        else:
            dimension = 384  # Default fallback
        
        try:
            # Try to create an index that supports add_with_ids
            # IndexFlatIP may not support add_with_ids in all FAISS versions
            # We'll try IndexIVFFlat which generally does, but requires training
            # For simplicity, we'll use IndexFlatIP and handle add_with_ids fallback
            _index = faiss.IndexFlatIP(dimension)
            print(f"Created new FAISS index with dimension {dimension} (IndexFlatIP)")
        except Exception as e:
            print(f"Failed to create FAISS index: {e}")
            _index = None
            return
    
    # Load ID map if available
    if os.path.exists(id_map_path):
        try:
            with open(id_map_path, 'r') as f:
                _id_map = json.load(f)
            # Convert keys to integers for consistency
            _id_map = {int(k): v for k, v in _id_map.items()}
            print(f"Loaded ID map with {len(_id_map)} entries")
        except Exception as e:
            print(f"Failed to load ID map: {e}")
            _id_map = {}
    else:
        _id_map = {}
        print("Created empty ID map")

def add_embedding(memory_id, raw_text):
    """
    Add an embedding for a memory to the FAISS index.
    
    Args:
        memory_id (str): The unique ID of the memory.
        raw_text (str): The raw text content to embed.
    """
    global _index, _id_map, _model
    
    if not FAISS_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE or _model is None or _index is None:
        print("FAISS not properly initialized. Skipping embedding addition.")
        return
    
    # CRITICAL: Always pass text as a list to avoid the sentence-transformers bug
    # model.encode("text") returns shape (384,) -> flat array
    # model.encode(["text"]) returns shape (1, 384) -> proper 2D array
    try:
        emb = _model.encode([raw_text], normalize_embeddings=True)[0]
        # emb should now be a 1D array of shape (dimension,)
        fid = len(_id_map)
        
        # Try to use add_with_ids, fallback to add() + manual ID tracking if needed
        try:
            _index.add_with_ids(np.array([emb]), np.array([fid]))
        except Exception as e:
            # Fallback: use add() and maintain our own ID mapping separately
            # We'll store the mapping from FAISS internal ID to memory ID in _id_map
            # But we need to know what FAISS internal ID was assigned
            # For IndexFlatIP, add() assigns sequential IDs starting from current ntotal
            faiss_id = _index.ntotal
            _index.add(np.array([emb]))
            _id_map[faiss_id] = memory_id
            # Note: We're using FAISS internal ID as key, not our sequential fid
            # This is okay as long as we're consistent
            print(f"Used fallback add() method for FAISS (assigned ID {faiss_id})")
            return
        
        # Only update _id_map if add_with_ids succeeded
        _id_map[fid] = memory_id
        
        # Persist the changes
        _persist()
        
    except Exception as e:
        print(f"Failed to add embedding for memory {memory_id}: {e}")

def search_embeddings(query_text, k=5):
    """
    Search the FAISS index for similar embeddings.
    
    Args:
        query_text (str): The query text to search for.
        k (int): Number of results to return.
    
    Returns:
        list: List of tuples (memory_id, score) sorted by score descending.
    """
    global _index, _id_map, _model
    
    if not FAISS_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE or _model is None or _index is None:
        return []
    
    if _index.ntotal == 0:
        return []
    
    try:
        # CRITICAL: Always pass query as a list
        q_emb = _model.encode([query_text], normalize_embeddings=True)[0]
        D, I = _index.search(np.array([q_emb]), k)
        
        results = []
        for score, fid in zip(D[0], I[0]):
            if fid == -1:  # FAISS returns -1 for empty slots
                continue
            
            # Get memory ID from our ID map
            # Note: We need to handle both possible ID mapping schemes
            memory_id = _id_map.get(int(fid))
            if memory_id is not None:
                results.append((memory_id, float(score)))
        
        return results
    except Exception as e:
        print(f"Failed to search embeddings: {e}")
        return []

def remove_embedding(memory_id):
    """
    Remove an embedding from the FAISS index.
    Note: This is a simplified implementation that marks for lazy rebuild.
    A production implementation might want to rebuild the index immediately
    or use a more sophisticated approach.
    
    Args:
        memory_id (str): The ID of the memory to remove.
    """
    global _id_map
    
    # Find the FAISS ID(s) associated with this memory_id
    # Since we might have used either scheme, we need to check both
    fid_to_remove = None
    for fid, mid in _id_map.items():
        if mid == memory_id:
            fid_to_remove = fid
            break
    
    if fid_to_remove is not None:
        # Remove from ID map
        del _id_map[fid_to_remove]
        # In a full implementation, we would also remove from the index
        # For now, we mark for lazy rebuild (could be done nightly)
        print(f"Marked memory {memory_id} for removal from FAISS index (lazy rebuild)")
        # We could persist the ID map now, but the index still contains the vector
        # For simplicity, we'll just update the ID map and rely on nightly rebuild
        _persist_id_map()
    else:
        print(f"Warning: Could not find memory ID {memory_id} in FAISS ID map")

def _persist():
    """Persist both FAISS index and ID map to disk."""
    _persist_index()
    _persist_id_map()

def _persist_index():
    """Persist FAISS index to disk."""
    global _index, _storage_path
    if _index is not None:
        try:
            index_path = os.path.join(_storage_path, 'indexes', 'faiss.index')
            faiss.write_index(_index, index_path)
            print(f"Persisted FAISS index to {index_path}")
        except Exception as e:
            print(f"Failed to persist FAISS index: {e}")

def _persist_id_map():
    """Persist ID map to disk."""
    global _id_map, _storage_path
    if _storage_path is not None:
        try:
            id_map_path = os.path.join(_storage_path, 'indexes', 'id_map.json')
            # Convert keys to strings for JSON serialization
            id_map_to_save = {str(k): v for k, v in _id_map.items()}
            with open(id_map_path, 'w') as f:
                json.dump(id_map_to_save, f, indent=2)
            print(f"Persisted ID map to {id_map_path}")
        except Exception as e:
            print(f"Failed to persist ID map: {e}")

# Initialize on import
init_faiss()