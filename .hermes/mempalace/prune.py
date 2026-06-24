"""MemPalace Pruning System - Memory pruning with archiving."""

import json
import os
import shutil
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple
import sys

# Add the mempalace directory to path for imports
sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))

try:
    from score import score_memory
except ImportError as e:
    print(f"Warning: Could not import MemPalace modules: {e}")
    # Define fallback function
    def score_memory(event, weights=None): return 0.5, {}

_storage_path: str = None

# Pruning thresholds
PRUNE_THRESHOLD_LOW_SCORE = 0.2      # Memories below this score are candidates for pruning
PRUNE_MAX_AGE_DAYS = 365             # Memories older than this are candidates for pruning
PRUNE_REINFORCEMENT_MIN = 0          # Minimum reinforcements to avoid pruning

def init_pruning(storage_path: str):
    """Initialize the pruning system."""
    global _storage_path
    _storage_path = storage_path
    
    # Create archive directory
    archive_dir = os.path.join(_storage_path, 'raw', 'archive')
    os.makedirs(archive_dir, exist_ok=True)
    
    print(f"Pruning system initialized at {_storage_path}")

def _is_old_enough_to_prune(timestamp_str: str, max_age_days: int) -> bool:
    """
    Check if a memory is old enough to be considered for pruning.
    
    Args:
        timestamp_str: ISO format timestamp string
        max_age_days: Maximum age in days before pruning consideration
        
    Returns:
        bool: True if memory is old enough for pruning consideration
    """
    try:
        # Parse timestamp - handle both timezone-aware and naive
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        event_time = datetime.fromisoformat(timestamp_str)
        # Ensure timezone aware (assume UTC if naive)
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        age_days = (now - event_time).total_seconds() / (3600 * 24)
        return age_days > max_age_days
    except Exception:
        # If parsing fails, err on the side of caution (don't prune)
        return False

def should_prune_memory(event: Dict[Any, Any], score: float, individual_scores: Dict[str, float]) -> bool:
    """
    Determine if a memory should be pruned based on score, age, and usage.
    
    Args:
        event: Event dictionary
        score: Composite memory score
        individual_scores: Individual component scores
        
    Returns:
        bool: True if memory should be pruned
    """
    # Never prune memories with skip_pruning flag
    if event.get('skip_pruning', False):
        return False
    
    # Never prune consolidated memories (they're already distilled)
    if event.get('memory_id'):  # Has a memory ID from consolidation
        return False
    
    # Check age
    timestamp_str = event.get('timestamp', event.get('captured_at', ''))
    if _is_old_enough_to_prune(timestamp_str, PRUNE_MAX_AGE_DAYS):
        # Old memories are more likely to be pruned
        age_factor = 0.7
    else:
        age_factor = 1.0
    
    # Check reinforcement (usage)
    event_id = event.get('event_id', '')
    reinforcement_count = 0  # Would need to check reinforcement system
    # For now, we'll skip this check and rely on score/age
    
    # Low score memories are prime candidates
    if score < PRUNE_THRESHOLD_LOW_SCORE:
        return True
    
    # Very low usage combined with moderate score might warrant pruning
    # This would need integration with reinforcement system
    
    return False

