import json
import os
from datetime import datetime, timezone

def add_explainability_metadata(memory_event, query=None, retrieval_context=None):
    """
    Add explainability metadata to a memory event.
    
    Args:
        memory_event (dict): The memory event to annotate.
        query (str, optional): The query that led to this memory's retrieval.
        retrieval_context (dict, optional): Context about how this memory was retrieved.
    
    Returns:
        dict: The memory event with added explainability metadata.
    """
    if '_explainability' not in memory_event:
        memory_event['_explainability'] = {}
    
    # Add timestamp for when explainability was added
    memory_event['_explainability']['added_at'] = datetime.now(timezone.utc).isoformat()
    
    if query is not None:
        memory_event['_explainability']['query'] = query
        
        # Add query-specific explanation
        content = memory_event.get('content', '').lower()
        context = memory_event.get('context', '').lower()
        raw_text = memory_event.get('raw_text', '').lower()
        query_lower = query.lower()
        
        memory_event['_explainability']['query_match'] = {
            'content_contains': query_lower in content,
            'context_contains': query_lower in context,
            'raw_text_contains': query_lower in raw_text,
            'exact_phrase_in_content': query in memory_event.get('content', ''),
            'exact_phrase_in_context': query in memory_event.get('context', '')
        }
        
        # Calculate match strength
        matches = sum([
            memory_event['_explainability']['query_match']['content_contains'],
            memory_event['_explainability']['query_match']['context_contains'],
            memory_event['_explainability']['query_match']['raw_text_contains']
        ])
        memory_event['_explainability']['query_match_strength'] = matches / 3.0
    
    if retrieval_context is not None:
        memory_event['_explainability']['retrieval_context'] = retrieval_context
    
    # Add scoring explanation if available
    if '_score' in memory_event:
        memory_event['_explainability']['score'] = memory_event['_score']
        
        # If we have the original scoring components, preserve them
        # This would be populated during scoring
    
    # Add layer information if available
    if '_layer' in memory_event:
        layer_descriptions = {
            0: "Vector search (FAISS)",
            1: "Working memory (recent, high rehearsal)",
            2: "High-confidence consolidated memories",
            3: "Episodic memories (context-rich)",
            4: "Raw memories (everything else)"
        }
        memory_event['_explainability']['layer'] = {
            'number': memory_event['_layer'],
            'description': layer_descriptions.get(memory_event['_layer'], f"Layer {memory_event['_layer']}")
        }
    
    # Add store type information
    if '_store_type' in memory_event:
        memory_event['_explainability']['store_type'] = memory_event['_store_type']
    
    return memory_event

def create_retrieval_explanation(query, results, storage_path=None):
    """
    Create a comprehensive explanation for a retrieval operation.
    
    Args:
        query (str): The query that was used.
        results (list): List of memory results from retrieval.
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        dict: Explanation of the retrieval operation.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    explanation = {
        'query': query,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'total_results': len(results),
        'results_by_layer': {},
        'results_by_store_type': {},
        'score_distribution': {
            'min': float('inf'),
            'max': float('-inf'),
            'avg': 0.0
        },
        'explainability_notes': []
    }
    
    if not results:
        explanation['explainability_notes'].append("No memories found matching the query.")
        return explanation
    
    # Analyze results by layer and store type
    layer_counts = {}
    store_type_counts = {}
    scores = []
    
    for result in results:
        # Count by layer
        layer = result.get('_layer', 'unknown')
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
        
        # Count by store type
        store_type = result.get('_store_type', 'unknown')
        store_type_counts[store_type] = store_type_counts.get(store_type, 0) + 1
        
        # Collect scores
        score = result.get('_score')
        if score is not None:
            scores.append(score)
    
    explanation['results_by_layer'] = layer_counts
    explanation['results_by_store_type'] = store_type_counts
    
    if scores:
        explanation['score_distribution']['min'] = min(scores)
        explanation['score_distribution']['max'] = max(scores)
        explanation['score_distribution']['avg'] = sum(scores) / len(scores)
    
    # Add notes about the retrieval
    if layer_counts:
        layer_desc = {
            0: "Vector search (FAISS)",
            1: "Working memory",
            2: "High-confidence consolidated",
            3: "Episodic",
            4: "Raw"
        }
        layers_found = [layer_desc.get(k, f"Layer {k}") for k in sorted(layer_counts.keys()) if k in layer_desc]
        explanation['explainability_notes'].append(
            f"Results retrieved from layers: {', '.join(layers_found)}"
        )
    
    if store_type_counts:
        stores_found = [f"{k} ({v})" for k, v in store_type_counts.items()]
        explanation['explainability_notes'].append(
            f"Results from stores: {', '.join(stores_found)}"
        )
    
    return explanation

def format_explanation_for_user(explanation):
    """
    Format an explanation dictionary into a human-readable string.
    
    Args:
        explanation (dict): The explanation dictionary from create_retrieval_explanation.
    
    Returns:
        str: Human-readable explanation.
    """
    lines = [
        f"Retrieval Explanation for query: '{explanation['query']}'",
        f"Timestamp: {explanation['timestamp']}",
        f"Total results found: {explanation['total_results']}",
        ""
    ]
    
    if explanation['explainability_notes']:
        lines.append("Notes:")
        for note in explanation['explainability_notes']:
            lines.append(f"  - {note}")
        lines.append("")
    
    if explanation['results_by_layer']:
        lines.append("Results by layer:")
        for layer, count in explanation['results_by_layer'].items():
            layer_desc = {
                0: "Vector search (FAISS)",
                1: "Working memory (recent, high rehearsal)",
                2: "High-confidence consolidated memories",
                3: "Episodic memories (context-rich)",
                4: "Raw memories (everything else)"
            }.get(layer, f"Layer {layer}")
            lines.append(f"  {layer_desc}: {count}")
        lines.append("")
    
    if explanation['results_by_store_type']:
        lines.append("Results by store type:")
        for store_type, count in explanation['results_by_store_type'].items():
            lines.append(f"  {store_type}: {count}")
        lines.append("")
    
    score_dist = explanation['score_distribution']
    if score_dist['min'] != float('inf'):
        lines.append("Score distribution:")
        lines.append(f"  Minimum: {score_dist['min']:.3f}")
        lines.append(f"  Maximum: {score_dist['max']:.3f}")
        lines.append(f"  Average: {score_dist['avg']:.3f}")
        lines.append("")
    
    return "\n".join(lines)