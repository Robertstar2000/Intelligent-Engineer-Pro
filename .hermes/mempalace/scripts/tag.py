import json
import os
from datetime import datetime, timezone

# Context tag taxonomy
CONTEXT_TAG_TAXONOMY = {
    'technical': ['programming', 'debugging', 'architecture', 'api', 'database', 'algorithm', 'framework'],
    'creative': ['writing', 'design', 'art', 'music', 'brainstorming', 'idea'],
    'research': ['reading', 'learning', 'investigation', 'analysis', 'study', 'paper'],
    'communication': ['meeting', 'conversation', 'email', 'chat', 'presentation', 'discussion'],
    'planning': ['strategy', 'goal', 'task', 'todo', 'schedule', 'deadline'],
    'personal': ['health', 'wellbeing', 'hobby', 'family', 'friend', 'emotion']
}

# Palace tag mapping (context tags -> memory palace locations)
PALACE_TAG_MAPPING = {
    'technical': 'library',
    'creative': 'studio',
    'research': 'study',
    'communication': 'hall',
    'planning': 'war_room',
    'personal': 'garden'
}

def get_context_tags(text):
    """
    Extract context tags from text based on the taxonomy.
    
    Args:
        text (str): The text to analyze for context tags.
    
    Returns:
        list: List of context tags found in the text.
    """
    text_lower = text.lower()
    tags = []
    
    for category, keywords in CONTEXT_TAG_TAXONOMY.items():
        for keyword in keywords:
            if keyword in text_lower:
                tags.append(category)
                break  # Only add each category once
    
    return tags

def get_palace_tag(context_tags):
    """
    Get the palace tag based on context tags.
    
    Args:
        context_tags (list): List of context tags.
    
    Returns:
        str: The palace tag, or 'entrance' as default.
    """
    # Check for direct mappings
    for tag in context_tags:
        if tag in PALACE_TAG_MAPPING:
            return PALACE_TAG_MAPPING[tag]
    
    # Fallback to entrance if no mapping found
    return 'entrance'

def tag_memory_event(memory_event, storage_path=None):
    """
    Tag a memory event with context and palace tags.
    
    Args:
        memory_event (dict): The memory event to tag.
        storage_path (str, optional): Path to the mempalace storage directory.
    
    Returns:
        dict: The memory event with added tags.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    # Extract text for tagging (content + context)
    text_for_tagging = f"{memory_event.get('content', '')} {memory_event.get('context', '')}"
    
    # Get context tags
    context_tags = get_context_tags(text_for_tagging)
    
    # Get palace tag
    palace_tag = get_palace_tag(context_tags)
    
    # Add tags to memory event
    memory_event['context_tags'] = context_tags
    memory_event['palace_tag'] = palace_tag
    
    return memory_event

def save_tagged_memory(memory_event, storage_path=None):
    """
    Save a tagged memory event to the appropriate store.
    
    Args:
        memory_event (dict): The memory event to save (should already have tags).
        storage_path (str, optional): Path to the mempalace storage directory.
    """
    if storage_path is None:
        storage_path = os.path.expanduser("~/.hermes/mempalace")
    
    memory_id = memory_event.get('id')
    if not memory_id:
        print("Error: Memory event missing ID")
        return
    
    # Save to raw store (already done in capture, but we'll update if needed)
    raw_file = os.path.join(storage_path, 'raw', f"{memory_id}.jsonl")
    try:
        with open(raw_file, 'a') as f:
            f.write(json.dumps(memory_event) + '\n')
    except Exception as e:
        print(f"Failed to write tagged memory to {raw_file}: {e}")
        return
    
    # Also save to palace-specific directory if palace_tag exists
    palace_tag = memory_event.get('palace_tag')
    if palace_tag:
        palace_dir = os.path.join(storage_path, 'palace', palace_tag)
        os.makedirs(palace_dir, exist_ok=True)
        palace_file = os.path.join(palace_dir, f"{memory_id}.jsonl")
        try:
            with open(palace_file, 'a') as f:
                f.write(json.dumps(memory_event) + '\n')
        except Exception as e:
            print(f"Failed to write palace memory to {palace_file}: {e}")