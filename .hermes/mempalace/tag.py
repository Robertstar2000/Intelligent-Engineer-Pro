"""MemPalace Tagging System - Context and palace tagging."""

import json
import os
from datetime import datetime, timezone
import re
from typing import List, Dict, Any, Set

_storage_path: str = None

# Context tag taxonomy - can be extended based on domain
CONTEXT_TAG_TAXONOMY = {
    'user_interaction': ['question', 'request', 'feedback', 'clarification'],
    'book_writing': ['draft', 'outline', 'character', 'plot', 'dialogue', 'editing'],
    'editorial_review': ['criteria', 'checklist', 'consistency', 'series', 'genre'],
    'research': ['source', 'citation', 'fact', 'reference'],
    'coding': ['bug', 'feature', 'refactor', 'test', 'debug'],
    'planning': ['goal', 'objective', 'milestone', 'deadline'],
    'memory': ['consolidation', 'recall', 'storage'],
    'system': ['startup', 'shutdown', 'error', 'warning', 'info']
}

# Palace tag mapping - maps context tags to memory palace locations
PALACE_TAG_MAPPING = {
    'question': 'hall_of_questions',
    'request': 'hall_of_requests', 
    'feedback': 'gallery_of_feedback',
    'clarification': 'room_of_clarity',
    'draft': 'library_drafts',
    'outline': 'planning_chamber',
    'character': 'character_gallery',
    'plot': 'plot_labyrinth',
    'dialogue': 'conversation_hall',
    'editing': 'editing_studio',
    'criteria': 'criteria_chamber',
    'checklist': 'checklist_room',
    'consistency': 'consistency_court',
    'series': 'series_archive',
    'genre': 'genre_wing',
    'source': 'source_library',
    'citation': 'citation_index',
    'fact': 'fact_repository',
    'reference': 'reference_desk',
    'bug': 'debugging_dungeon',
    'feature': 'feature_forge',
    'refactor': 'refactory_workshop',
    'test': 'testing_grounds',
    'planning': 'strategy_room',
    'goal': 'goal_altar',
    'objective': 'objective_obelisk',
    'milestone': 'milestone_markers',
    'deadline': 'time_tower',
    'memory': 'memory_vault',
    'consolidation': 'consolidation_chamber',
    'recall': 'recall_rotunda',
    'storage': 'storage_cellars',
    'system': 'system_core',
    'startup': 'dawn_chamber',
    'shutdown': 'dusk_chamber',
    'error': 'error_ogee',
    'warning': 'warning_watchtower',
    'info': 'info_inn'
}

def init_tagging(storage_path: str):
    """Initialize the tagging system."""
    global _storage_path
    _storage_path = storage_path
    print(f"Tagging system initialized at {_storage_path}")

def extract_context_tags(content: str, event_type: str = None) -> List[str]:
    """
    Extract context tags from content based on keywords and patterns.
    
    Args:
        content: Text content to analyze
        event_type: Optional event type for targeted tagging
        
    Returns:
        List of context tags
    """
    tags = set()
    content_lower = content.lower()
    
    # Add event type as tag if provided
    if event_type:
        tags.add(event_type)
    
    # Check for keywords from taxonomy
    for category, keywords in CONTEXT_TAG_TAXONOMY.items():
        for keyword in keywords:
            if keyword in content_lower:
                tags.add(keyword)
                # Also add the category as a broader tag
                tags.add(category)
    
    # Pattern-based tagging
    patterns = {
        r'\b(book|chapter|novel|story)\b': 'book_writing',
        r'\b(editorial|review|critique)\b': 'editorial_review',
        r'\b(character|persona|protagonist)\b': 'character',
        r'\b(plot|storyline|narrative)\b': 'plot',
        r'\b(series|sequence|trilogy)\b': 'series',
        r'\b(genre|style|tone)\b': 'genre',
        r'\b(edit|revise|rewrite)\b': 'editing',
        r'\b(research|study|investigate)\b': 'research',
        r'\b(source|reference|citation)\b': 'source',
        r'\b(bug|error|issue|problem)\b': 'bug',
        r'\b(feature|enhancement|improvement)\b': 'feature',
        r'\b(test|testing|qa)\b': 'test',
        r'\b(refactor|refactoring|restructure)\b': 'refactor',
        r'\b(plan|planning|strategy)\b': 'planning',
        r'\b(goal|objective|target|aim)\b': 'goal',
        r'\b(milestone|checkpoint|benchmark)\b': 'milestone',
        r'\b(deadline|due|date|time)\b': 'deadline',
        r'\b(memory|recall|remember|store)\b': 'memory',
        r'\b(consolidate|merge|combine)\b': 'consolidation',
        r'\b(start|begin|init|launch)\b': 'startup',
        r'\b(stop|end|finish|shutdown)\b': 'shutdown',
        r'\b(error|fail|exception|crash)\b': 'error',
        r'\b(warning|caution|alert)\b': 'warning',
        r'\b(info|information|detail|data)\b': 'info'
    }
    
    for pattern, tag in patterns.items():
        if re.search(pattern, content_lower):
            tags.add(tag)
    
    return list(tags)

def save_context_tags(event_id: str, tags: List[str]):
    """
    Save context tags for an event.
    
    Args:
        event_id: ID of the event
        tags: List of context tags to save
    """
    if _storage_path is None:
        raise RuntimeError("Tagging system not initialized. Call init_tagging() first.")
    
    tags_dir = os.path.join(_storage_path, 'tags')
    os.makedirs(tags_dir, exist_ok=True)
    
    tags_file = os.path.join(tags_dir, f'{event_id}.json')
    tag_data = {
        'event_id': event_id,
        'tags': tags,
        'saved_at': datetime.now(timezone.utc).isoformat()
    }
    
    with open(tags_file, 'w') as f:
        json.dump(tag_data, f, indent=2)

def get_palace_tags(context_tags: List[str]) -> List[str]:
    """
    Map context tags to palace tags using predefined mapping.
    
    Args:
        context_tags: List of context tags
        
    Returns:
        List of palace tags
    """
    palace_tags = set()
    for tag in context_tags:
        if tag in PALACE_TAG_MAPPING:
            palace_tags.add(PALACE_TAG_MAPPING[tag])
    return list(palace_tags)

def get_tag_count() -> int:
    """Get count of tag files stored."""
    if _storage_path is None:
        return 0
    tags_dir = os.path.join(_storage_path, 'tags')
    if not os.path.exists(tags_dir):
        return 0
    return len([f for f in os.listdir(tags_dir) if f.endswith('.json')])