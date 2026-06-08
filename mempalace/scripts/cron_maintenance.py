#!/usr/bin/env python3
"""
MemPalace Cron Maintenance Script
Runs consolidation, pruning, and reports system statistics
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add the mempalace directory to path
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".hermes"))

import mempalace
from mempalace import consolidate, prune, explain, capture, score, tag, reinforce

def main():
    """Run maintenance operations"""
    print("=== MemPalace Cron Maintenance ===")
    start_time = datetime.now()
    
    try:
        # Initialize MemPalace
        print("Initializing MemPalace...")
        mempalace.init_mempalace()
        
        # Run consolidation
        print("\n1. Running consolidation...")
        # Load recent events (last 7 days)
        events = capture.load_recent_events(days=7)
        print(f"   Loaded {len(events)} recent events")
        
        if events:
            # Score events
            scored_events = score.score_events(events)
            print(f"   Scored {len(scored_events)} events")
            
            # Consolidate high-scoring memories
            consolidated_count = consolidate.consolidate_memories(scored_events)
            print(f"   Consolidated {consolidated_count} memories")
        else:
            print("   No recent events to consolidate")
            consolidated_count = 0
        
        # Run pruning
        print("\n2. Running pruning...")
        pruning_result = prune.prune_memories(dry_run=False)
        print(f"   Pruned: {pruning_result['pruned']} memories")
        print(f"   Archived: {pruning_result['archived']} memories")
        
        # Get system statistics
        print("\n3. System Statistics:")
        
        # Raw memories stats
        raw_dir = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "raw")
        raw_count = 0
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
                                            raw_count += 1
                                    except json.JSONDecodeError:
                                        pass
                    except Exception:
                        pass
        print(f"   Raw memories: {raw_count}")
        
        # Consolidated memories stats
        semantic_count = len([f for f in os.listdir(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "semantic")) if f.endswith('.json')]) if os.path.exists(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "semantic")) else 0
        episodic_count = len([f for f in os.listdir(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "episodic")) if f.endswith('.json')]) if os.path.exists(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "episodic")) else 0
        procedural_count = len([f for f in os.listdir(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "procedural")) if f.endswith('.json')]) if os.path.exists(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "procedural")) else 0
        print(f"   Semantic memories: {semantic_count}")
        print(f"   Episodic memories: {episodic_count}")
        print(f"   Procedural memories: {procedural_count}")
        
        # Embedding index stats
        from mempalace import embed
        index_stats = embed.get_index_stats()
        print(f"   FAISS index vectors: {index_stats.get('total_vectors', 0)}")
        print(f"   ID map entries: {index_stats.get('id_map_entries', 0)}")
        
        # Reinforcement stats
        reinforced_memories = reinforce.get_reinforced_memories(limit=10)
        print(f"   Top reinforced memories: {len(reinforced_memories)}")
        
        # Explanation stats
        explanation_stats = explain.get_explanation_stats()
        print(f"   Total explanations logged: {explanation_stats.get('total_explanations', 0)}")
        
        # Archive size
        archive_dir = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "archive", "raw")
        archive_size_mb = 0
        if os.path.exists(archive_dir):
            total_size = 0
            for filename in os.listdir(archive_dir):
                filepath = os.path.join(archive_dir, filename)
                if os.path.isfile(filepath):
                    total_size += os.path.getsize(filepath)
            archive_size_mb = round(total_size / (1024 * 1024), 2)
        print(f"   Archive size: {archive_size_mb} MB")
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"\nMaintenance completed in {duration:.2f} seconds")
        
        return 0
        
    except Exception as e:
        print(f"ERROR during maintenance: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())