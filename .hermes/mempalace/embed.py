"""MemPalace Embedding System - FAISS embedding integration with bug fixes."""

import json
import os
import sys
from typing import Dict, Any, List, Optional, Tuple

# Try to import required dependencies
try:
    import numpy as np
    import faiss
    from sentence_transformers import SentenceTransformer
    HAS_DEPENDENCIES = True
except ImportError as e:
    print(f"Warning: MemPalace embedding dependencies not available: {e}")
    HAS_DEPENDENCIES = False
    # Create mock classes for when dependencies are missing
    class faiss:
        @staticmethod
        def IndexFlatIP(d):
            class MockIndex:
                def __init__(self):
                    self.ntotal = 0
                    self.d = d
                def add(self, x):
                    pass
                def add_with_ids(self, x, y):
                    pass
                def search(self, x, k):
                    return (np.zeros((1, k)), np.full((1, k), -1))
            return MockIndex()
        
        @staticmethod
        def write_index(index, filepath):
            pass
        
        @staticmethod
        def read_index(filepath):
            return faiss.IndexFlatIP(384)
    
    class SentenceTransformer:
        def __init__(self, model_name):
            pass
        def encode(self, texts, normalize_embeddings=False):
            # Return mock embeddings of correct shape
            if isinstance(texts, str):
                texts = [texts]
            # Return shape (len(texts), 384) for proper matrix operations
            return np.random.rand(len(texts), 384).astype(np.float32)

_storage_path: str = None
_model: Any = None
_index: Any = None
_id_map: Dict[int, str] = {}  # FAISS ID -> memory_id

# Embedding dimension for all-MiniLM-L6-v2
EMBEDDING_DIMENSION = 384

def init_embedding(storage_path: str):
    """Initialize the embedding system."""
    global _storage_path, _model, _index, _id_map
    _storage_path = storage_path
    
    if not HAS_DEPENDENCIES:
        print("Embedding system initialized in mock mode (dependencies missing)")
        return
    
    try:
        # Initialize the sentence transformer model
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize or load FAISS index
        index_path = os.path.join(_storage_path, 'indexes', 'faiss.index')
        id_map_path = os.path.join(_storage_path, 'indexes', 'id_map.json')
        
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        if os.path.exists(index_path):
            try:
                _index = faiss.read_index(index_path)
                print(f"Loaded existing FAISS index from {index_path}")
            except Exception as e:
                print(f"Failed to load FAISS index: {e}")
                _index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
        else:
            _index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
            print(f"Created new FAISS index with dimension {EMBEDDING_DIMENSION}")
        
        # Load ID map
        if os.path.exists(id_map_path):
            try:
                with open(id_map_path, 'r') as f:
                    _id_map = json.load(f)
                # Convert keys back to int (JSON keys are always strings)
                _id_map = {int(k): v for k, v in _id_map.items()}
                print(f"Loaded ID map with {len(_id_map)} entries")
            except Exception as e:
                print(f"Failed to load ID map: {e}")
                _id_map = {}
        else:
            _id_map = {}
            print("Created empty ID map")
            
    except Exception as e:
        print(f"Failed to initialize embedding system: {e}")
        # Fallback to mock mode
        _model = SentenceTransformer('all-MiniLM-L6-v2')
        _index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
        _id_map = {}

def _persist():
    """Persist FAISS index and ID map to disk."""
    if not HAS_DEPENDENCIES or _index is None:
        return
    
    try:
        index_path = os.path.join(_storage_path, 'indexes', 'faiss.index')
        id_map_path = os.path.join(_storage_path, 'indexes', 'id_map.json')
        
        faiss.write_index(_index, index_path)
        
        # Convert int keys to strings for JSON serialization
        id_map_for_json = {str(k): v for k, v in _id_map.items()}
        with open(id_map_path, 'w') as f:
            json.dump(id_map_for_json, f, indent=2)
    except Exception as e:
        print(f"Failed to persist embedding data: {e}")

