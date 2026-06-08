import json
import os
from datetime import datetime, timezone
import math

# Scoring weights (can be adjusted)
WEIGHTS = {
    'recency': 0.3,
    'rehearsal': 0.25,
    'emotional_valence': 0.2,
    'context_relevance': 0.15,
    'palace_strength': 0.1
}

def _parse_timestamp(timestamp_str):
    """
    Parse a timestamp string into a timezone-aware datetime object.
    Handles both timezone-aware and naive datetime strings.
    """
    if isinstance(timestamp_str, str):
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        try:
            dt = datetime.fromisoformat(timestamp_str)
        except ValueError:
            # Fallback for other formats if needed
            dt = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
    else:
        dt = timestamp_str
    
    # Ensure timezone-aware (assume UTC if naive)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def compute_recency_score(timestamp_str, half_life_hours=24):
    """
    Compute recency score using exponential decay.
    Score ranges from 0 to 1, with 1 being most recent.
    """
    try:
        dt = _parse_timestamp(timestamp_str)
        now = datetime.now(timezone.utc)
        delta_hours = (now - dt).total_seconds() / 3600
        # Exponential decay: score = 0.5^(delta_hours / half_life_hours)
        score = math.pow(0.5, delta_hours / half_life_hours)
        return max(0.0, min(1.0, score))
    except Exception:
        return 0.0

def compute_rehearsal_score(memory_event):
    """
    Compute rehearsal score based on how many times the memory has been accessed/reinforced.
    For now, we'll use a simple count from the event's metadata.
    """
    # In a full implementation, this would track access counts
    # For now, we'll use a placeholder or look for a 'rehearsal_count' field
    rehearsal_count = memory_event.get('rehearsal_count', 0)
    # Normalize: assume 5+ rehearsals gives max score
    return min(1.0, rehearsal_count / 5.0)

def compute_emotional_valence_score(memory_event):
    """
    Compute emotional valence score.
    For simplicity, we'll use a placeholder or look for sentiment in the event.
    In a real system, this might use sentiment analysis.
    """
    # Placeholder: neutral event gets 0.5, positive/negative adjust from there
    # We could look for keywords or a sentiment field
    sentiment = memory_event.get('sentiment', 0.0)  # -1 to 1
    # Convert to 0-1 scale: (sentiment + 1) / 2
    return max(0.0, min(1.0, (sentiment + 1) / 2.0))

def compute_context_relevance_score(memory_event):
    """
    Compute context relevance score based on context tags.
    For now, we'll use the number of context tags as a proxy.
    """
    context_tags = memory_event.get('context_tags', [])
    # Normalize: assume 5+ tags gives max score
    return min(1.0, len(context_tags) / 5.0)

def compute_palace_strength_score(memory_event):
    """
    Compute palace strength score based on palace tag and frequency.
    For now, we'll use a simple heuristic: if palace_tag is set, give some score.
    """
    palace_tag = memory_event.get('palace_tag')
    if palace_tag and palace_tag != 'entrance':
        return 0.8  # Arbitrary score for non-entrance palace
    elif palace_tag == 'entrance':
        return 0.5
    else:
        return 0.0

def compute_memory_score(memory_event):
    """
    Compute the overall score for a memory event using weighted factors.
    
    Args:
        memory_event (dict): The memory event to score.
    
    Returns:
        float: The computed score between 0 and 1.
    """
    # Compute individual scores
    recency = compute_recency_score(memory_event.get('timestamp'))
    rehearsal = compute_rehearsal_score(memory_event)
    emotional = compute_emotional_valence_score(memory_event)
    context = compute_context_relevance_score(memory_event)
    palace = compute_palace_strength_score(memory_event)
    
    # Apply weights
    score = (
        WEIGHTS['recency'] * recency +
        WEIGHTS['rehearsal'] * rehearsal +
        WEIGHTS['emotional_valence'] * emotional +
        WEIGHTS['context_relevance'] * context +
        WEIGHTS['palace_strength'] * palace
    )
    
    return max(0.0, min(1.0, score))

def score_memory_file(filepath):
    """
    Score a memory event stored in a JSONL file.
    
    Args:
        filepath (str): Path to the JSONL file containing the memory event.
    
    Returns:
        tuple: (memory_id, score) or (None, None) if failed.
    """
    try:
        with open(filepath, 'r') as f:
            line = f.readline().strip()
            if not line:
                return None, None
            data = json.loads(line)
            # Validate that data is a dict
            if not isinstance(data, dict):
                print(f"Warning: Expected dict in {filepath}, got {type(data)}")
                return None, None
            memory_id = data.get('id')
            score = compute_memory_score(data)
            return memory_id, score
    except Exception as e:
        print(f"Error scoring memory file {filepath}: {e}")
        return None, None

def score_all_memories(storage_path=None):
    """
    Score all memory events in the raw store.
    
    Args:
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        dict: Mapping of memory_id to score.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    raw_dir = os.path.join(storage_path, 'raw')
    if not os.path.exists(raw_dir):
        return {}
    
    scores = {}
    for filename in os.listdir(raw_dir):
        if filename.endswith('.jsonl'):
            filepath = os.path.join(raw_dir, filename)
            memory_id, score = score_memory_file(filepath)
            if memory_id is not None and score is not None:
                scores[memory_id] = score
    
    return scores