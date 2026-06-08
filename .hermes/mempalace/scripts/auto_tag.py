#!/usr/bin/env python3
"""
MemPalace Auto-tagging System
Automatically assigns scientific context tags and palace tags for vector metadata and palace mapping.
"""
import json
import sys
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple
import math

# Scientific domain keywords for context tagging
SCIENCE_KEYWORDS = {
    'physics': ['physics', 'quantum', 'relativity', 'particle', 'atom', 'molecule', 'energy', 'force', 'motion', 'gravity', 'electromagnetic'],
    'chemistry': ['chemistry', 'chemical', 'reaction', 'compound', 'element', 'bond', 'catalyst', 'pH', 'titration', 'synthesis'],
    'biology': ['biology', 'bio', 'cell', 'dna', 'rna', 'protein', 'gene', 'organism', 'evolution', 'ecosystem', 'metabolism'],
    'computer_science': ['computer', 'programming', 'algorithm', 'data structure', 'complexity', 'machine learning', 'ai', 'neural network', 'software', 'hardware'],
    'mathematics': ['math', 'mathematics', 'calculus', 'algebra', 'geometry', 'statistics', 'probability', 'theorem', 'proof', 'equation'],
    'engineering': ['engineering', 'engineer', 'design', 'build', 'construct', 'mechanical', 'electrical', 'civil', 'aerospace'],
    'medicine': ['medical', 'medicine', 'health', 'disease', 'treatment', 'diagnosis', 'patient', 'clinical', 'therapy', 'surgery'],
    'psychology': ['psychology', 'psychological', 'cognitive', 'behavior', 'memory', 'learning', 'emotion', 'personality', 'therapy'],
    'linguistics': ['linguistic', 'language', 'grammar', 'syntax', 'semantics', 'phonetics', 'translation', 'dialect'],
    'philosophy': ['philosophy', 'ethics', 'morality', 'logic', 'metaphysics', 'epistemology', 'aesthetics', 'existence'],
    'economics': ['economics', 'economic', 'market', 'finance', 'trade', 'supply', 'demand', 'inflation', 'gdp', 'investment'],
    'environmental_science': ['environment', 'environmental', 'climate', 'ecology', 'pollution', 'conservation', 'sustainability', 'renewable'],
    'astronomy': ['astronomy', 'astronomical', 'star', 'planet', 'galaxy', 'universe', 'cosmos', 'telescope', 'nebula', 'black hole'],
    'geology': ['geology', 'geological', 'earth', 'rock', 'mineral', 'plate tectonics', 'volcano', 'earthquake', 'fossil', 'stratum']
}

# Project-specific terminology detection (would be customized per workspace)
PROJECT_KEYWORDS = {
    'web_development': ['html', 'css', 'javascript', 'frontend', 'backend', 'api', 'rest', 'graphql', 'http', 'server', 'client'],
    'mobile_dev': ['ios', 'android', 'mobile', 'app', 'swift', 'kotlin', 'react native', 'flutter'],
    'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'dataframe', 'visualization', 'statistics'],
    'devops': ['docker', 'kubernetes', 'ci/cd', 'pipeline', 'deployment', 'infrastructure', 'aws', 'azure', 'gcp'],
    'cybersecurity': ['security', 'encryption', 'authentication', 'authorization', 'vulnerability', 'firewall', 'malware', 'phishing'],
    'game_dev': ['game', 'unity', 'unreal', 'graphics', 'rendering', 'physics engine', 'gameplay', 'sprite']
}

# Temporal markers patterns
TEMPORAL_PATTERNS = [
    r'\b\d{4}\b',  # Years
    r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # Dates
    r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # Dates with dashes
    r'\b\d+\s*(seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b',  # Durations
    r'\b(today|yesterday|tomorrow|now|then|soon|later|early|late)\b',  # Relative time
    r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b'  # Months
]

# Entity type patterns
ENTITY_PATTERNS = {
    'person': r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',  # Simple name pattern
    'tool': r'\b\w+(\s+\w+)*\s+(framework|library|tool|software|platform|system|application)\b',
    'concept': r'\b\w+(\s+\w+)*\s+(theory|model|method|approach|technique|algorithm|protocol)\b',
    'location': r'\b\w+(\s+\w+)*\s+(city|country|state|province|region|area|zone|district)\b'
}

