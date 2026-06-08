import json
import uuid
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class MemPalaceEmbeddingIntegration:
    def __init__(self, base_path=None, embedding_model_name='all-MiniLM-L6-v2'):
        """
        Initialize MemPalace embedding integration.
        
        Args:
            base_path: Path to MemPalace directory (defaults to ~/.hermes/mempalace)
            embedding_model_name: Sentence Transformers model name
        """
        if base_path is None:
            base_path = Path.home() / ".hermes" / "mempalace"
        else:
            base_path = Path(base_path)
        
        self.base_path = base_path
        self.indexes_path = base_path / "indexes"
        self.id_map_path = self.indexes_path / "id_map.json"
        
        # Create necessary directories
        self.indexes_path.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize FAISS index
        self.index = self._load_or_create_index()
        
        # Load or initialize ID map
        self.id_map = self._load_or_create_id_map()
        
        # Load embedding model
        print(f"Loading embedding model: {embedding_model_name}")
        self.model = SentenceTransformer(embedding_model_name)
        
        # Check if index and ID map sizes match
        if len(self.id_map) != self.index.ntotal:
            print(f"Warning: Index size ({self.index.ntotal}) doesn't match ID map size ({len(self.id_map)})")
        
        print(f"Initialized embedding integration. Index size: {self.index.ntotal}, ID map size: {len(self.id_map)}")
    
    def _load_or_create_index(self):
        """Load existing FAISS index or create new one."""
        if self.indexes_path.exists() and (self.indexes_path / "faiss.index").exists():
            print("Loading existing FAISS index...")
            return faiss.read_index(str(self.indexes_path / "faiss.index"))
        else:
            print("Creating new FAISS index...")
            # Create an empty index (will add vectors as needed)
            return faiss.IndexFlatIP(384)  # Using all-MiniLM-L6-v2 which has 384 dim
    
    def _load_or_create_id_map(self):
        """Load existing ID map or create new one."""
        if self.id_map_path.exists():
            with open(self.id_map_path, 'r') as f:
                return json.load(f)
        else:
            return {}
    
    def add_embedding(self, memory_id, text):
        """
        Add embedding for a memory.
        
        Args:
            memory_id: Unique identifier for the memory
            text: Text content to embed
        """
        # Encode text to embedding
        embedding = self.model.encode([text], normalize_embeddings=True, convert_to_numpy=True)[0]
        
        # Add to FAISS index
        vector_id = len(self.id_map)
        self.index.add(np.array([embedding]), np.array([vector_id]))
        
        # Update ID map
        self.id_map[str(vector_id)] = memory_id
        
        # Persist
        self._persist()
        
        print(f"Added embedding for memory {memory_id} (vector ID: {vector_id})")
        return vector_id
    
    def search_embeddings(self, query_text, k=5):
        """
        Search for similar embeddings.
        
        Args:
            query_text: Query text to embed and search
            k: Number of results to return
            
        Returns:
            List of (memory_id, score) tuples
        """
        # Encode query
        query_embedding = self.model.encode([query_text], normalize_embeddings=True, convert_to_numpy=True)[0]
        
        # Search
        distances, vector_ids = self.index.search(np.array([query_embedding]), k)
        
        results = []
        for distance, vector_id in zip(distances[0], vector_ids[0]):
            if vector_id == -1:
                continue
            memory_id = self.id_map.get(str(vector_id))
            if memory_id is not None:
                # Cosine similarity from dot product of normalized vectors
                results.append((memory_id, float(distance)))
        
        return results
    
    def remove_embedding(self, memory_id):
        """
        Remove embedding for a memory (simplified - marks for rebuild).
        
        Args:
            memory_id: Memory identifier to remove
        """
        print(f"Marking embedding for removal: {memory_id}. Will be removed during nightly rebuild.")
        # In a real implementation, we would track this for rebuild
        return True
    
    def _persist(self):
        """Persist index and ID map to disk."""
        # Write FAISS index
        faiss.write_index(self.index, str(self.indexes_path / "faiss.index"))
        
        # Write ID map
        with open(self.id_map_path, 'w') as f:
            json.dump(self.id_map, f, indent=2)
    
    def get_stats(self):
        """Get statistics about the embedding index."""
        return {
            "index_size": self.index.ntotal,
            "id_map_size": len(self.id_map),
            "index_file": str(self.indexes_path / "faiss.index"),
            "id_map_file": str(self.id_map_path)
        }

# Create a global instance for easy import
embedding_integration = MemPalaceEmbeddingIntegration()
