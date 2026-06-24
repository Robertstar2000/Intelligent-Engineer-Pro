"""MemPalace Consolidation System - Memory promotion to semantic/episodic/procedural stores."""

import json
import os
import shutil
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
import sys

# Add the mempalace directory to path for imports
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

try:
    from capture import get_raw_event_count
    from tag import extract_context_tags, get_palace_tags, save_context_tags
    from score import score_memory
except ImportError as e:
    print(f"Warning: Could not import MemPalace modules: {e}")
    # Define fallback functions
    def get_raw_event_count(): return 0
    def extract_context_tags(content, event_type=None): return []
    def get_palace_tags(context_tags): return []
    def save_context_tags(event_id, tags): pass
    def score_memory(event, weights=None): return 0.5, {}

_storage_path: str = None

# Consolidation threshold - memories scoring above this are promoted
CONSOLIDATION_THRESHOLD = 0.6

def init_consolidation(storage_path: str):
    """Initialize the consolidation system."""
    global _storage_path
    _storage_path = storage_path
    
    # Create consolidated store directories
    for store in ['semantic', 'episodic', 'procedural']:
        store_dir = os.path.join(_storage_path, store)
        os.makedirs(store_dir, exist_ok=True)
    
    print(f"Consolidation system initialized at {_storage_path}")

def should_consolidate_memory(event: Dict[Any, Any], score: float) -> bool:
    """
    Determine if a memory should be consolidated based on score and content.
    
    Args:
        event: Event dictionary
        score: Composite memory score
        
    Returns:
        bool: True if memory should be consolidated
    """
    # Check explicit skip flag
    if event.get('skip_consolidation', False):
        return False
    
    # Check threshold
    if score < CONSOLIDATION_THRESHOLD:
        return False
    
    # Additional checks could go here (e.g., duplicate detection)
    return True

def determine_store_type(event: Dict[Any, Any], score: float, individual_scores: Dict[str, float]) -> str:
    """
    Determine which consolidated store to use based on event characteristics.
    
    Args:
        event: Event dictionary
        score: Composite memory score
        individual_scores: Individual component scores
        
    Returns:
        str: Store type ('semantic', 'episodic', or 'procedural')
    """
    event_type = event.get('type', '').lower()
    content = event.get('content', '').lower()
    
    # Procedural memories: skills, habits, procedures, how-to knowledge
    procedural_indicators = [
        'how to', 'procedure', 'process', 'method', 'technique', 'skill',
        'habit', 'routine', 'step by step', 'tutorial', 'guide', 'algorithm'
    ]
    if any(indicator in content for indicator in procedural_indicators):
        return 'procedural'
    
    # Episodic memories: specific events, experiences, personal episodes
    episodic_indicators = [
        'i ', 'me ', 'my ', 'personal', 'experience', 'happened', 'occurred',
        'event', 'incident', 'episode', 'memory of', 'remember when'
    ]
    if any(indicator in content for indicator in episodic_indicators) or \
       event_type in ['user_interaction', 'personal_experience', 'episode']:
        return 'episodic'
    
    # Default to semantic for facts, concepts, general knowledge
    return 'semantic'

def consolidate_memory(event: Dict[Any, Any]) -> Optional[str]:
    """
    Consolidate a memory to the appropriate store.
    
    Args:
        event: Event dictionary to consolidate
        
    Returns:
        str: New memory ID if consolidated, None if not
    """
    if _storage_path is None:
        raise RuntimeError("Consolidation system not initialized. Call init_consolidation() first.")
    
    # Score the memory
    composite_score, individual_scores = score_memory(event)
    
    # Check if should consolidate
    if not should_consolidate_memory(event, composite_score):
        return None
    
    # Determine store type
    store_type = determine_store_type(event, composite_score, individual_scores)
    
    # Generate memory ID
    timestamp = datetime.now(timezone.utc).isoformat()
    content_str = json.dumps(event, sort_keys=True)
    memory_id = f"mem_{hash(content_str)}_{int(datetime.now(timezone.utc).timestamp())}"
    
    # Prepare consolidated memory record
    consolidated_memory = {
        **event,
        'memory_id': memory_id,
        'consolidated_at': timestamp,
        'consolidation_score': composite_score,
        'individual_scores': individual_scores,
        'store_type': store_type,
        'storage_version': '1.1.0'
    }
    
    # Extract and save tags
    context_tags = extract_context_tags(
        event.get('content', ''), 
        event.get('type')
    )
    palace_tags = get_palace_tags(context_tags)
    consolidated_memory['context_tags'] = context_tags
    consolidated_memory['palace_tags'] = palace_tags
    save_context_tags(memory_id, context_tags)
    
    # Store in appropriate directory
    store_dir = os.path.join(_storage_path, store_type)
    memory_file = os.path.join(store_dir, f'{memory_id}.json')
    
    with open(memory_file, 'w') as f:
        json.dump(consolidated_memory, f, indent=2)
    
    return memory_id

def consolidate_memories() -> int:
    """
    Consolidate memories from raw store that meet threshold.
    
    Returns:
        int: Number of memories consolidated
    """
    if _storage_path is None:
        raise RuntimeError("Consolidation system not initialized. Call init_consolidation() first.")
    
    consolidated_count = 0
    raw_dir = os.path.join(_storage_path, 'raw')
    
    if not os.path.exists(raw_dir):
        return 0
    
    # Process all raw event files
    for fname in os.listdir(raw_dir):
        if not fname.endswith('.jsonl'):
            continue
        
        fpath = os.path.join(raw_dir, fname)
        try:
            with open(fpath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        event = json.loads(line)
                        # Skip if not a dict (handle legacy artifacts)
                        if not isinstance(event, dict):
                            continue
                            
                        # Attempt consolidation
                        memory_id = consolidate_memory(event)
                        if memory_id:
                            consolidated_count += 1
                            
                    except json.JSONDecodeError:
                        # Skip invalid JSON lines
                        continue
                    except Exception as e:
                        # Log error but continue processing
                        print(f"Error processing event in {fname}:{line_num}: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error reading raw file {fname}: {e}")
            continue
    
    return consolidated_count

def get_consolidation_stats() -> Dict[str, Any]:
    """Get statistics about consolidated memories."""
    if _storage_path is None:
        return {}
    
    stats = {}
    for store_type in ['semantic', 'episodic', 'procedural']:
        store_dir = os.path.join(_storage_path, store_type)
        if os.path.exists(store_dir):
            count = len([f for f in os.listdir(store_dir) if f.endswith('.json')])
            stats[store_type] = count
        else:
            stats[store_type] = 0
    
    return stats

def get_component_status() -> Dict[str, Any]:
    """Get status of consolidation component."""
    return {
        'initialized': _storage_path is not None,
        'storage_path': _storage_path,
        'consolidation_threshold': CONSOLIDATION_THRESHOLD,
        'stats': get_consolidation_stats()
    }