def prune_memory(event: Dict[Any, Any], event_id: str) -> bool:
    """
    Prune a memory by moving it to archive.
    
    Args:
        event: Event dictionary to prune
        event_id: ID of the event
        
    Returns:
        bool: True if memory was pruned
    """
    if _storage_path is None:
        raise RuntimeError("Pruning system not initialized. Call init_pruning() first.")
    
    # Locate the raw event file
    raw_dir = os.path.join(_storage_path, 'raw')
    archive_dir = os.path.join(raw_dir, 'archive')
    
    # Look for the event file
    event_file = None
    for fname in os.listdir(raw_dir):
        if fname.endswith('.jsonl') and fname != 'archive':
            fpath = os.path.join(raw_dir, fname)
            try:
                with open(fpath, 'r') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            data = json.loads(line)
                            if isinstance(data, dict) and data.get('event_id') == event_id:
                                event_file = fpath
                                break
                        except json.JSONDecodeError:
                            continue
                if event_file:
                    break
            except Exception:
                continue
    
    if not event_file:
        return False
    
    # Move to archive (we'll implement a simple copy+delete approach for safety)
    # In a more sophisticated system, we might want to track what's archived
    archive_file = os.path.join(archive_dir, f'{event_id}.jsonl')
    
    try:
        # Copy the specific line to archive (simplified - archive whole file for now)
        shutil.copy2(event_file, archive_file)
        # Note: In production, we'd want to remove just this entry, not the whole file
        # For simplicity in this implementation, we'll just note that archiving happened
        return True
    except Exception:
        return False

def prune_memories() -> int:
    """
    Prune memories from raw store that meet criteria.
    
    Returns:
        int: Number of memories pruned
    """
    if _storage_path is None:
        raise RuntimeError("Pruning system not initialized. Call init_pruning() first.")
    
    pruned_count = 0
    raw_dir = os.path.join(_storage_path, 'raw')
    
    if not os.path.exists(raw_dir):
        return 0
    
    # Process all raw event files
    for fname in os.listdir(raw_dir):
        if not fname.endswith('.jsonl') or fname == 'archive':
            continue
        
        fpath = os.path.join(raw_dir, fname)
        try:
            # Read all lines first
            lines = []
            with open(fpath, 'r') as f:
                lines = f.readlines()
            
            # Process lines and keep those that shouldn't be pruned
            kept_lines = []
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    kept_lines.append(line)  # Keep empty lines
                    continue
                
                try:
                    event = json.loads(line)
                    # Skip if not a dict (handle legacy artifacts)
                    if not isinstance(event, dict):
                        kept_lines.append(line)
                        continue
                        
                    # Score the memory
                    composite_score, individual_scores = score_memory(event)
                    
                    # Check if should prune
                    if should_prune_memory(event, composite_score, individual_scores):
                        # Archive this event (simplified approach)
                        event_id = event.get('event_id', f'unknown_{line_num}')
                        if prune_memory(event, event_id):
                            pruned_count += 1
                            # Don't add to kept_lines (effectively removing it)
                            continue
                    
                    # Keep this line
                    kept_lines.append(line)
                    
                except json.JSONDecodeError:
                    # Keep invalid JSON lines (don't prune them)
                    kept_lines.append(line)
                except Exception as e:
                    # Keep lines that cause errors (don't prune them)
                    print(f"Error processing event in {fname}:{line_num}: {e}")
                    kept_lines.append(line)
            
            # Write back the kept lines
            with open(fpath, 'w') as f:
                for line in kept_lines:
                    f.write(line + '\n' if not line.endswith('\n') else line)
                        
        except Exception as e:
            print(f"Error processing raw file {fname}: {e}")
            continue
    
    return pruned_count

def get_archive_size() -> float:
    """
    Get size of archive in MB.
    
    Returns:
        float: Archive size in megabytes
    """
    if _storage_path is None:
        return 0.0
    
    archive_dir = os.path.join(_storage_path, 'raw', 'archive')
    if not os.path.exists(archive_dir):
        return 0.0
    
    total_size = 0
    try:
        for fname in os.listdir(archive_dir):
            fpath = os.path.join(archive_dir, fname)
            if os.path.isfile(fpath):
                total_size += os.path.getsize(fpath)
    except Exception:
        pass
    
    return total_size / (1024 * 1024)  # Convert to MB

def get_component_status() -> Dict[str, Any]:
    """Get status of pruning component."""
    return {
        'initialized': _storage_path is not None,
        'storage_path': _storage_path,
        'prune_threshold_low_score': PRUNE_THRESHOLD_LOW_SCORE,
        'prune_max_age_days': PRUNE_MAX_AGE_DAYS,
        'archive_size_mb': get_archive_size()
    }