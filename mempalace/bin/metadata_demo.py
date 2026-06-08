#!/usr/bin/env python3
"""
Demonstrate explainability metadata and auto-tagging for MemPalace.
"""
import json
import os
import sys
import re
from datetime import datetime, timezone

def auto_tag_context(text):
    """
    Automatically assign scientific context tags based on terminology detection.
    """
    text_lower = text.lower()
    context_tags = []
    
    # Scientific domain tags
    science_domains = {
        'physics': ['physics', 'quantum', 'relativity', 'particle', 'atom', 'molecule', 
                   'force', 'energy', 'mass', 'velocity', 'acceleration'],
        'cs': ['computer', 'software', 'programming', 'algorithm', 'data structure',
               'complexity', 'database', 'network', 'protocol', 'api', 'framework'],
        'bio': ['biology', 'genetic', 'dna', 'rna', 'protein', 'cell', 'organism',
                'evolution', 'species', 'ecosystem'],
        'math': ['mathematics', 'calculus', 'algebra', 'geometry', 'statistics',
                 'probability', 'theorem', 'proof', 'equation'],
        'chem': ['chemistry', 'chemical', 'reaction', 'compound', 'element',
                 'molecule', 'bond', 'catalyst'],
        'eng': ['engineering', 'mechanical', 'electrical', 'civil', 'aerospace',
                'material', 'stress', 'strain']
    }
    
    for domain, keywords in science_domains.items():
        if any(keyword in text_lower for keyword in keywords):
            context_tags.append(domain)
    
    # Technical concepts
    tech_concepts = ['machine learning', 'ai', 'neural network', 'deep learning',
                     'cloud computing', 'docker', 'kubernetes', 'aws', 'azure',
                     'git', 'github', 'sql', 'nosql', 'rest', 'graphql']
    
    for concept in tech_concepts:
        if concept in text_lower:
            context_tags.append(concept.replace(' ', '_'))
    
    # Temporal markers
    temporal_patterns = [
        r'\b\d{4}\b',  # years
        r'\b\d{1,2}:\d{2}\b',  # times
        r'\b\d+\s*(seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b'
    ]
    
    for pattern in temporal_patterns:
        if re.search(pattern, text_lower):
            context_tags.append('temporal')
            break
    
    # Entity types (simplified)
    entity_indicators = {
        'person': ['he', 'she', 'they', 'him', 'her', 'them', 'mr.', 'mrs.', 'dr.'],
        'tool': ['python', 'javascript', 'docker', 'kubernetes', 'git', 'vim', 'emacs'],
        'concept': ['theory', 'principle', 'concept', 'idea', 'method', 'approach'],
        'location': ['server', 'database', 'cloud', 'office', 'home', 'website']
    }
    
    for entity_type, indicators in entity_indicators.items():
        if any(indicator in text_lower for indicator in indicators):
            context_tags.append(f"entity:{entity_type}")
    
    # Emotional valence and priority signals
    priority_words = ['urgent', 'critical', 'important', 'priority', 'asap', 'emergency']
    emotional_words = ['happy', 'sad', 'frustrated', 'excited', 'worried', 'pleased']
    
    if any(word in text_lower for word in priority_words):
        context_tags.append('priority:high')
    
    if any(word in text_lower for word in emotional_words):
        context_tags.append('emotional:positive' if any(w in text_lower for w in ['happy', 'excited', 'pleased']) else 'emotional:negative')
    
    return list(set(context_tags))  # Remove duplicates

def derive_palace_tags(context_tags):
    """
    Derive palace locations from context tags using predefined mapping.
    """
    palace_mapping = {
        'physics': 'science_wing',
        'cs': 'technology_wing', 
        'bio': 'science_wing',
        'math': 'science_wing',
        'chem': 'science_wing',
        'eng': 'engineering_wing',
        'machine_learning': 'ai_lab',
        'deep_learning': 'ai_lab',
        'cloud_computing': 'infrastructure_hall',
        'docker': 'devops_room',
        'kubernetes': 'devops_room',
        'aws': 'cloud_hall',
        'azure': 'cloud_hall',
        'git': 'development_room',
        'github': 'development_room',
        'sql': 'data_hall',
        'nosql': 'data_hall',
        'rest': 'api_room',
        'graphql': 'api_room',
        'temporal': 'timeline_tunnel',
        'entity:person': 'people_wing',
        'entity:tool': 'tools_closet',
        'entity:concept': 'ideas_hall',
        'entity:location': 'places_wing',
        'priority:high': 'urgent_closet',
        'emotional:positive': 'positive_hall',
        'emotional:negative': 'reflection_room'
    }
    
    palace_tags = []
    for tag in context_tags:
        # Check for exact matches
        if tag in palace_mapping:
            palace_tags.append(palace_mapping[tag])
        # Check for partial matches (e.g., entity:person)
        else:
            for key, value in palace_mapping.items():
                if tag.startswith(key.split(':')[0] + ':') or key.startswith(tag.split(':')[0] + ':'):
                    palace_tags.append(value)
                    break
    
    # Add default tags if none found
    if not palace_tags:
        palace_tags = ['general_atrium']
    
    return list(set(palace_tags))[:5]  # Limit and deduplicate

