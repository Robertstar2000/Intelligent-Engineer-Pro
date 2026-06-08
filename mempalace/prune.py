"""
Pruning system for MemPalace - memory pruning with archiving
"""

import os
import json
import shutil
from datetime import datetime, timezone
import score
import capture
from datetime import timedelta

# Pruning thresholds
PRUNE_AGE_DAYS = 30  # Memories older than this are candidates for pruning
PRUNE_SCORE_THRESHOLD = 0.3  # Memories scoring below this are pruned
ARCHIVE_DIR = 'archive'

def init_pruning(storage_path):
    """Initialize pruning system"""
    global _STORAGE_PATH
    _STORAGE_PATH = storage_path
    
    # Ensure archive directory exists
    archive_path = os.path.join(_STORAGE_PATH, ARCHIVE_DIR)
    os.makedirs(archive_path, exist_ok=True)

def prune_memories(dry_run=False):
    """Prune low-value, old memories"""
    if not _STORAGE_PATH:
        raise RuntimeError("Pruning system not initialized. Call init_pruning first.")
    
    pruned_count = 0
    archived_count = 0
    
    # Prune raw memories
    pruned_raw, archived_raw = _prune_raw_memories(dry_run)
    pruned_count += pruned_raw
    archived_count += archived_raw
    
    # Note: We typically don't prune consolidated memories as they represent important knowledge
    # But we could add logic to prune very old consolidated memories if needed
    
    return {
        'pruned': pruned_count,
        'archived': archived_count,
        'dry_run': dry_run
    }

def _prune_raw_memories(dry_run=False):
    """Prune raw memory events"""
    pruned = 0
    archived = 0
    
    if not _STORAGE_PATH:
        return pruned, archived
    
    raw_dir = os.path.join(_STORAGE_PATH, 'raw')
    archive_dir = os.path.join(_STORAGE_PATH, ARCHIVE_DIR, 'raw')
    os.makedirs(archive_dir, exist_ok=True)
    
    # Calculate cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=PRUNE_AGE_DAYS)
    
    # Process each raw file
    if os.path.exists(raw_dir):
        for filename in os.listdir(raw_dir):
            if filename.endswith('.jsonl'):
                filepath = os.path.join(raw_dir, filename)
                archive_filepath = os.path.join(archive_dir, filename)
                
                # Read all events
                kept_lines = []
                pruned_lines = []
                
                try:
                    with open(filepath, 'r') as f:
                        for line_num, line in enumerate(f, 1):
                            line = line.strip()
                            if not line:
                                continue
                            
                            try:
                                event = json.loads(line)
                                # Validate it's a dict
                                if not isinstance(event, dict):
                                    # Keep non-dict lines (they might be valid in some contexts)
                                    kept_lines.append(line)
                                    continue
                                
                                # Check if event should be pruned
                                timestamp_str = event.get('timestamp', '')
                                should_prune = False
                                
                                if timestamp_str:
                                    try:
                                        # Handle both timezone-aware and naive timestamps
                                        # First, ensure timestamp_str is a string
                                        if not isinstance(timestamp_str, str):
                                            # If it's not a string, try to convert or skip
                                            print(f"Warning: timestamp is not a string: {timestamp_str} (type: {type(timestamp_str)})")
                                            # On error, keep the memory (don't prune)
                                            continue
                                        
                                        if timestamp_str.endswith('Z'):
                                            timestamp_str = timestamp_str[:-1] + '+00:00'
                                        timestamp = datetime.fromisoformat(timestamp_str)
                                        # Ensure timezone-aware (assume UTC if naive)
                                        if timestamp.tzinfo is None:
                                            timestamp = timestamp.replace(tzinfo=timezone.utc)
                                        else:
                                            timestamp = timestamp.astimezone(timezone.utc)
                                        
                                        # Check age
                                        if timestamp < cutoff_date:
                                            # Check score (need to score the event)
                                            event_score = score.score_event(event)
                                            if event_score < PRUNE_SCORE_THRESHOLD:
                                                should_prune = True
                                    except Exception as e:
                                        print(f"Error parsing timestamp in {filepath}:{line_num}: {e}")
                                        # On error, keep the memory (don't prune)
                                
                                if should_prune:
                                    pruned_lines.append(line)
                                    pruned += 1
                                else:
                                    kept_lines.append(line)
                                    
                            except json.JSONDecodeError as e:
                                print(f"Invalid JSON in {filepath}:{line_num}: {e}")
                                # Keep invalid JSON lines (safer)
                                kept_lines.append(line)
                    
                    # Write back kept lines or archive if dry_run=False
                    if dry_run:
                        # Just count what would be pruned
                        pass
                    else:
                        if len(pruned_lines) > 0:
                            # Archive the pruned lines
                            if pruned_lines:
                                with open(archive_filepath, 'a') as f:
                                    for line in pruned_lines:
                                        f.write(line + '\n')
                                
                                # Rewrite original file with kept lines
                                with open(filepath, 'w') as f:
                                    for line in kept_lines:
                                        f.write(line + '\n')
                                
                                archived += len(pruned_lines)
                        # If no lines pruned, keep original file
                        
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
    
    return pruned, archived

def get_pruning_stats():
    """Get statistics about pruning candidates"""
    if not _STORAGE_PATH:
        return {}
    
    stats = {
        'total_raw_memories': 0,
        'candidates_for_pruning': 0,
        'would_be_pruned': 0,
        'archive_size_mb': 0
    }
    
    raw_dir = os.path.join(_STORAGE_PATH, 'raw')
    archive_dir = os.path.join(_STORAGE_PATH, ARCHIVE_DIR, 'raw')
    
    # Count raw memories
    if os.path.exists(raw_dir):
        for filename in os.listdir(raw_dir):
            if filename.endswith('.jsonl'):
                filepath = os.path.join(raw_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    event = json.loads(line)
                                    if isinstance(event, dict):
                                        stats['total_raw_memories'] += 1
                                except json.JSONDecodeError:
                                    pass
                except Exception:
                    pass
    
    # Count archive size
    if os.path.exists(archive_dir):
        total_size = 0
        for filename in os.listdir(archive_dir):
            filepath = os.path.join(archive_dir, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
        stats['archive_size_mb'] = round(total_size / (1024 * 1024), 2)
    
    return stats

# Import timedelta at the top level to avoid issues
from datetime import timedelta