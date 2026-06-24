"""MemPalace Scoring System - Memory scoring algorithm."""

import json
import os
import math
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

_storage_path: str = None

# Scoring weights - can be tuned based on domain
DEFAULT_WEIGHTS = {
    'recency': 0.3,      # How recent the memory is
    'relevance': 0.25,   # How relevant to current context
    'importance': 0.2,   # Explicit importance markers
    'emotional': 0.15,   # Emotional salience
    'usage': 0.1         # Historical usage/reinforcement
}

# Recency decay half-life (in hours)
RECENCY_HALF_LIFE_HOURS = 24.0

def init_scoring(storage_path: str):
    """Initialize the scoring system."""
    global _storage_path
    _storage_path = storage_path
    print(f"Scoring system initialized at {_storage_path}")

def calculate_recency_score(timestamp_str: str) -> float:
    """
    Calculate recency score based on time decay.
    
    Args:
        timestamp_str: ISO format timestamp string
        
    Returns:
        float: Recency score between 0 and 1
    """
    try:
        # Parse timestamp - handle both timezone-aware and naive
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        event_time = datetime.fromisoformat(timestamp_str)
        # Ensure timezone aware (assume UTC if naive)
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        hours_diff = (now - event_time).total_seconds() / 3600.0
        
        # Exponential decay with half-life
        decay_factor = math.exp(-math.log(2) * hours_diff / RECENCY_HALF_LIFE_HOURS)
        return max(0.0, min(1.0, decay_factor))
    except Exception:
        # If parsing fails, return low score
        return 0.1

def calculate_relevance_score(content: str, context_tags: List[str] = None) -> float:
    """
    Calculate relevance score based on content and tags.
    
    Args:
        content: Memory content
        context_tags: Optional context tags
        
    Returns:
        float: Relevance score between 0 and 1
    """
    score = 0.5  # Base relevance
    
    # Length factor - very short or very long content gets lower relevance
    length = len(content)
    if length < 10:
        score *= 0.5  # Too short
    elif length > 1000:
        score *= 0.8  # Quite long but still relevant
    
    # Tag diversity factor - more diverse tags indicate broader relevance
    if context_tags:
        unique_tags = len(set(context_tags))
        if unique_tags > 5:
            score *= 1.2
        elif unique_tags < 2:
            score *= 0.8
        # Cap at 1.0
        score = min(1.0, score)
    
    return max(0.0, min(1.0, score))

def calculate_importance_score(event: Dict[Any, Any]) -> float:
    """
    Calculate importance score based on event markers.
    
    Args:
        event: Event dictionary
        
    Returns:
        float: Importance score between 0 and 1
    """
    score = 0.5  # Base importance
    
    # Check for explicit importance markers
    importance_fields = ['importance', 'priority', 'significance']
    for field in importance_fields:
        if field in event:
            try:
                val = float(event[field])
                # Normalize assuming 0-1 or 0-10 scale
                if val > 1.0:  # Assume 0-10 scale
                    val = val / 10.0
                score = max(score, min(1.0, val))
            except (ValueError, TypeError):
                pass
    
    # Check for high-value event types
    high_value_types = ['user_interaction', 'editorial_decision', 'breakthrough', 'insight']
    event_type = event.get('type', '')
    if any(hvt in event_type.lower() for hvt in high_value_types):
        score = min(1.0, score + 0.2)
    
    return max(0.0, min(1.0, score))

def calculate_emotional_score(content: str) -> float:
    """
    Calculate emotional salience score.
    
    Args:
        content: Memory content
        
    Returns:
        float: Emotional score between 0 and 1
    """
    content_lower = content.lower()
    
    # Positive emotional indicators
    positive_words = ['love', 'like', 'enjoy', 'happy', 'joy', 'excited', 'proud', 
                     'satisfied', 'pleased', 'glad', 'delighted', 'thrilled']
    negative_words = ['hate', 'dislike', 'angry', 'sad', 'frustrated', 'annoyed',
                     'disappointed', 'upset', 'worried', 'anxious', 'afraid', 'scared']
    
    pos_count = sum(1 for word in positive_words if word in content_lower)
    neg_count = sum(1 for word in negative_words if word in content_lower)
    
    # Normalize by content length (rough approximation)
    word_count = len(content.split())
    if word_count > 0:
        emotion_density = (pos_count + neg_count) / word_count * 100  # Per 100 words
        # Convert to 0-1 scale with diminishing returns
        emotional_score = min(1.0, emotion_density / 10.0)  # Cap at 10 emotions per 100 words
    else:
        emotional_score = 0.0
    
    # Slight boost for any emotional content
    if emotional_score > 0:
        emotional_score = max(emotional_score, 0.3)
    
    return emotional_score

def calculate_usage_score(event_id: str) -> float:
    """
    Calculate usage score based on historical retrieval/reinforcement.
    
    Args:
        event_id: ID of the event
        
    Returns:
        float: Usage score between 0 and 1
    """
    if _storage_path is None:
        return 0.0
    
    # Check reinforcement file
    reinforcement_file = os.path.join(_storage_path, 'reinforcement.jsonl')
    if not os.path.exists(reinforcement_file):
        return 0.0
    
    try:
        reinforcement_count = 0
        with open(reinforcement_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get('event_id') == event_id:
                        reinforcement_count += 1
                except json.JSONDecodeError:
                    continue
        
        # Logarithmic scaling - first few reinforcements matter most
        if reinforcement_count == 0:
            return 0.0
        elif reinforcement_count == 1:
            return 0.3
        else:
            # Diminishing returns after 5 reinforcements
            return min(1.0, 0.3 + 0.7 * (1 - math.exp(-reinforcement_count / 5.0)))
    except Exception:
        return 0.0

def score_memory(event: Dict[Any, Any], weights: Dict[str, float] = None) -> Tuple[float, Dict[str, float]]:
    """
    Calculate composite memory score using weighted factors.
    
    Args:
        event: Event dictionary to score
        weights: Optional custom weights (defaults to DEFAULT_WEIGHTS)
        
    Returns:
        Tuple of (composite_score, individual_scores)
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS
    
    # Extract components
    content = event.get('content', '')
    timestamp_str = event.get('timestamp', event.get('captured_at', ''))
    context_tags = event.get('context_tags', [])
    
    # Calculate individual scores
    recency_score = calculate_recency_score(timestamp_str)
    relevance_score = calculate_relevance_score(content, context_tags)
    importance_score = calculate_importance_score(event)
    emotional_score = calculate_emotional_score(content)
    usage_score = calculate_usage_score(event.get('event_id', ''))
    
    individual_scores = {
        'recency': recency_score,
        'relevance': relevance_score,
        'importance': importance_score,
        'emotional': emotional_score,
        'usage': usage_score
    }
    
    # Calculate weighted composite score
    composite_score = (
        weights['recency'] * recency_score +
        weights['relevance'] * relevance_score +
        weights['importance'] * importance_score +
        weights['emotional'] * emotional_score +
        weights['usage'] * usage_score
    )
    
    return max(0.0, min(1.0, composite_score)), individual_scores

def get_component_status() -> Dict[str, Any]:
    """Get status of scoring component."""
    return {
        'initialized': _storage_path is not None,
        'storage_path': _storage_path,
        'weights': DEFAULT_WEIGHTS,
        'recency_half_life_hours': RECENCY_HALF_LIFE_HOURS
    }