def create_explainability_metadata(memory_id, origin_events, confidence_factors, 
                                 context_tags, palace_tags, retrieval_info=None):
    """
    Create explainability metadata for a memory.
    """
    metadata = {
        "memory_id": memory_id,
        "origin": {
            "contributing_events": origin_events,  # List of memory_ids or timestamps
            "consolidation_timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "source_types": list(set([event.get('source_type', 'unknown') for event in origin_events])) if origin_events else []
        },
        "confidence": {
            "overall": confidence_factors.get('overall', 0.5),
            "factors": confidence_factors,
            "based_on": ["source_reliability", "consensus_among_sources", "corroborating_evidence"]
        },
        "context": {
            "tags": context_tags,
            "palace_location": palace_tags,
            "temporal_validity": {
                "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
                "estimated_decay": "6 months"  # Simplified
            },
            "spatial_metadata": {
                "derived_from_context": True,
                "mapping_version": "1.0"
            }
        },
        "contradictions": {
            "pointers": [],  # Would be filled during consolidation
            "conflict_resolution": "none_detected"
        },
        "reinforcement_history": {
            "retrieval_count": 0,
            "application_count": 0,
            "last_retrieved": None,
            "last_applied": None,
            "reinforcement_events": []
        },
        "decay_curve": {
            "initial_salience": confidence_factors.get('salience', 0.5),
            "half_life_days": 180,  # 6 months
            "current_estimated_value": confidence_factors.get('overall', 0.5)  # Simplified
        },
        "retrieval_info": retrieval_info or {}
    }
    
    return metadata

def demonstrate_metadata():
    """
    Demonstrate the explainability metadata and auto-tagging functionality.
    """
    # Example memory text
    example_text = "We decided to move the staging deployment to AWS eu-west-2 for better latency and cost optimization. This was based on performance testing showing 40% improvement."
    
    print("=== MemPalace Explainability Metadata and Auto-tagging Demo ===\n")
    
    print(f"Input text: {example_text}\n")
    
    # Auto-tagging
    context_tags = auto_tag_context(example_text)
    print(f"Auto-assigned context tags: {context_tags}")
    
    palace_tags = derive_palace_tags(context_tags)
    print(f"Derived palace tags: {palace_tags}\n")
    
    # Example confidence factors (would come from scoring/consolidation)
    confidence_factors = {
        'salience': 0.8,
        'reliability': 0.9,  # Direct user statement
        'utility': 0.85,     # Deployment decision
        'recency': 0.95,     # Very recent
        'priority': 0.7,     # Contains optimization language
        'overall': 0.83
    }
    
    # Example origin events (in practice, these would be raw memory IDs)
    origin_events = [
        {
            "memory_id": "raw_event_001",
            "source_type": "chat",
            "timestamp": "2026-04-19T02:00:00Z",
            "text": "We moved staging to eu-west-2."
        },
        {
            "memory_id": "raw_event_002", 
            "source_type": "chat",
            "timestamp": "2026-04-19T02:05:00Z",
            "text": "Performance tests show 40% latency improvement in eu-west-2."
        }
    ]
    
    # Create explainability metadata
    memory_id = "consolidated_memory_001"
    metadata = create_explainability_metadata(
        memory_id=memory_id,
        origin_events=origin_events,
        confidence_factors=confidence_factors,
        context_tags=context_tags,
        palace_tags=palace_tags,
        retrieval_info={
            "query_that_led_to_creation": "deployment decisions aws",
            "creation_reason": "High score consolidation"
        }
    )
    
    print("Generated Explainability Metadata:")
    print(json.dumps(metadata, indent=2))
    
    # Show how this would be stored with a consolidated memory
    consolidated_memory = {
        "memory_id": memory_id,
        "text": example_text,
        "memory_type": "semantic",
        "timestamp": "2026-04-19T02:10:00Z",
        "validity_window": "2026-04-19T02:10:00Z/2027-04-19T02:10:00Z",
        "confidence": confidence_factors['overall'],
        "reinforcement_count": 0,
        "context_tags": context_tags,
        "palace_tags": palace_tags,
        "evidence_refs": ["chat:sess123:45", "chat:sess123:46"],
        "entities": ["staging", "deployment", "AWS", "eu-west-2"],
        "explainability": metadata
    }
    
    print("\n=== Example Consolidated Memory with Metadata ===")
    print(json.dumps(consolidated_memory, indent=2))

if __name__ == "__main__":
    demonstrate_metadata()
EOF