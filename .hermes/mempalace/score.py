"""
Scoring system for MemPalace - memory scoring algorithm
"""

import os
import math
from datetime import datetime, timezone
import tag

# Storage path - will be set by init_scoring
_STORAGE_PATH = None

# Scoring weights (can be tuned)
WEIGHTS = {
    'recency': 0.3,
    'context': 0.2,
    'palace': 0.2,
    'length': 0.1,
    'importance': 0.2
}

# Recency decay half-life (in hours)
RECENCY_HALF_LIFE = 24.0

def init_scoring(storage_path):
    """Initialize scoring system"""
    global _STORAGE_PATH
    _STORAGE_PATH = storage_path

def score_event(event):
    """Score a memory event based on multiple factors"""
    if not _STORAGE_PATH:
        raise RuntimeError("Scoring system not initialized. Call init_scoring first.")
    
    # Extract event data
    event_data = event.get('data', {}) if isinstance(event, dict) else {}
    timestamp_str = event.get('timestamp', '')
    
    # 1. Recency score (exponential decay with half-life)
    recency_score = 0.0
    if timestamp_str:
        try:
            # Handle both timezone-aware and naive timestamps
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str[:-1] + '+00:00'
            timestamp = datetime.fromisoformat(timestamp_str)
            # Ensure timezone-aware (assume UTC if naive)
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            else:
                timestamp = timestamp.astimezone(timezone.utc)
            
            now = datetime.now(timezone.utc)
            hours_diff = (now - timestamp).total_seconds() / 3600.0
            # Exponential decay: score = exp(-lambda * hours)
            lambda_decay = math.log(2) / RECENCY_HALF_LIFE
            recency_score = math.exp(-lambda_decay * hours_diff)
            # Ensure score is in [0, 1]
            recency_score = max(0.0, min(1.0, recency_score))
        except Exception as e:
            print(f"Error parsing timestamp for recency: {e}")
            recency_score = 0.5  # Default middle score on error
    
    # 2. Context tag score (proportion of relevant context tags)
    context_score = 0.0
    try:
        # Extract text for tagging
        text_content = ""
        if isinstance(event_data, dict):
            for field in ['content', 'text', 'message', 'description', 'title']:
                if field in event_data and isinstance(event_data[field], str):
                    text_content = event_data[field]
                    break
        if not text_content:
            text_content = str(event_data)
        
        context_tags = tag.extract_context_tags(text_content)
        # Score based on number of context tags found (up to a reasonable max)
        max_expected_tags = 5  # Adjust based on taxonomy
        context_score = min(1.0, len(context_tags) / max_expected_tags)
    except Exception as e:
        print(f"Error computing context score: {e}")
        context_score = 0.0
    
    # 3. Palace tag score (proportion of relevant palace tags)
    palace_score = 0.0
    try:
        # Reuse context tags or extract again
        if 'context_tags' not in locals():
            text_content = ""
            if isinstance(event_data, dict):
                for field in ['content', 'text', 'message', 'description', 'title']:
                    if field in event_data and isinstance(event_data[field], str):
                        text_content = event_data[field]
                        break
            if not text_content:
                text_content = str(event_data)
            context_tags = tag.extract_context_tags(text_content)
        
        palace_tags = tag.extract_palace_tags(context_tags)
        # Score based on number of palace tags found (up to a reasonable max)
        max_expected_palace = 3  # Adjust based on mapping
        palace_score = min(1.0, len(palace_tags) / max_expected_palace)
    except Exception as e:
        print(f"Error computing palace score: {e}")
        palace_score = 0.0
    
    # 4. Length score (normalize by expected length)
    length_score = 0.0
    try:
        if isinstance(event_data, dict):
            # Try to get text content again
            text_content = ""
            for field in ['content', 'text', 'message', 'description', 'title']:
                if field in event_data and isinstance(event_data[field], str):
                    text_content = event_data[field]
                    break
            if not text_content:
                text_content = str(event_data)
        else:
            text_content = str(event_data)
        
        # Normalize length: assume 500 chars is good, 1000+ is max
        text_len = len(text_content)
        if text_len >= 1000:
            length_score = 1.0
        elif text_len <= 0:
            length_score = 0.0
        else:
            length_score = text_len / 1000.0  # Linear up to 1000 chars
    except Exception as e:
        print(f"Error computing length score: {e}")
        length_score = 0.0
    
    # 5. Importance score (from explicit importance field or default)
    importance_score = 0.5  # Default middle importance
    try:
        if isinstance(event_data, dict) and 'importance' in event_data:
            imp = event_data['importance']
            if isinstance(imp, (int, float)):
                # Clamp to [0, 1]
                importance_score = max(0.0, min(1.0, float(imp)))
    except Exception as e:
        print(f"Error computing importance score: {e}")
        importance_score = 0.5
    
    # Calculate weighted sum
    total_score = (
        WEIGHTS['recency'] * recency_score +
        WEIGHTS['context'] * context_score +
        WEIGHTS['palace'] * palace_score +
        WEIGHTS['length'] * length_score +
        WEIGHTS['importance'] * importance_score
    )
    
    # Ensure final score is in [0, 1]
    total_score = max(0.0, min(1.0, total_score))
    
    return total_score

def score_events(events):
    """Score a list of events"""
    scored_events = []
    for event in events:
        score = score_event(event)
        scored_event = event.copy() if isinstance(event, dict) else {'raw_data': event}
        scored_event['mempalace_score'] = score
        scored_events.append(scored_event)
    return scored_events