"""
Tagging system for MemPalace - context and palace tagging
"""

import os
import re
from typing import List, Dict, Set
import json
from datetime import datetime, timezone

# Storage path - will be set by init_tagging
_STORAGE_PATH = None

# Context tag taxonomy - can be extended
CONTEXT_TAG_TAXONOMY = {
    'technical': ['code', 'programming', 'debugging', 'algorithm', 'database', 'api', 'framework', 'library'],
    'business': ['meeting', 'project', 'deadline', 'client', 'sales', 'marketing', 'finance', 'strategy'],
    'personal': ['health', 'exercise', 'food', 'travel', 'family', 'friends', 'hobby', 'learning'],
    'creative': ['writing', 'design', 'art', 'music', 'brainstorm', 'idea', 'concept'],
    'research': ['paper', 'study', 'experiment', 'data', 'analysis', 'hypothesis', 'literature'],
    'communication': ['email', 'message', 'call', 'presentation', 'discussion', 'feedback']
}

# Palace tag mapping - maps context tags to memory palaces
PALACE_TAG_MAPPING = {
    'technical': 'workshop',
    'business': 'office',
    'personal': 'home',
    'creative': 'studio',
    'research': 'library',
    'communication': 'hall'
}

def init_tagging(storage_path):
    """Initialize tagging system"""
    global _STORAGE_PATH
    _STORAGE_PATH = storage_path

def extract_context_tags(text: str) -> List[str]:
    """Extract context tags from text based on taxonomy"""
    if not text:
        return []
    
    text_lower = text.lower()
    tags = set()
    
    for category, keywords in CONTEXT_TAG_TAXONOMY.items():
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                tags.add(category)
                break  # One match per category is enough
    
    return list(tags)

def extract_palace_tags(context_tags: List[str]) -> List[str]:
    """Derive palace tags from context tags"""
    palace_tags = set()
    for tag in context_tags:
        if tag in PALACE_TAG_MAPPING:
            palace_tags.add(PALACE_TAG_MAPPING[tag])
    
    # If no palace tags found, use a default
    if not palace_tags:
        palace_tags.add('atrium')  # Default palace
    
    return list(palace_tags)

def tag_event(event_data: dict) -> dict:
    """Add context and palace tags to event data"""
    # Extract text content for tagging
    text_content = ""
    if isinstance(event_data, dict):
        # Try common content fields
        for field in ['content', 'text', 'message', 'description', 'title']:
            if field in event_data and isinstance(event_data[field], str):
                text_content = event_data[field]
                break
    
    # If no text found, use string representation
    if not text_content:
        text_content = str(event_data)
    
    context_tags = extract_context_tags(text_content)
    palace_tags = extract_palace_tags(context_tags)
    
    # Add tags to event data
    tagged_data = event_data.copy() if isinstance(event_data, dict) else {'raw_data': event_data}
    tagged_data['context_tags'] = context_tags
    tagged_data['palace_tags'] = palace_tags
    
    return tagged_data
def save_context_tags(event_id, tags):
    """Save context tags for a memory event"""
    if not _STORAGE_PATH:
        raise RuntimeError("Tagging system not initialized. Call init_tagging first.")
    
    tags_file = os.path.join(_STORAGE_PATH, 'context_tags.jsonl')
    
    try:
        with open(tags_file, 'a') as f:
            f.write(json.dumps({
                'memory_id': event_id,
                'tags': tags,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }) + '\n')
    except Exception as e:
        print(f"Failed to write context tags: {e}")
