# FAISS Stale Vector Detection & Recovery

When raw store files are archived (by cleanup_extractions.py or manual moves), the FAISS index retains vectors pointing to those deleted records. These are **stale vectors** — they still match semantic queries but return memory IDs that no longer exist in the raw store.

## Detection Script

Run this to cross-reference the FAISS ID map against live content:

```python
import json, os, faiss

storage = os.path.expanduser('~/.hermes/mempalace')
raw_dir = os.path.join(storage, 'raw')
idx = faiss.read_index(os.path.join(storage, 'indexes', 'faiss.index'))
with open(os.path.join(storage, 'indexes', 'id_map.json')) as f:
    id_map = json.load(f)

# Collect all memory IDs from raw store (.json + .jsonl)
live_ids = set()
for fname in os.listdir(raw_dir):
    if fname == 'archive':
        continue
    fpath = os.path.join(raw_dir, fname)
    if fname.endswith('.json'):
        try:
            d = json.load(open(fpath))
            mid = d.get('memory_id') or d.get('id')
            if mid: live_ids.add(str(mid))
        except Exception:
            pass
    elif fname.endswith('.jsonl'):
        try:
            for line in open(fpath):
                line = line.strip()
                if not line: continue
                evt = json.loads(line)
                if isinstance(evt, dict):
                    mid = evt.get('memory_id') or evt.get('id') or evt.get('event_id')
                    if mid: live_ids.add(str(mid))
        except Exception:
            pass

stale = [(fid, mid) for fid, mid in id_map.items() if mid not in live_ids]
print(f"FAISS: {idx.ntotal} vectors, ID map: {len(id_map)} entries")
print(f"Live raw records: {len(live_ids)}")
print(f"Stale entries: {len(stale)}")
for fid, mid in stale[:10]:
    print(f"  [{fid}] -> {mid}")
if len(stale) > 10:
    print(f"  ... and {len(stale) - 10} more")
```

## Analysis

| Scenario | Likely cause | Action |
|----------|-------------|--------|
| All entries live | Clean system | No action |
| Stale entries are "Chapter_*" or "mem_*" IDs | Extraction cleanup archived raw files but FAISS wasn't rebuilt | Run `--rebuild-only` |
| Stale entries from bulk imports | Bulk import happened, then raw files were pruned | Run full cleanup |
| FAISS count mismatches ID map count | Index corruption or interrupted write | Rebuild from scratch |

## Recovery

### Option A: Rebuild from all current raw content (safe)
```bash
cd ~/.hermes/mempalace/scripts
python3 cleanup_extractions.py --rebuild-only
```

### Option B: Mark stale entries for lazy rebuild (no-op)
The `remove_embedding()` function in embed.py is a pass-through (`# Simplified: mark for lazy rebuild`). Call it on each stale memory ID — it won't remove the vector but the nightly rebuild (if configured) will skip those IDs.

### Option C: Full reset
```bash
cd ~/.hermes/mempalace/scripts
python3 cleanup_extractions.py  # archives + rebuilds
```

## Prevention Checklist

- After any archive/cleanup operation, **always** run `detect_stale_faiss_entries()` or the cross-reference script above
- Keep `cleanup_extractions.py` compatible with the current raw store format (.jsonl)
- Never manually delete raw files without rebuilding FAISS
- Periodically (weekly) check for stale vectors as part of cron maintenance
