#!/usr/bin/env python3
"""
Score a captured memory event based on various features.
"""
import json
import os
import sys
from datetime import datetime, timezone
import math

def calculate_score(event_data):
    """
    Calculate a weighted score for a memory event.
    
    Features:
    - salience: importance to goals or identity (0-1)
    - recurrence: repeated mentions across sessions (0-1)
    - recency: decay over time, not immediate deletion (0-1)
    - emotional or priority markers: urgent, critical, blocked (0-1)
    - utility: likely to improve future answers or actions (0-1)
    - reliability: direct user statement or verified system result beats inference (0-1)
    - interference risk: ambiguous or conflicting memory gets lower automatic promotion (0-1, inverted)
    """
    
    # Base score from provided salience and reliability
    salience = event_data.get('salience', 0.5)
    reliability = event_data.get('reliability', 0.5)
    
    # Recency score: exponential decay with half-life of 30 days
    timestamp_str = event_data['timestamp']
    if timestamp_str.endswith('Z'):
        timestamp_str = timestamp_str[:-1] + '+00:00'
    try:
        event_time = datetime.fromisoformat(timestamp_str)
    except ValueError:
        # Fallback for unexpected format
        event_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    # Ensure timezone awareness (assume UTC if naive)
    if event_time.tzinfo is None:
        event_time = event_time.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    days_old = (now - event_time).total_seconds() / (24 * 3600)
    recency_score = math.exp(-days_old / 30)  # Half-life of ~30 days
    
    # Utility score: based on provisional type (semantic and procedural are more useful)
    provisional_type = event_data.get('provisional_type', 'episodic')
    utility_map = {
        'semantic': 0.9,
        'procedural': 0.8,
        'preference': 0.85,
        'episodic': 0.6,
        'task-state': 0.4
    }
    utility = utility_map.get(provisional_type, 0.5)
    
    # Priority markers: check for urgent/critical/blocked in text
    text = event_data.get('raw_text', '').lower()
    priority_keywords = ['urgent', 'critical', 'blocked', 'important', 'priority']
    priority_score = min(1.0, sum(0.2 for kw in priority_keywords if kw in text))
    
    # Recurrence: would need to check against other events - simplified for now
    # In a full implementation, this would search for similar entities/topics
    recurrence_score = 0.5  # Placeholder
    
    # Interference risk: check for ambiguity indicators
    ambiguity_indicators = ['maybe', 'perhaps', 'might', 'could', 'unclear', 'confusing']
    ambiguity_count = sum(1 for indicator in ambiguity_indicators if indicator in text)
    interference_risk = min(1.0, ambiguity_count * 0.2)  # More ambiguity = higher risk
    interference_score = 1.0 - interference_risk  # Invert: lower risk = higher score
    
    # Weighted combination
    weights = {
        'salience': 0.25,
        'reliability': 0.2,
        'recency': 0.15,
        'utility': 0.15,
        'priority': 0.1,
        'recurrence': 0.1,
        'interference': 0.05
    }
    
    score = (
        weights['salience'] * salience +
        weights['reliability'] * reliability +
        weights['recency'] * recency_score +
        weights['utility'] * utility +
        weights['priority'] * priority_score +
        weights['recurrence'] * recurrence_score +
        weights['interference'] * interference_score
    )
    
    return min(1.0, max(0.0, score))

def score_memory_event(event_file_path):
    """Score a memory event from its JSON file."""
    try:
        with open(event_file_path, 'r') as f:
            event_data = json.load(f)
        
        score = calculate_score(event_data)
        
        # Add score to the event data
        event_data['score'] = score
        event_data['scored_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Write back the scored event
        with open(event_file_path, 'w') as f:
            json.dump(event_data, f, indent=2)
        
        return score
    except Exception as e:
        print(f"Error scoring memory event: {e}", file=sys.stderr)
        return 0.0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        event_file = sys.argv[1]
    else:
        # Score all events in raw directory
        raw_dir = os.path.expanduser("~/.hermes/mempalace/raw")
        if not os.path.exists(raw_dir):
            print("No raw memories found to score", file=sys.stderr)
            sys.exit(0)
        
        scores = []
        for filename in os.listdir(raw_dir):
            if filename.endswith('.json'):
                event_file = os.path.join(raw_dir, filename)
                score = score_memory_event(event_file)
                scores.append(score)
                print(f"Scored {filename}: {score:.3f}")
        
        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"Average score: {avg_score:.3f} across {len(scores)} memories")
        sys.exit(0)
    
    # Score single file
    score = score_memory_event(event_file)
    print(f"Score for {event_file}: {score:.3f}")
EOF