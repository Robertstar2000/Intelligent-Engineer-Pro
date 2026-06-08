#!/usr/bin/env python3
"""
Prune low-value memories from MemPalace stores.
"""
import json
import os
import sys
from datetime import datetime, timezone
import time

def calculate_memory_value(memory_data):
    """
    Calculate the overall value of a memory for pruning decisions.
    Higher value = less likely to be pruned.
    """
    # Factors that increase value:
    # - reinforcement count (more used = more valuable)
    # - confidence (higher confidence = more valuable)
    # - recency (more recent = more valuable)
    # - score (original scoring)
    # - semantic/procedural types (more valuable than episodic/raw)
    
    reinforcement_count = memory_data.get('reinforcement_count', 0)
    confidence = memory_data.get('confidence', 0.5)
    score = memory_data.get('score', 0.5)  # Original score if available
    
    # Recency factor
    timestamp_str = memory_data.get('timestamp', '')
    try:
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        event_time = datetime.fromisoformat(timestamp_str)
        now = datetime.now(timezone.utc)
        days_old = (now - event_time).total_seconds() / (24 * 3600)
        # Recency score: newer memories get higher value
        recency_factor = max(0.1, math.exp(-days_old / 180))  # Half-life of ~180 days
    except:
        recency_factor = 0.5
    
    # Type factor: semantic and procedural are more valuable
    memory_type = memory_data.get('memory_type', memory_data.get('provisional_type', 'episodic'))
    type_weights = {
        'semantic': 1.0,
        'procedural': 0.9,
        'preferences': 0.85,
        'episodic': 0.6,
        'task-state': 0.5
    }
    type_factor = type_weights.get(memory_type, 0.5)
    
    # Combined value score (0-1 range, higher = more valuable)
    # Normalize reinforcement count (assume >10 is max benefit)
    reinforcement_norm = min(1.0, reinforcement_count / 10.0)
    
    value = (
        0.3 * reinforcement_norm +
        0.25 * confidence +
        0.2 * score +
        0.15 * recency_factor +
        0.1 * type_factor
    )
    
    return min(1.0, max(0.0, value))

def should_prune_memory(memory_data, max_age_days=365, min_value_threshold=0.2):
    """
    Determine if a memory should be pruned based on age and value.
    """
    # Never prune certain types of memories
    protected_types = ['semantic', 'procedural']  # Core knowledge types
    memory_type = memory_data.get('memory_type', memory_data.get('provisional_type', ''))
    
    if memory_type in protected_types:
        # Even protected memories can be pruned if extremely low value and very old
        if memory_data.get('reinforcement_count', 0) == 0:
            # Check age and value
            timestamp_str = memory_data.get('timestamp', '')
            try:
                if timestamp_str.endswith('Z'):
                    timestamp_str = timestamp_str[:-1] + '+00:00'
                event_time = datetime.fromisoformat(timestamp_str)
                now = datetime.now(timezone.utc)
                days_old = (now - event_time).total_seconds() / (24 * 3600)
                
                if days_old > max_age_days * 2:  # Only prune if very old (2x threshold)
                    value = calculate_memory_value(memory_data)
                    if value < min_value_threshold * 0.5:  # Much lower threshold for protected
                        return True, f"Protected type but very old ({days_old:.0f} days) and very low value ({value:.3f})"
            except:
                pass
        return False, "Protected memory type"
    
    # Check age
    timestamp_str = memory_data.get('timestamp', '')
    try:
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        event_time = datetime.fromisoformat(timestamp_str)
        now = datetime.now(timezone.utc)
        days_old = (now - event_time).total_seconds() / (24 * 3600)
        
        if days_old > max_age_days:
            value = calculate_memory_value(memory_data)
            if value < min_value_threshold:
                return True, f"Old ({days_old:.0f} days) and low value ({value:.3f})"
    except:
        # If we can't parse timestamp, be conservative and don't prune
        return False, "Unable to determine age"
    
    return False, "Does not meet pruning criteria"