# Emotional and priority signals
EMOTIONAL_INDICATORS = {
    'urgent': ['urgent', 'asap', 'immediately', 'critical', 'emergency'],
    'positive': ['great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'good', 'success', 'won'],
    'negative': ['bad', 'terrible', 'awful', 'horrible', 'failed', 'error', 'problem', 'issue'],
    'frustration': ['stuck', 'frustrated', 'annoyed', 'confused', 'difficult', 'hard', 'struggle'],
    'satisfaction': ['satisfied', 'pleased', 'happy', 'content', 'resolved', 'fixed', 'working']
}

def extract_context_tags(text: str, existing_tags: List[str] = None) -> List[str]:
    """
    Extract scientific context tags from text.
    
    Args:
        text: Input text to analyze
        existing_tags: Tags to preserve/add to
        
    Returns:
        List of context tags
    """
    if existing_tags is None:
        existing_tags = []
    
    tags = set(existing_tags)
    text_lower = text.lower()
    
    # Scientific domain detection
    for domain, keywords in SCIENCE_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            tags.add(domain)
    
    # Project-specific terminology
    for project, keywords in PROJECT_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            tags.add(project)
    
    # Temporal markers
    for pattern in TEMPORAL_PATTERNS:
        if re.search(pattern, text_lower):
            tags.add('temporal')
            break  # Add temporal tag once if any temporal pattern found
    
    # Entity type detection (simplified)
    for entity_type, pattern in ENTITY_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            tags.add(f'entity:{entity_type}')
    
    # Emotional and priority signals
    for emotion, indicators in EMOTIONAL_INDICATORS.items():
        if any(indicator in text_lower for indicator in indicators):
            tags.add(f'emotion:{emotion}')
    
    # Extract potential technical terms (capitalized words, acronyms)
    # Look for acronyms (2+ consecutive uppercase letters)
    acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
    for acronym in acronyms:
        if len(acronym) >= 2 and acronym not in ['AI', 'API', 'HTTP', 'URL', 'XML', 'JSON', 'SQL', 'HTML', 'CSS', 'JS']:
            tags.add(f'acronym:{acronym.lower()}')
    
    # Extract quoted terms as potential important concepts
    quoted_terms = re.findall(r'"([^"]*)"', text)
    for term in quoted_terms:
        if len(term.strip()) > 2:
            tags.add(f'quoted:{term.lower().replace(" ", "_")}')
    
    return list(tags)

def map_to_palace_tags(context_tags: List[str], user_mappings: Dict[str, str] = None) -> List[str]:
    """
    Map context tags to palace tags using predefined or user-defined mappings.
    
    Args:
        context_tags: List of context tags
        user_mappings: Optional user-defined mappings from context to palace locations
        
    Returns:
        List of palace tags
    """
    # Default mapping from context domains to palace locations
    default_palace_mapping = {
        'physics': 'science_lab',
        'chemistry': 'science_lab', 
        'biology': 'science_lab',
        'computer_science': 'tech_wing',
        'mathematics': 'study_room',
        'engineering': 'workshop',
        'medicine': 'infirmary',
        'psychology': 'study_room',
        'linguistics': 'library',
        'philosophy': 'study_room',
        'economics': 'office',
        'environmental_science': 'conservatory',
        'astronomy': 'observatory',
        'geology': 'museum',
        'web_development': 'dev_wing',
        'mobile_dev': 'dev_wing',
        'data_science': 'data_center',
        'devops': 'operations',
        'cybersecurity': 'security_wing',
        'game_dev': 'creative_studio',
        'temporal': 'archive',
        'emotion:urgent': 'war_room',
        'emotion:positive': 'celebration_hall',
        'emotion:negative': 'reflection_room',
        'emotion:frustration': 'problem_solving',
        'emotion:satisfaction': 'celebration_hall'
    }
    
    # Use user mappings if provided, otherwise use defaults
    mapping = user_mappings if user_mappings else default_palace_mapping
    
    palace_tags = set()
    
    for tag in context_tags:
        # Direct mapping
        if tag in mapping:
            palace_tags.add(mapping[tag])
        # Handle prefixed tags (emotion:, entity:, acronym:, quoted:)
        else:
            prefix = tag.split(':')[0] if ':' in tag else tag
            if prefix in mapping:
                palace_tags.add(mapping[prefix])
            # Fallback mappings for common cases
            elif tag.startswith('emotion:'):
                emotion = tag.split(':', 1)[1]
                if emotion == 'urgent':
                    palace_tags.add('war_room')
                elif emotion in ['positive', 'satisfaction']:
                    palace_tags.add('celebration_hall')
                elif emotion == 'negative':
                    palace_tags.add('reflection_room')
                elif emotion == 'frustration':
                    palace_tags.add('problem_solving')
            elif tag.startswith('entity:'):
                palace_tags.add('entities_wing')
            elif tag.startswith('acronym:') or tag.startswith('quoted:'):
                palace_tags.add('reference_library')
            elif 'temporal' in tag:
                palace_tags.add('archive')
            else:
                # Default palace location for unmapped tags
                palace_tags.add('general_storage')
    
    # Ensure we have at least one palace tag
    if not palace_tags:
        palace_tags.add('general_storage')
    
    return list(palace_tags)

def enhance_memory_with_tags(memory: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance a memory with auto-generated context and palace tags.
    
    Args:
        memory: Memory dictionary to enhance
        
    Returns:
        Enhanced memory with context_tags and palace_tags
    """
    enhanced = memory.copy()
    
    # Extract text to analyze
    text_to_analyze = ""
    if 'raw_text' in enhanced:
        text_to_analyze = enhanced['raw_text']
    elif 'text' in enhanced:
        text_to_analyze = enhanced['text']
    
    # Get existing tags
    existing_context = set(enhanced.get('context_tags', []))
    existing_palace = set(enhanced.get('palace_tags', []))
    
    # Generate context tags
    context_tags = extract_context_tags(text_to_analyze, list(existing_context))
    enhanced['context_tags'] = list(context_tags)
    
    # Generate palace tags from context tags
    palace_tags = map_to_palace_tags(context_tags)
    # Merge with existing palace tags
    all_palace_tags = set(palace_tags) | existing_palace
    enhanced['palace_tags'] = list(all_palace_tags)
    
    # Add tagging metadata
    if '_tagging_metadata' not in enhanced:
        enhanced['_tagging_metadata'] = {}
    
    enhanced['_tagging_metadata'].update({
        'context_tagging_version': '1.0',
        'palace_mapping_version': '1.0',
        'tagged_at': datetime.now(timezone.utc).isoformat(),
        'auto_generated': True
    })
    
    return enhanced

def batch_tag_memories(store_type: str) -> Dict[str, Any]:
    """
    Batch process all memories in a store to add/update tags.
    
    Args:
        store_type: Type of memory store to process
        
    Returns:
        Processing statistics
    """
    store_dir = Path.home() / '.hermes' / 'mempalace' / f'{store_type}s'
    if not store_dir.exists():
        return {'error': f'Store {store_type} does not exist'}
    
    stats = {
        'total_processed': 0,
        'tags_added': 0,
        'palace_tags_added': 0,
        'errors': 0
    }
    
    for memory_file in store_dir.glob('*.json'):
        stats['total_processed'] += 1
        
        try:
            # Read memory
            with open(memory_file, 'r') as f:
                memory = json.load(f)
            
            # Store original tag counts
            orig_context_count = len(memory.get('context_tags', []))
            orig_palace_count = len(memory.get('palace_tags', []))
            
            # Enhance with tags
            enhanced_memory = enhance_memory_with_tags(memory)
            
            # Calculate new tags added
            new_context_count = len(enhanced_memory.get('context_tags', []))
            new_palace_count = len(enhanced_memory.get('palace_tags', []))
            
            stats['tags_added'] += (new_context_count - orig_context_count)
            stats['palace_tags_added'] += (new_palace_count - orig_palace_count)
            
            # Write back enhanced memory
            with open(memory_file, 'w') as f:
                json.dump(enhanced_memory, f, indent=2)
                
        except Exception as e:
            stats['errors'] += 1
            print(f"Error processing {memory_file}: {e}")
    
    return stats

if __name__ == '__main__':
    # Test the tagging functions
    test_memory = {
        'memory_id': 'test-123',
        'user_id': 'u456',
        'timestamp': '2026-04-18T03:00:00Z',
        'raw_text': 'We decided to use Python and TensorFlow for the machine learning project. The model achieved 95% accuracy on the test dataset.',
        'memory_type': 'semantic',
        'confidence': 0.9,
        'context_tags': ['machine_learning'],
        'palace_tags': ['tech_wing']
    }
    
    print("Original memory:")
    print(json.dumps(test_memory, indent=2))
    
    enhanced = enhance_memory_with_tags(test_memory)
    print("\nEnhanced with auto-tagging:")
    print(json.dumps(enhanced, indent=2))
    
    # Test batch tagging (uncomment to run)
    # print("\nBatch tagging semantic memories:")
    # result = batch_tag_memories('semantic')
    # print(json.dumps(result, indent=2))