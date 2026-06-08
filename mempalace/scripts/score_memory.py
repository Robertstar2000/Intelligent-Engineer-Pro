#!/usr/bin/env python3
"""
MemPalace Memory Scoring
Scores captured memories before consolidation.
"""
import json
import sys
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

def calculate_salience(event: Dict[str, Any]) -> float:
    """Calculate salience score based on importance to goals or identity."""
    score = 0.5  # Base score
    
    # Increase for user facts, decisions, constraints
    provisional_type = event.get('provisional_type', '')
    if provisional_type in ['semantic', 'preference', 'procedural']:
        score += 0.2
    
    # Increase for entities that seem important
    entities = event.get('entities', [])
    important_keywords = ['user', 'prefer', 'decide', 'constraint', 'goal', 'project']
    if any(keyword in str(entities).lower() for keyword in important_keywords):
        score += 0.1
    
    # Increase for unresolved tasks or failures
    raw_text = event.get('raw_text', '').lower()
    if any(word in raw_text for word in ['fail', 'error', 'problem', 'issue', 'blocked']):
        score += 0.15
    
    return min(score, 1.0)

def calculate_recurrence(user_id: str, session_id: str, raw_text: str) -> float:
    """Calculate recurrence score based on repeated mentions."""
    # This would typically query the raw storage for similar events
    # For now, return a placeholder based on text length and simplicity
    # In practice, this would search for similar events across sessions
    return 0.3  # Placeholder

def calculate_recency(timestamp_str: str) -> float:
    """Calculate recency score with decay over time."""
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        hours_diff = (now - timestamp).total_seconds() / 3600
        
        # Decay function: score decreases over time but never hits zero
        # Using exponential decay with half-life of 7 days (168 hours)
        decay_factor = math.exp(-0.693 * hours_diff / 168)
        return max(decay_factor, 0.1)  # Minimum score of 0.1
    except:
        return 0.5  # Default if parsing fails

def calculate_emotional_priority(event: Dict[str, Any]) -> float:
    """Calculate score based on emotional or priority markers."""
    score = 0.0
    raw_text = event.get('raw_text', '').lower()
    
    # Priority markers
    if any(word in raw_text for word in ['urgent', 'critical', 'important', 'asap']):
        score += 0.3
    if any(word in raw_text for word in ['blocked', 'stuck', 'need help']):
        score += 0.2
    
    # Emotional valence (simplified)
    positive_words = ['great', 'good', 'success', 'working', 'fixed']
    negative_words = ['bad', 'wrong', 'broken', 'failed', 'terrible']
    if any(word in raw_text for word in positive_words):
        score += 0.1
    if any(word in raw_text for word in negative_words):
        score += 0.15  # Negative events often more memorable
    
    return min(score, 0.5)

def calculate_utility(event: Dict[str, Any]) -> float:
    """Calculate utility: likely to improve future answers or actions."""
    score = 0.3  # Base utility
    
    # Increase for procedural knowledge
    if event.get('provisional_type') == 'procedural':
        score += 0.3
    
    # Increase for factual information
    if event.get('provisional_type') == 'semantic':
        score += 0.2
    
    # Increase for specific, actionable information
    raw_text = event.get('raw_text', '')
    if len(raw_text) > 20 and any(char.isdigit() for char in raw_text):
        score += 0.1  # Specific details often useful
    
    return min(score, 1.0)

def calculate_reliability(event: Dict[str, Any]) -> float:
    """Calculate reliability: direct user statement beats inference."""
    score = 0.5  # Base reliability
    
    source_type = event.get('source_type', '')
    if source_type == 'user_statement':
        score += 0.4
    elif source_type == 'chat':
        score += 0.2
    elif source_type == 'tool_output':
        score += 0.3  # Verified system result
    elif source_type == 'inference':
        score += 0.0  # Lower reliability for inferences
    
    # Check for verification signals
    raw_text = event.get('raw_text', '').lower()
    if any(word in raw_text for word in ['confirmed', 'verified', 'tested', 'proven']):
        score += 0.2
    
    return min(score, 1.0)

def calculate_interference_risk(event: Dict[str, Any]) -> float:
    """Calculate interference risk: ambiguous or conflicting memory gets lower score."""
    risk = 0.0  # Start with no risk
    
    # Check for ambiguity in text
    raw_text = event.get('raw_text', '')
    ambiguous_phrases = ['maybe', 'perhaps', 'might be', 'could be', 'i think', 'probably']
    if any(phrase in raw_text.lower() for phrase in ambiguous_phrases):
        risk += 0.3
    
    # Check for conflicting entities or topics (would need context from other memories)
    # For now, use heuristic based on vague language
    vague_words = ['thing', 'stuff', 'something', 'somehow']
    if any(word in raw_text.lower() for word in vague_words):
        risk += 0.2
    
    return min(risk, 0.5)  # Cap interference risk

def score_memory(event: Dict[str, Any]) -> Dict[str, Any]:
    """Score a memory event and return scored event."""
    # Calculate individual scores
    salience = calculate_salience(event)
    recurrence = calculate_recurrence(
        event.get('user_id', ''), 
        event.get('session_id', ''), 
        event.get('raw_text', '')
    )
    recency = calculate_recency(event.get('timestamp', ''))
    emotional = calculate_emotional_priority(event)
    utility = calculate_utility(event)
    reliability = calculate_reliability(event)
    interference = calculate_interference_risk(event)
    
    # Weighted combination (weights can be tuned)
    weights = {
        'salience': 0.25,
        'recurrence': 0.15,
        'recency': 0.15,
        'emotional': 0.10,
        'utility': 0.15,
        'reliability': 0.15,
        'interference': -0.05  # Negative weight - higher interference lowers score
    }
    
    total_score = (
        weights['salience'] * salience +
        weights['recurrence'] * recurrence +
        weights['recency'] * recency +
        weights['emotional'] * emotional +
        weights['utility'] * utility +
        weights['reliability'] * reliability +
        weights['interference'] * interference
    )
    
    # Normalize to 0-1 range (though should already be in range)
    total_score = max(0.0, min(1.0, total_score))
    
    # Add scores to event
    scored_event = event.copy()
    scored_event['salience_score'] = salience
    scored_event['recurrence_score'] = recurrence
    scored_event['recency_score'] = recency
    scored_event['emotional_score'] = emotional
    scored_event['utility_score'] = utility
    scored_event['reliability_score'] = reliability
    scored_event['interference_score'] = interference
    scored_event['total_score'] = total_score
    scored_event['scored_at'] = datetime.now(timezone.utc).isoformat()
    
    return scored_event

if __name__ == '__main__':
    # Read JSON from stdin
    try:
        data = sys.stdin.read().strip()
        if not data:
            sys.exit(0)
        event = json.loads(data)
        scored_event = score_memory(event)
        # Output the scored event
        print(json.dumps(scored_event))
    except json.JSONDecodeError as e:
        print(json.dumps({'error': f'Invalid JSON: {e}'}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)