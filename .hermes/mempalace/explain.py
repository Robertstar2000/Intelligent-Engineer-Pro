"""
Explainability system for MemPalace - decision logging for explainability
"""

import os
import json
from datetime import datetime, timezone

# Storage path - will be set by init_explainability
_STORAGE_PATH = None
_EXPLANATION_FILE = None

def init_explainability(storage_path):
    """Initialize explainability system"""
    global _STORAGE_PATH, _EXPLANATION_FILE
    _STORAGE_PATH = storage_path
    prefs_dir = os.path.join(_STORAGE_PATH, 'preferences')
    os.makedirs(prefs_dir, exist_ok=True)
    _EXPLANATION_FILE = os.path.join(prefs_dir, 'explanations.jsonl')
    
    # Ensure file exists
    if not os.path.exists(_EXPLANATION_FILE):
        with open(_EXPLANATION_FILE, 'w') as f:
            pass  # Create empty file

def log_explanation(event_id, decision_type, details, context=""):
    """Log an explanation for a MemPalace decision"""
    if not _STORAGE_PATH or not _EXPLANATION_FILE:
        raise RuntimeError("Explainability system not initialized. Call init_explainability first.")
    
    explanation_event = {
        'event_id': event_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'decision_type': decision_type,  # e.g., 'capture', 'score', 'consolidate', 'prune', 'retrieve'
        'details': details,
        'context': context
    }
    
    try:
        with open(_EXPLANATION_FILE, 'a') as f:
            f.write(json.dumps(explanation_event) + '\n')
    except Exception as e:
        print(f"Failed to write explanation event: {e}")

def get_explanations(limit=100, decision_type=None):
    """Get explanation events"""
    if not _STORAGE_PATH or not _EXPLANATION_FILE:
        return []
    
    explanations = []
    
    try:
        with open(_EXPLANATION_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        event = json.loads(line)
                        if decision_type is None or event.get('decision_type') == decision_type:
                            explanations.append(event)
                            if len(explanations) >= limit:
                                break
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"Error reading explanation file: {e}")
        return []
    
    # Return most recent first
    explanations.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return explanations

def get_explanation_stats():
    """Get statistics about explanations"""
    if not _STORAGE_PATH or not _EXPLANATION_FILE:
        return {}
    
    stats = {
        'total_explanations': 0,
        'by_decision_type': {}
    }
    
    try:
        with open(_EXPLANATION_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        event = json.loads(line)
                        stats['total_explanations'] += 1
                        decision_type = event.get('decision_type', 'unknown')
                        stats['by_decision_type'][decision_type] = stats['by_decision_type'].get(decision_type, 0) + 1
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        print(f"Error reading explanation file for stats: {e}")
    
    return stats