#!/usr/bin/env python3
"""
Consolidate high-score memory events into durable memory stores.
"""
import json
import os
import sys
import uuid
from datetime import datetime, timezone
import math

def consolidate_memory(event_data, score_threshold=0.7):
    """
    Consolidate a memory event into appropriate durable store based on score and type.
    """
    score = event_data.get('score', 0.0)
    if score < score_threshold:
        return None  # Not ready for consolidation
    
    provisional_type = event_data.get('provisional_type', 'episodic')
    memory_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Determine target store
    store_map = {
        'semantic': 'semantic',
        'procedural': 'procedural',
        'preference': 'preferences',
        'episodic': 'episodic',
        'task-state': 'episodic'  # Task states go to episodic for now
    }
    
    target_store = store_map.get(provisional_type, 'episodic')
    
    # Create consolidated memory
    consolidated = {
        "memory_id": memory_id,
        "user_id": event_data.get('user_id', 'default'),
        "text": event_data.get('raw_text', ''),
        "memory_type": target_store,
        "timestamp": event_data.get('timestamp', timestamp),
        "validity_window": f"{event_data.get('timestamp', timestamp)}/2027-04-09T10:00:00Z",  # 1 year validity
        "confidence": min(0.95, score * 1.1),  # Boost confidence slightly
        "reinforcement_count": 0,
        "context_tags": [],  # Would be populated by auto-tagging in full implementation
        "palace_tags": [],   # Would be populated by palace mapping
        "evidence_refs": [event_data.get('evidence_ref', '')],
        "entities": event_data.get('entities', []),
        "relations": [],
        "contradicted_by": [],
        "superseded_by": None
    }
    
    # Add some basic context tags based on entities/topics
    entities = event_data.get('entities', [])
    topics = event_data.get('topics', [])
    context_tags = list(set(entities + topics))
    consolidated['context_tags'] = context_tags[:10]  # Limit tags
    
    # Basic palace tags derivation (simplified)
    palace_tags = []
    for tag in context_tags:
        if any(infra in tag.lower() for infra in ['server', 'deploy', 'aws', 'cloud', 'infra']):
            palace_tags.append('infrastructure')
        if any(tool in tag.lower() for tool in ['python', 'code', 'script', 'program']):
            palace_tags.append('development')
        if any(data in tag.lower() for data in ['data', 'database', 'sql', 'query']):
            palace_tags.append('data')
    
    # Add some default tags if none found
    if not palace_tags:
        palace_tags = ['general']
    consolidated['palace_tags'] = list(set(palace_tags))[:5]
    
    return consolidated, target_store

def store_consolidated_memory(consolidated_data, store_type):
    """Store consolidated memory in the appropriate directory."""
    base_dir = os.path.expanduser("~/.hermes/mempalace")
    store_dir = os.path.join(base_dir, store_type)
    os.makedirs(store_dir, exist_ok=True)
    
    memory_id = consolidated_data['memory_id']
    memory_file = os.path.join(store_dir, f"{memory_id}.json")
    
    with open(memory_file, 'w') as f:
        json.dump(consolidated_data, f, indent=2)
    
    return memory_file

def consolidate_memories(score_threshold=0.7):
    """Process all scored memories in raw directory for consolidation."""
    raw_dir = os.path.expanduser("~/.hermes/mempalace/raw")
    if not os.path.exists(raw_dir):
        print("No raw memories found to consolidate", file=sys.stderr)
        return 0
    
    consolidated_count = 0
    for filename in os.listdir(raw_dir):
        if not filename.endswith('.json'):
            continue
            
        event_file = os.path.join(raw_dir, filename)
        try:
            with open(event_file, 'r') as f:
                event_data = json.load(f)
            
            # Check if already processed (has score)
            if 'score' not in event_data:
                continue  # Skip unscored events
            
            consolidated_data, store_type = consolidate_memory(event_data, score_threshold)
            if consolidated_data:
                store_file = store_consolidated_memory(consolidated_data, store_type)
                print(f"Consolidated {filename} -> {store_type}/{os.path.basename(store_file)} (score: {event_data['score']:.3f})")
                consolidated_count += 1
                
                # Optionally mark as processed (could move to processed directory)
                # For now, we'll leave it but could add a processed flag
                
        except Exception as e:
            print(f"Error processing {filename}: {e}", file=sys.stderr)
    
    return consolidated_count

if __name__ == "__main__":
    threshold = 0.7
    if len(sys.argv) > 1:
        try:
            threshold = float(sys.argv[1])
        except ValueError:
            print(f"Invalid threshold: {sys.argv[1]}, using default {threshold}", file=sys.stderr)
    
    count = consolidate_memories(threshold)
    print(f"Consolidation complete: {count} memories promoted")
EOF