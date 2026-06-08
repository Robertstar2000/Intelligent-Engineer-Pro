"""
Daily Consolidation Script for MemPalace
Promotes important memories from raw to semantic store based on scoring.
"""

import os
import json
from datetime import datetime, timedelta, timezone

def _ensure_timezone_aware(dt_str: str) -> datetime:
    """
    Ensure datetime string is timezone-aware (UTC).
    Handles both timezone-aware and naive strings.
    """
    # If ends with Z, replace with +00:00
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1] + '+00:00'
    # If no timezone info, assume UTC
    if '+' not in dt_str and '-' not in dt_str[-6:]:
        dt_str += '+00:00'
    return datetime.fromisoformat(dt_str)

PALACE_PATH = os.path.expanduser("~/.hermes/mempalace")

def score_memory(memory):
    score = 0.0
    
    if 'score' in memory:
        score = float(memory['score'])
    
    timestamp_str = memory['timestamp']
    try:
        timestamp = _ensure_timezone_aware(timestamp_str)
        now = datetime.now(timezone.utc)
        
        # Give bonus for recent memories (within last 24 hours)
        if (now - timestamp) < timedelta(hours=24):
            score += 0.2
    except Exception as e:
        print(f"Error processing timestamp {timestamp_str}: {e}")
        # If we can't parse the timestamp, skip recency bonus
    
    if memory.get('type') == 'user_interaction':
        score += 0.3
    elif memory.get('type') == 'important_decision':
        score += 0.5
    elif memory.get('type') == 'task_completion':
        score += 0.2
    
    tags = memory.get('tags', [])
    if len(tags) >= 3:
        score += 0.1
    elif len(tags) >= 5:
        score += 0.2
    
    reinforcements = memory.get('reinforced', 0)
    if reinforcements >= 2:
        score += 0.2 * min(reinforcements, 5)
    
    return min(score, 1.0)

def consolidate_memories():
    raw_dir = os.path.join(PALACE_PATH, 'raw')
    semantic_dir = os.path.join(PALACE_PATH, 'semantic')
    
    consolidated_count = 0
    
    if not os.path.exists(semantic_dir):
        os.makedirs(semantic_dir)
    
    for filename in os.listdir(raw_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(raw_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    memory = json.load(f)
                
                if memory.get('consolidated', False):
                    continue
                
                memory_score = score_memory(memory)
                memory['score'] = memory_score
                
                if memory_score >= 0.6:
                    consolidated_memory = {
                        'id': memory['id'],
                        'type': memory['type'],
                        'content': memory['content'],
                        'context': memory['context'],
                        'tags': memory['tags'],
                        'timestamp': memory['timestamp'],
                        'source': memory['source'],
                        'score': memory_score,
                        'consolidated': True,
                        'reinforced': memory.get('reinforced', 0),
                        'original_id': memory.get('hermes_id', memory['id']),
                        'summary': memory['content'][:100] + "..." if len(memory['content']) > 100 else memory['content']
                    }
                    
                    semantic_path = os.path.join(semantic_dir, f"{memory['id']}.json")
                    with open(semantic_path, 'w') as f:
                        json.dump(consolidated_memory, f, indent=2)
                    
                    memory['consolidated'] = True
                    with open(filepath, 'w') as f:
                        json.dump(memory, f, indent=2)
                    
                    consolidated_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    print(f"Daily consolidation complete: {consolidated_count} memories promoted")

if __name__ == "__main__":
    consolidate_memories()
