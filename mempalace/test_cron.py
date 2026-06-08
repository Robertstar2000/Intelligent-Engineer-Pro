#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".hermes", "mempalace"))
import mempalace
from datetime import datetime, timezone

def main():
    print("=== MemPalace Cron Job Test ===")
    # Initialize
    mempalace.init_mempalace()
    print(f"Storage: {mempalace.get_storage_path()}")
    
    # Capture a test event representing this cron run
    event = {
        'type': 'cron_job',
        'content': 'MemPalace maintenance cron job executed at ' + datetime.now(timezone.utc).isoformat(),
        'context': 'Hermes Agent scheduled maintenance',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
    event_id = mempalace.capture_memory(event)
    print(f"Captured event ID: {event_id}")
    
    # Retrieve recent memories
    memories = mempalace.retrieve_memory('cron job maintenance', k=5)
    print(f"Retrieved {len(memories)} memories")
    for i, mem in enumerate(memories):
        layer = mem.get('retrieval_layer', 'unknown')
        content = mem.get('content', str(mem))[:100]
        print(f"  {i+1}. [{layer}] {content}")
    
    # Get stats
    from mempalace import embed
    stats = embed.get_index_stats()
    print(f"FAISS vectors: {stats.get('total_vectors', 0)}")
    print(f"ID map entries: {stats.get('id_map_entries', 0)}")
    
    # Run consolidation and pruning (lightweight)
    from mempalace import capture, score, consolidate, prune
    recent = capture.load_recent_events(days=1)
    print(f"Recent events (last day): {len(recent)}")
    if recent:
        scored = score.score_events(recent)
        print(f"Scored events: {len(scored)}")
        consolidated = consolidate.consolidate_memories(scored)
        print(f"Consolidated: {consolidated}")
        pruned = prune.prune_memories(dry_run=False)
        print(f"Pruned: {pruned['pruned']}, Archived: {pruned['archived']}")
    
    # Final stats
    raw_dir = os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "raw")
    raw_count = 0
    if os.path.exists(raw_dir):
        for f in os.listdir(raw_dir):
            if f.endswith('.jsonl'):
                with open(os.path.join(raw_dir, f), 'r') as fp:
                    for line in fp:
                        if line.strip():
                            raw_count += 1
    print(f"Final raw memories: {raw_count}")
    semantic = len([f for f in os.listdir(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "semantic")) if f.endswith('.json')]) if os.path.exists(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "semantic")) else 0
    episodic = len([f for f in os.listdir(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "episodic")) if f.endswith('.json')]) if os.path.exists(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "episodic")) else 0
    procedural = len([f for f in os.listdir(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "procedural")) if f.endswith('.json')]) if os.path.exists(os.path.join(os.path.expanduser("~"), ".hermes", "mempalace", "procedural")) else 0
    print(f"Semantic: {semantic}, Episodic: {episodic}, Procedural: {procedural}")

if __name__ == "__main__":
    main()