def prune_store(store_dir, max_age_days=365, min_value_threshold=0.2, 
                archive_instead_of_delete=False):
    """
    Prune memories from a specific store.
    """
    if not os.path.exists(store_dir):
        return 0, 0
    
    pruned_count = 0
    archived_count = 0
    
    # Create archive directory if needed
    if archive_instead_of_delete:
        archive_dir = os.path.join(os.path.dirname(store_dir), f"{os.path.basename(store_dir)}_archive")
        os.makedirs(archive_dir, exist_ok=True)
    
    for filename in os.listdir(store_dir):
        if not filename.endswith('.json'):
            continue
            
        filepath = os.path.join(store_dir, filename)
        try:
            with open(filepath, 'r') as f:
                memory_data = json.load(f)
            
            should_prune, reason = should_prune_memory(memory_data, max_age_days, min_value_threshold)
            
            if should_prune:
                if archive_instead_of_delete:
                    # Move to archive
                    archive_path = os.path.join(archive_dir, filename)
                    os.rename(filepath, archive_path)
                    archived_count += 1
                    print(f"Archived {filename}: {reason}")
                else:
                    # Delete permanently
                    os.remove(filepath)
                    pruned_count += 1
                    print(f"Pruned {filename}: {reason}")
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}", file=sys.stderr)
    
    return pruned_count, archived_count

def prune_memories(max_age_days=365, min_value_threshold=0.2, 
                   archive_instead_of_delete=False):
    """
    Prune memories from all MemPalace stores.
    """
    base_dir = os.path.expanduser("~/.hermes/mempalace")
    store_types = ['raw', 'episodic', 'semantic', 'procedural', 'preferences']
    
    total_pruned = 0
    total_archived = 0
    
    print(f"Starting pruning process...")
    print(f"Max age: {max_age_days} days")
    print(f"Min value threshold: {min_value_threshold}")
    print(f"Archive instead of delete: {archive_instead_of_delete}")
    print()
    
    for store_type in store_types:
        store_dir = os.path.join(base_dir, store_type)
        if not os.path.exists(store_dir):
            print(f"Store {store_type} does not exist, skipping")
            continue
        
        print(f"Processing {store_type} store...")
        pruned, archived = prune_store(
            store_dir, 
            max_age_days=max_age_days,
            min_value_threshold=min_value_threshold,
            archive_instead_of_delete=archive_instead_of_delete
        )
        total_pruned += pruned
        total_archived += archived
        print(f"  {store_type}: {pruned} pruned, {archived} archived")
        print()
    
    print(f"Pruning complete!")
    print(f"Total pruned: {total_pruned}")
    print(f"Total archived: {total_archived}")
    
    return total_pruned, total_archived

if __name__ == "__main__":
    import math  # Import for calculate_memory_value function
    
    # Parse command line arguments
    max_age_days = 365
    min_value_threshold = 0.2
    archive_instead_of_delete = False
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--max-age" and i + 1 < len(sys.argv):
            try:
                max_age_days = int(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"Invalid max-age value: {sys.argv[i + 1]}", file=sys.stderr)
                sys.exit(1)
        elif arg == "--min-value" and i + 1 < len(sys.argv):
            try:
                min_value_threshold = float(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"Invalid min-value value: {sys.argv[i + 1]}", file=sys.stderr)
                sys.exit(1)
        elif arg == "--archive":
            archive_instead_of_delete = True
            i += 1
        elif arg == "--help":
            print("Usage: prune.py [--max-age DAYS] [--min-value THRESHOLD] [--archive]")
            print("  --max-age DAYS: Maximum age in days before considering for pruning (default: 365)")
            print("  --min-value THRESHOLD: Minimum value threshold (0-1) below which memories are pruned (default: 0.2)")
            print("  --archive: Archive memories instead of deleting them")
            sys.exit(0)
        else:
            print(f"Unknown argument: {arg}", file=sys.stderr)
            sys.exit(1)
    
    pruned, archived = prune_memories(
        max_age_days=max_age_days,
        min_value_threshold=min_value_threshold,
        archive_instead_of_delete=archive_instead_of_delete
    )
    
    # Exit with appropriate code
    sys.exit(0)
EOF