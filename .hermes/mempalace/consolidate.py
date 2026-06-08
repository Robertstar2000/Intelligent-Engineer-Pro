"""
Consolidation system for MemPalace - memory promotion to semantic/episodic/procedural
"""

import os
import json
import shutil
from datetime import datetime, timezone
import score
import tag
import capture

# Storage path - will be set by init_consolidation
_STORAGE_PATH = None

# Consolidation threshold - memories scoring above this get promoted
CONSOLIDATION_THRESHOLD = 0.6

def init_consolidation(storage_path):
    """Initialize consolidation system"""
    global _STORAGE_PATH
    _STORAGE_PATH = storage_path
    
    # Ensure consolidated directories exist
    for subdir in ['semantic', 'episodic', 'procedural']:
        os.makedirs(os.path.join(_STORAGE_PATH, subdir), exist_ok=True)

def consolidate_memories(events=None):
    """Consolidate high-scoring memories to appropriate stores"""
    if not _STORAGE_PATH:
        raise RuntimeError("Consolidation system not initialized. Call init_consolidation first.")
    
    # Load events if not provided
    if events is None:
        events = capture.load_recent_events(days=7)  # Last week
    
    # Score events
    scored_events = score.score_events(events)
    
    consolidated_count = 0
    for event in scored_events:
        score_val = event.get('mempalace_score', 0.0)
        
        # Check if above threshold
        if score_val >= CONSOLIDATION_THRESHOLD:
            # Determine memory type based on context tags
            context_tags = event.get('context_tags', [])
            
            # Simple heuristic for memory type assignment
            memory_type = 'semantic'  # Default
            if any(tag in ['personal', 'health', 'family', 'friends'] for tag in context_tags):
                memory_type = 'episodic'
            elif any(tag in ['technical', 'code', 'programming', 'algorithm'] for tag in context_tags):
                memory_type = 'procedural'
            
            # Store in appropriate consolidated store
            store_dir = os.path.join(_STORAGE_PATH, memory_type)
            
            # Generate unique filename
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
            event_id = event.get('id', 'unknown')[:8]
            filename = f"{timestamp}_{event_id}.json"
            filepath = os.path.join(store_dir, filename)
            
            # Prepare consolidated memory
            consolidated_memory = {
                'id': event.get('id'),
                'timestamp': event.get('timestamp'),
                'original_data': event.get('data'),
                'context_tags': event.get('context_tags', []),
                'palace_tags': event.get('palace_tags', []),
                'mempalace_score': score_val,
                'consolidation_timestamp': datetime.now(timezone.utc).isoformat(),
                'summary': _generate_summary(event)
            }
            
            try:
                with open(filepath, 'w') as f:
                    json.dump(consolidated_memory, f, indent=2)
                consolidated_count += 1
            except Exception as e:
                print(f"Failed to write consolidated memory: {e}")
    
    return consolidated_count

def _generate_summary(event):
    """Generate a summary text for the consolidated memory"""
    event_data = event.get('data', {})
    
    # Extract text content
    text_content = ""
    if isinstance(event_data, dict):
        for field in ['content', 'text', 'message', 'description', 'title']:
            if field in event_data and isinstance(event_data[field], str):
                text_content = event_data[field]
                break
    if not text_content:
        text_content = str(event_data)
    
    # Simple summary: first 200 chars + context
    summary = text_content[:200]
    if len(text_content) > 200:
        summary += "..."
    
    # Add context tags if available
    context_tags = event.get('context_tags', [])
    if context_tags:
        summary += f" [Tags: {', '.join(context_tags)}]"
    
    return summary

def load_consolidated_memories(memory_type=None, limit=100):
    """Load consolidated memories from stores"""
    if not _STORAGE_PATH:
        return []
    
    memories = []
    
    # Determine which stores to load
    stores_to_check = []
    if memory_type:
        stores_to_check = [memory_type]
    else:
        stores_to_check = ['semantic', 'episodic', 'procedural']
    
    for store in stores_to_check:
        store_dir = os.path.join(_STORAGE_PATH, store)
        if not os.path.exists(store_dir):
            continue
        
        # Get files sorted by modification time (newest first)
        try:
            files = []
            for f in os.listdir(store_dir):
                if f.endswith('.json'):
                    filepath = os.path.join(store_dir, f)
                    files.append((filepath, os.path.getmtime(filepath)))
            
            files.sort(key=lambda x: x[1], reverse=True)  # Newest first
            
            # Load memories
            for filepath, _ in files[:limit]:
                try:
                    with open(filepath, 'r') as f:
                        memory = json.load(f)
                        memories.append(memory)
                except Exception as e:
                    print(f"Error loading consolidated memory from {filepath}: {e}")
        except Exception as e:
            print(f"Error accessing store {store}: {e}")
    
    return memories