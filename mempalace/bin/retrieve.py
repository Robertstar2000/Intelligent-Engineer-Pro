#!/usr/bin/env python3
"""
Retrieve memories from MemPalace layers based on query and context.
"""
import json
import os
import sys
import re
from datetime import datetime, timezone
import math

def load_json_file(filepath):
    """Safely load a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return None

def calculate_relevance(query, memory, context_tags_weight=0.4, palace_tags_weight=0.3, 
                       text_similarity_weight=0.2, recency_weight=0.1):
    """
    Calculate relevance score for a memory given a query.
    """
    query_lower = query.lower()
    
    # Text similarity (simple keyword matching for now)
    text = memory.get('text', '').lower()
    query_words = set(re.findall(r'\b\w+\b', query_lower))
    text_words = set(re.findall(r'\b\w+\b', text))
    
    if not query_words:
        text_similarity = 0.0
    else:
        overlap = len(query_words.intersection(text_words))
        text_similarity = overlap / len(query_words)
    
    # Context tags relevance
    context_tags = memory.get('context_tags', [])
    context_relevance = 0.0
    if context_tags and query_words:
        tag_words = set()
        for tag in context_tags:
            tag_words.update(re.findall(r'\b\w+\b', tag.lower()))
        overlap = len(query_words.intersection(tag_words))
        if query_words:
            context_relevance = overlap / len(query_words)
    
    # Palace tags relevance
    palace_tags = memory.get('palace_tags', [])
    palace_relevance = 0.0
    if palace_tags and query_words:
        tag_words = set()
        for tag in palace_tags:
            tag_words.update(re.findall(r'\b\w+\b', tag.lower()))
        overlap = len(query_words.intersection(tag_words))
        if query_words:
            palace_relevance = overlap / len(query_words)
    
    # Recency score
    timestamp_str = memory.get('timestamp', '')
    try:
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        event_time = datetime.fromisoformat(timestamp_str)
        now = datetime.now(timezone.utc)
        days_old = (now - event_time).total_seconds() / (24 * 3600)
        # Exponential decay with half-life of 90 days for consolidated memories
        recency_score = math.exp(-days_old / 90)
    except:
        recency_score = 0.5  # Default if timestamp parsing fails
    
    # Confidence boost
    confidence = memory.get('confidence', 0.5)
    
    # Weighted combination
    relevance = (
        context_tags_weight * context_relevance +
        palace_tags_weight * palace_relevance +
        text_similarity_weight * text_similarity +
        recency_weight * recency_score
    ) * confidence  # Apply confidence as a multiplier
    
    return min(1.0, relevance)

def retrieve_from_store(store_dir, query, limit=10):
    """Retrieve memories from a specific store."""
    if not os.path.exists(store_dir):
        return []
    
    memories = []
    for filename in os.listdir(store_dir):
        if not filename.endswith('.json'):
            continue
            
        filepath = os.path.join(store_dir, filename)
        memory = load_json_file(filepath)
        if memory is None:
            continue
            
        relevance = calculate_relevance(query, memory)
        if relevance > 0.1:  # Minimum relevance threshold
            memories.append((memory, relevance, filepath))
    
    # Sort by relevance descending
    memories.sort(key=lambda x: x[1], reverse=True)
    
    # Return top results
    return memories[:limit]

def retrieve_memory(query, user_id="default", layers=None):
    """
    Retrieve memories using layered approach.
    
    Layers:
    A: working memory (current session - not implemented here, would come from Hermes)
    B: high-confidence semantic and procedural memory
    C: episodic recall
    D: deep raw evidence
    """
    if layers is None:
        layers = ['B', 'C']  # Default to semantic/procedural and episodic
    
    base_dir = os.path.expanduser("~/.hermes/mempalace")
    store_map = {
        'semantic': os.path.join(base_dir, 'semantic'),
        'procedural': os.path.join(base_dir, 'procedural'),
        'preferences': os.path.join(base_dir, 'preferences'),
        'episodic': os.path.join(base_dir, 'episodic'),
        'raw': os.path.join(base_dir, 'raw')
    }
    
    all_results = []
    
    # Layer B: semantic and procedural (high-confidence)
    if 'B' in layers:
        for store_type in ['semantic', 'procedural', 'preferences']:
            store_dir = store_map[store_type]
            results = retrieve_from_store(store_dir, query, limit=5)
            for memory, relevance, filepath in results:
                memory['_relevance'] = relevance
                memory['_store_type'] = store_type
                memory['_layer'] = 'B'
                all_results.append(memory)
    
    # Layer C: episodic recall
    if 'C' in layers:
        store_dir = store_map['episodic']
        results = retrieve_from_store(store_dir, query, limit=5)
        for memory, relevance, filepath in results:
            memory['_relevance'] = relevance
            memory['_store_type'] = 'episodic'
            memory['_layer'] = 'C'
            all_results.append(memory)
    
    # Layer D: raw evidence (only if specifically requested or low results)
    if 'D' in layers and len(all_results) < 3:
        store_dir = store_map['raw']
        results = retrieve_from_store(store_dir, query, limit=3)
        for memory, relevance, filepath in results:
            memory['_relevance'] = relevance
            memory['_store_type'] = 'raw'
            memory['_layer'] = 'D'
            all_results.append(memory)
    
    # Sort all results by relevance
    all_results.sort(key=lambda x: x.get('_relevance', 0), reverse=True)
    
    return all_results

def format_memory_for_output(memory):
    """Format a memory for output with explainability metadata."""
    output = {
        "memory_id": memory.get('memory_id'),
        "text": memory.get('text', memory.get('raw_text', '')),
        "memory_type": memory.get('memory_type', memory.get('provisional_type', 'unknown')),
        "timestamp": memory.get('timestamp'),
        "confidence": memory.get('confidence', 0.0),
        "reinforcement_count": memory.get('reinforcement_count', 0),
        "context_tags": memory.get('context_tags', []),
        "palace_tags": memory.get('palace_tags', []),
        "entities": memory.get('entities', []),
        "relevance": memory.get('_relevance', 0.0),
        "layer": memory.get('_layer', 'unknown'),
        "store_type": memory.get('_store_type', 'unknown'),
        "explainability": {
            "why_retrieved": f"Matched query with relevance {memory.get('_relevance', 0.0):.2f}",
            "memory_type": memory.get('memory_type', memory.get('provisional_type', 'unknown')),
            "context_tags": memory.get('context_tags', []),
            "palace_tags": memory.get('palace_tags', []),
            "confidence": memory.get('confidence', 0.0),
            "timestamp": memory.get('timestamp'),
            "source_pointer": memory.get('evidence_refs', [memory.get('evidence_ref', '')])[0] if memory.get('evidence_refs') or memory.get('evidence_ref') else None
        }
    }
    
    # Add validity window if available
    if 'validity_window' in memory:
        output['validity_window'] = memory['validity_window']
    
    # Add contradictions/supersession info if available
    if 'contradicted_by' in memory:
        output['contradicted_by'] = memory['contradicted_by']
    if 'superseded_by' in memory:
        output['superseded_by'] = memory['superseded_by']
    
    return output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: retrieve.py <query> [layers]", file=sys.stderr)
        print("Layers: B (semantic/procedural/preferences), C (episodic), D (raw)", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    layers = sys.argv[2] if len(sys.argv) > 2 else "BC"
    
    memories = retrieve_memory(query, layers=layers)
    
    if not memories:
        print(json.dumps({"results": [], "count": 0}, indent=2))
        sys.exit(0)
    
    formatted_memories = [format_memory_for_output(m) for m in memories]
    
    result = {
        "query": query,
        "results": formatted_memories,
        "count": len(formatted_memories),
        "layers_queried": layers
    }
    
    print(json.dumps(result, indent=2))
EOF