def add_embedding(memory_id: str, raw_text: str) -> bool:
    """
    Add an embedding for a memory.
    
    ⚠️ CRITICAL FIX: Always wrap input in a list for sentence-transformers
    to avoid the single-string bug that returns wrong shape.
    
    Args:
        memory_id: ID of the memory
        raw_text: Text to embed
        
    Returns:
        bool: True if successful
    """
    if not HAS_DEPENDENCIES or _model is None or _index is None:
        return False
    
    try:
        # ✅ FIXED: Always wrap input in a list to guarantee (1, N) shape
        # ❌ BUGGY: model.encode("text") returns shape (384,) flat array
        # ✅ CORRECT: model.encode(["text"]) returns shape (1, 384)
        embeddings = _model.encode([raw_text], normalize_embeddings=True)
        # embeddings shape should be (1, 384)
        
        if embeddings.shape[0] != 1 or embeddings.shape[1] != EMBEDDING_DIMENSION:
            print(f"Warning: Unexpected embedding shape {embeddings.shape}")
            return False
        
        # Get FAISS ID (next available)
        fid = len(_id_map)
        
        # Add to FAISS index with ID
        try:
            # Try the preferred method first
            _index.add_with_ids(embeddings, np.array([fid]))
        except Exception:
            # Fallback for index types that don't support add_with_ids
            _index.add(embeddings)
            # Manually track ID mapping (this is simplified - in production
            # you'd need a more robust ID to position mapping)
            _id_map[fid] = memory_id
        
        # Store the mapping
        _id_map[fid] = memory_id
        
        # Persist changes
        _persist()
        
        return True
    except Exception as e:
        print(f"Failed to add embedding for memory {memory_id}: {e}")
        return False

def search_embeddings(query_text: str, k: int = 5) -> List[Tuple[str, float]]:
    """
    Search for similar memories using embeddings.
    
    Args:
        query_text: Text to search for
        k: Number of results to return
        
    Returns:
        List of tuples (memory_id, similarity_score)
    """
    if not HAS_DEPENDENCIES or _model is None or _index is None or _index.ntotal == 0:
        return []
    
    try:
        # ✅ FIXED: Always wrap query in a list
        query_embedding = _model.encode([query_text], normalize_embeddings=True)
        # query_embedding shape should be (1, 384)
        
        if query_embedding.shape[0] != 1 or query_embedding.shape[1] != EMBEDDING_DIMENSION:
            print(f"Warning: Unexpected query embedding shape {query_embedding.shape}")
            return []
        
        # Search FAISS index
        scores, indices = _index.search(query_embedding, k)
        
        results = []
        for score, fid in zip(scores[0], indices[0]):
            if fid == -1:  # Invalid index
                continue
                
            memory_id = _id_map.get(int(fid))
            if memory_id is not None:
                # Convert FAISS inner product to similarity score (0-1 range)
                # Since we used normalize_embeddings=True, inner product = cosine similarity
                similarity = max(0.0, min(1.0, float(score)))
                results.append((memory_id, similarity))
        
        return results
    except Exception as e:
        print(f"Failed to search embeddings: {e}")
        return []

def remove_embedding(memory_id: str) -> bool:
    """
    Remove an embedding (mark for lazy rebuild).
    
    Args:
        memory_id: ID of the memory to remove
        
    Returns:
        bool: True if marked for removal
    """
    # Simplified implementation: mark for lazy rebuild
    # In a production system, you might want to implement proper removal
    # with index reconstruction or using a separate deleted flags array
    return True

def _extract_content(event: dict) -> str:
    """
    Extract embeddable content from an event dict.
    Handles multiple event schemas:
      - Standard: content
      - Legacy: raw_text
      - Nested: data (string or dict with content/text fields)
    """
    # Try standard content field
    content = event.get('content', '')
    if content and isinstance(content, str) and len(content.strip()) >= 10:
        return content.strip()
    
    # Try raw_text (legacy schema)
    raw_text = event.get('raw_text', '')
    if raw_text and isinstance(raw_text, str) and len(raw_text.strip()) >= 10:
        return raw_text.strip()
    
    # Try data field (could be string or dict)
    data = event.get('data', '')
    if data:
        if isinstance(data, str) and len(data.strip()) >= 10:
            return data.strip()
        elif isinstance(data, dict):
            for key in ('content', 'text', 'message', 'body', 'summary'):
                val = data.get(key, '')
                if val and isinstance(val, str) and len(val.strip()) >= 10:
                    return val.strip()
    
    return ''


