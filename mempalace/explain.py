"""MemPalace Explainability System - Decision logging for explainability."""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Add the mempalace directory to path for imports
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

_storage_path: str = None

def init_explainability(storage_path: str):
    """Initialize the explainability system."""
    global _storage_path
    _storage_path = storage_path
    
    # Create explanations directory
    explanations_dir = os.path.join(_storage_path, 'explanations')
    os.makedirs(explanations_dir, exist_ok=True)
    
    print(f"Explainability system initialized at {_storage_path}")

def log_decision(decision_type: str, event_id: str, rationale: Dict[Any, Any], 
                context: Dict[Any, Any] = None) -> str:
    """
    Log a decision for explainability.
    
    Args:
        decision_type: Type of decision (consolidation, pruning, retrieval, etc.)
        event_id: ID of the event the decision concerns
        rationale: Dictionary explaining the decision rationale
        context: Optional contextual information
        
    Returns:
        str: Explanation ID
    """
    if _storage_path is None:
        raise RuntimeError("Explainability system not initialized. Call init_explainability() first.")
    
    # Generate explanation ID
    timestamp = datetime.now(timezone.utc).isoformat()
    rationale_str = json.dumps(rationale, sort_keys=True)
    explanation_id = f"exp_{hash(rationale_str)}_{int(datetime.now(timezone.utc).timestamp())}"
    
    # Prepare explanation record
    explanation = {
        'explanation_id': explanation_id,
        'decision_type': decision_type,
        'event_id': event_id,
        'timestamp': timestamp,
        'rationale': rationale,
        'context': context or {},
        'storage_version': '1.1.0'
    }
    
    # Store explanation
    explanations_dir = os.path.join(_storage_path, 'explanations')
    explanation_file = os.path.join(explanations_dir, f'{explanation_id}.json')
    
    with open(explanation_file, 'w') as f:
        json.dump(explanation, f, indent=2)
    
    return explanation_id

def log_consolidation_decision(event: Dict[Any, Any], score: float, 
                             individual_scores: Dict[str, float],
                             store_type: str, consolidated: bool) -> str:
    """
    Log a consolidation decision.
    
    Args:
        event: Event dictionary
        score: Composite memory score
        individual_scores: Individual component scores
        store_type: Target store type
        consolidated: Whether the event was consolidated
        
    Returns:
        str: Explanation ID
    """
    event_id = event.get('event_id', 'unknown')
    
    rationale = {
        'composite_score': score,
        'individual_scores': individual_scores,
        'store_type': store_type,
        'threshold_used': 0.6,  # From consolidate.py
        'decision': 'consolidated' if consolidated else 'not_consolidated',
        'reasoning': [
            f"Score {score:.3f} {'≥' if score >= 0.6 else '<'} threshold 0.6",
            f"Score breakdown: recency={individual_scores.get('recency', 0):.3f}, "
            f"relevance={individual_scores.get('relevance', 0):.3f}, "
            f"importance={individual_scores.get('importance', 0):.3f}, "
            f"emotional={individual_scores.get('emotional', 0):.3f}, "
            f"usage={individual_scores.get('usage', 0):.3f}"
        ]
    }
    
    context = {
        'event_type': event.get('type', 'unknown'),
        'content_length': len(event.get('content', '')),
        'has_context_tags': bool(event.get('context_tags')),
        'has_palace_tags': bool(event.get('palace_tags'))
    }
    
    return log_decision('consolidation', event_id, rationale, context)

def log_pruning_decision(event: Dict[Any, Any], score: float,
                        individual_scores: Dict[str, float],
                        pruned: bool) -> str:
    """
    Log a pruning decision.
    
    Args:
        event: Event dictionary
        score: Composite memory score
        individual_scores: Individual component scores
        pruned: Whether the event was pruned
        
    Returns:
        str: Explanation ID
    """
    event_id = event.get('event_id', 'unknown')
    
    rationale = {
        'composite_score': score,
        'individual_scores': individual_scores,
        'prune_threshold_low_score': 0.2,  # From prune.py
        'prune_max_age_days': 365,         # From prune.py
        'decision': 'pruned' if pruned else 'not_pruned',
        'reasoning': [
            f"Score {score:.3f} {'<' if score < 0.2 else '≥'} low-score threshold 0.2",
            f"Score breakdown: recency={individual_scores.get('recency', 0):.3f}, "
            f"relevance={individual_scores.get('relevance', 0):.3f}, "
            f"importance={individual_scores.get('importance', 0):.3f}, "
            f"emotional={individual_scores.get('emotional', 0):.3f}, "
            f"usage={individual_scores.get('usage', 0):.3f}"
        ]
    }
    
    context = {
        'event_type': event.get('type', 'unknown'),
        'content_length': len(event.get('content', '')),
        'timestamp': event.get('timestamp', event.get('captured_at', ''))
    }
    
    return log_decision('pruning', event_id, rationale, context)

def log_retrieval_decision(query: str, results: Dict[str, List[Dict[Any, Any]]]) -> str:
    """
    Log a retrieval decision.
    
    Args:
        query: Search query
        results: Retrieval results by layer
        
    Returns:
        str: Explanation ID
    """
    # Generate a query-based ID
    query_str = json.dumps(query, sort_keys=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    explanation_id = f"exp_query_{hash(query_str)}_{int(datetime.now(timezone.utc).timestamp())}"
    
    total_results = sum(len(layer_results) for layer_results in results.values())
    
    rationale = {
        'query': query,
        'total_results_returned': total_results,
        'results_by_layer': {layer: len(results) for layer, results in results.items()},
        'decision': 'retrieval_completed',
        'reasoning': [
            f"Query: '{query}'",
            f"Returned {total_results} total memories across {len([l for l in results.values() if l])} layers",
            f"Layer breakdown: " + ", ".join([f"{layer}: {count}" for layer, count in 
                                            [(k, len(v)) for k, v in results.items()] if count > 0])
        ]
    }
    
    context = {
        'query_length': len(query),
        'query_word_count': len(query.split())
    }
    
    return log_decision('retrieval', explanation_id, rationale, context)

def get_explanation_count() -> int:
    """Get count of explanation files stored."""
    if _storage_path is None:
        return 0
    explanations_dir = os.path.join(_storage_path, 'explanations')
    if not os.path.exists(explanations_dir):
        return 0
    return len([f for f in os.listdir(explanations_dir) if f.endswith('.json')])

def get_component_status() -> Dict[str, Any]:
    """Get status of explainability component."""
    return {
        'initialized': _storage_path is not None,
        'storage_path': _storage_path,
        'explanation_count': get_explanation_count()
    }