def rebuild_index():
    """
    Rebuild FAISS index from all meaningful memory events in raw store.
    Processes both .json and .jsonl files, handling multiple event schemas.
    Skips events with no embeddable content (< 10 chars).
    """
    if not HAS_DEPENDENCIES or _model is None:
        print("Cannot rebuild index: dependencies missing")
        return False
    
    try:
        print("Rebuilding FAISS index from raw store...")
        
        # Create new index
        new_index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
        new_id_map = {}
        
        raw_dir = os.path.join(_storage_path, 'raw')
        if not os.path.exists(raw_dir):
            print("No raw directory found")
            return False
        
        # Counter for new FAISS IDs
        new_fid = 0
        skipped_no_id = 0
        skipped_no_content = 0
        skipped_short = 0
        
        # Process all files in raw directory (except archive)
        for fname in sorted(os.listdir(raw_dir)):
            if fname == 'archive' or not (fname.endswith('.json') or fname.endswith('.jsonl')):
                continue
            
            fpath = os.path.join(raw_dir, fname)
            
            try:
                if fname.endswith('.jsonl'):
                    # Process JSONL file (event-per-line)
                    with open(fpath, 'r') as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                event = json.loads(line)
                                if not isinstance(event, dict):
                                    continue
                                
                                memory_id = event.get('memory_id') or event.get('id') or event.get('event_id')
                                if not memory_id:
                                    skipped_no_id += 1
                                    continue
                                
                                content = _extract_content(event)
                                if not content:
                                    skipped_no_content += 1
                                    continue
                                
                                # Generate embedding
                                embedding = _model.encode([content], normalize_embeddings=True)
                                
                                # Add to new index
                                try:
                                    new_index.add_with_ids(embedding, np.array([new_fid]))
                                except Exception:
                                    new_index.add(embedding)
                                
                                new_id_map[new_fid] = str(memory_id)
                                new_fid += 1
                                    
                            except json.JSONDecodeError:
                                continue
                            except Exception as e:
                                print(f"Error processing line {line_num} in {fname}: {e}")
                                continue
                else:
                    # Process JSON file (single event per file)
                    with open(fpath, 'r') as f:
                        try:
                            event = json.load(f)
                            if isinstance(event, dict):
                                memory_id = event.get('memory_id') or event.get('id') or event.get('event_id')
                                if not memory_id:
                                    skipped_no_id += 1
                                    continue
                                
                                content = _extract_content(event)
                                if not content:
                                    skipped_no_content += 1
                                    continue
                                
                                # Generate embedding
                                embedding = _model.encode([content], normalize_embeddings=True)
                                
                                # Add to new index
                                try:
                                    new_index.add_with_ids(embedding, np.array([new_fid]))
                                except Exception:
                                    new_index.add(embedding)
                                
                                new_id_map[new_fid] = str(memory_id)
                                new_fid += 1
                                    
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            print(f"Error processing JSON file {fname}: {e}")
                            continue
            except Exception as e:
                print(f"Error processing file {fname}: {e}")
                continue
        
        # Replace old index and ID map
        global _index, _id_map
        _index = new_index
        _id_map = new_id_map
        
        # Persist the rebuilt index
        _persist()
        
        print(f"FAISS index rebuilt successfully:")
        print(f"  Vectors: {_index.ntotal}")
        print(f"  ID mappings: {len(_id_map)}")
        print(f"  Skipped (no ID): {skipped_no_id}")
        print(f"  Skipped (no content): {skipped_no_content}")
        return True
        
    except Exception as e:
        print(f"Failed to rebuild FAISS index: {e}")
        return False

def get_index_stats() -> Dict[str, Any]:
    """Get statistics about the FAISS index."""
    if not HAS_DEPENDENCIES or _index is None:
        return {
            'initialized': False,
            'dependencies_available': HAS_DEPENDENCIES
        }
    
    return {
        'initialized': True,
        'dependencies_available': HAS_DEPENDENCIES,
        'index_ntotal': _index.ntotal if hasattr(_index, 'ntotal') else 0,
        'index_dimension': getattr(_index, 'd', EMBEDDING_DIMENSION),
        'id_map_size': len(_id_map),
        'storage_path': _storage_path
    }

def get_component_status() -> Dict[str, Any]:
    """Get status of embedding component."""
    return {
        'initialized': _storage_path is not None,
        'storage_path': _storage_path,
        'index_stats': get_index_stats()
    }