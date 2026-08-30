#!/usr/bin/env python3
"""
Clean up extraction-noise bloat in MemPalace raw store.

This script:
1. Identifies all file_extraction raw events (stored as .jsonl lines)
2. Archives them to raw/archive/ for safekeeping
3. Rebuilds the FAISS index from only meaningful memory events
4. Reports before/after stats and detects stale FAISS entries

Works with BOTH old .json-per-event format and current .jsonl (event-per-line) format.
Includes stale-vector detection after rebuild.

Usage:
  python3 cleanup_extractions.py [--dry-run]
  python3 cleanup_extractions.py [--rebuild-only]
"""

import json
import os
import sys
import shutil
from datetime import datetime, timezone

STORAGE_PATH = os.path.expanduser('~/.hermes/mempalace')
RAW_DIR = os.path.join(STORAGE_PATH, 'raw')
ARCHIVE_DIR = os.path.join(STORAGE_PATH, 'raw', 'archive')
INDEX_DIR = os.path.join(STORAGE_PATH, 'indexes')


def classify_json_file(fpath):
    """Classify a single .json file (old format). Returns ('extraction'|'meaningful'|'error', data)."""
    try:
        with open(fpath) as fh:
            data = json.load(fh)
        source = data.get('source_type', '')
        if source == 'file_extraction':
            return ('extraction', data)
        else:
            return ('meaningful', data)
    except Exception as e:
        return ('error', str(e))


def classify_jsonl_file(fpath):
    """Classify events in a .jsonl file (current format). Returns (extractions, meaningfuls, errors)."""
    extractions = []
    meaningful = []
    errors = []
    try:
        with open(fpath) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict):
                        meaningful.append(event)
                        continue
                    st = event.get('source_type', event.get('type', 'unknown'))
                    if st == 'file_extraction':
                        extractions.append(event)
                    else:
                        meaningful.append(event)
                except json.JSONDecodeError as e:
                    errors.append((line[:50], str(e)))
    except Exception as e:
        errors.append((os.path.basename(fpath), str(e)))
    return extractions, meaningful, errors


def scan_raw_store():
    """Scan raw/ directory, classifying all files by format."""
    extraction_entries = []
    meaningful_entries = []
    error_files = []
    total_size = 0

    for fname in sorted(os.listdir(RAW_DIR)):
        if fname == 'archive':
            continue
        fpath = os.path.join(RAW_DIR, fname)

        if fname.endswith('.json'):
            cls, data = classify_json_file(fpath)
            if cls == 'extraction':
                extraction_entries.append((fname, data))
                total_size += os.path.getsize(fpath)
            elif cls == 'meaningful':
                meaningful_entries.append((fname, data))
            else:
                error_files.append(fname)

        elif fname.endswith('.jsonl'):
            ex, mn, err = classify_jsonl_file(fpath)
            if ex:
                extraction_entries.append((fname, ex))
                total_size += os.path.getsize(fpath)
            if mn:
                meaningful_entries.append((fname, mn))
            if err:
                error_files.append((fname, err))

    return extraction_entries, meaningful_entries, error_files, total_size


def archive_files(extraction_entries, dry_run=True):
    """Archive files containing extraction events. Handles dedup."""
    if not extraction_entries:
        print("  No extraction files to archive.")
        return 0

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    moved = 0
    archived = set()

    for entry in extraction_entries:
        fname = entry[0]
        if fname in archived:
            continue
        archived.add(fname)
        src = os.path.join(RAW_DIR, fname)
        if not os.path.exists(src):
            continue
        dst = os.path.join(ARCHIVE_DIR, fname)
        if dry_run:
            moved += 1
        else:
            shutil.move(src, dst)
            moved += 1

    return moved


def count_events_in_entries(entries):
    """Count total events across entries (handles both .json dict and .jsonl list)."""
    count = 0
    for _, data in entries:
        if isinstance(data, list):
            count += len(data)
        else:
            count += 1
    return count


def rebuild_faiss_index(dry_run=True):
    """Rebuild FAISS index from all current raw content."""
    sys.path.insert(0, STORAGE_PATH)

    try:
        import numpy as np
        import faiss
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        print(f"  ERROR: Missing dependency: {e}")
        return False

    model_name = 'all-MiniLM-L6-v2'
    try:
        model = SentenceTransformer(model_name)
        dim = model.get_embedding_dimension()
        print(f"  Loaded model '{model_name}' (dim={dim})")
    except Exception as e:
        print(f"  ERROR: Failed to load model: {e}")
        return False

    # Collect all texts and IDs from current raw store
    texts = []
    memory_ids = []

    for fname in sorted(os.listdir(RAW_DIR)):
        if fname == 'archive':
            continue
        fpath = os.path.join(RAW_DIR, fname)

        if fname.endswith('.json'):
            try:
                with open(fpath) as f:
                    d = json.load(f)
                text = d.get('raw_text') or d.get('content', '')
                if text:
                    texts.append(text)
                    memory_ids.append(d.get('memory_id', d.get('id', fname.replace('.json', ''))))
            except Exception:
                pass

        elif fname.endswith('.jsonl'):
            try:
                with open(fpath) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        evt = json.loads(line)
                        if not isinstance(evt, dict):
                            continue
                        text = evt.get('raw_text') or evt.get('content', '')
                        if text:
                            texts.append(text)
                            memory_ids.append(evt.get('memory_id', evt.get('id', evt.get('event_id', ''))))
            except Exception:
                pass

    if dry_run:
        print(f"  [DRY RUN] Would rebuild FAISS index with {len(texts)} vectors. Skipping encoding.")
        return True

    if not texts:
        print("  No meaningful texts to index. Resetting FAISS index to empty.")
        index = faiss.IndexFlatIP(dim)
        id_map = {}
    else:
        print(f"  Encoding {len(texts)} memories...")
        embeddings = model.encode(texts, normalize_embeddings=True)
        index = faiss.IndexFlatIP(dim)
        id_map = {}
        for i, mid in enumerate(memory_ids):
            if mid:
                try:
                    index.add(np.array([embeddings[i]]))
                    id_map[str(i)] = mid
                except Exception as e:
                    print(f"  WARNING: Failed to add vector for {mid}: {e}")

        print(f"  Built FAISS index with {index.ntotal} vectors, {len(id_map)} ID map entries")

    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, os.path.join(INDEX_DIR, 'faiss.index'))
    with open(os.path.join(INDEX_DIR, 'id_map.json'), 'w') as f:
        json.dump(id_map, f)
    print(f"  Persisted: faiss.index + id_map.json")
    return True


def detect_stale_faiss_entries():
    """Check for FAISS entries pointing to non-existent raw content."""
    index_path = os.path.join(INDEX_DIR, 'faiss.index')
    id_map_path = os.path.join(INDEX_DIR, 'id_map.json')

    if not os.path.exists(index_path) or not os.path.exists(id_map_path):
        return []

    try:
        import faiss
        idx = faiss.read_index(index_path)
        with open(id_map_path) as f:
            id_map = json.load(f)
    except Exception:
        return []

    # Collect all memory IDs currently in raw store
    live_ids = set()
    if os.path.exists(RAW_DIR):
        for fname in os.listdir(RAW_DIR):
            if fname == 'archive':
                continue
            fpath = os.path.join(RAW_DIR, fname)
            if fname.endswith('.json'):
                try:
                    with open(fpath) as f:
                        d = json.load(f)
                    mid = d.get('memory_id') or d.get('id')
                    if mid:
                        live_ids.add(str(mid))
                except Exception:
                    pass
            elif fname.endswith('.jsonl'):
                try:
                    with open(fpath) as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            evt = json.loads(line)
                            if isinstance(evt, dict):
                                mid = evt.get('memory_id') or evt.get('id') or evt.get('event_id')
                                if mid:
                                    live_ids.add(str(mid))
                except Exception:
                    pass

    stale = []
    for fid, mid in id_map.items():
        if mid not in live_ids:
            stale.append((fid, mid))

    return stale


def print_faiss_verify_cmd():
    """Print the FAISS verification command users can run."""
    print()
    print("To verify ID map consistency after cleanup:")
    print('  python3 -c """')
    print('    import json, os, faiss')
    print("    idx = faiss.read_index(os.path.expanduser('~/.hermes/mempalace/indexes/faiss.index'))")
    print("    idm = json.load(open(os.path.expanduser('~/.hermes/mempalace/indexes/id_map.json')))")
    print("    print(f'Vectors: {idx.ntotal}, Map: {len(idm)}')")
    print("    print('Consistent' if idx.ntotal == len(idm) else 'MISMATCH')")
    print('  """')


def main():
    dry_run = '--dry-run' in sys.argv
    rebuild_only = '--rebuild-only' in sys.argv

    print(f"{'='*60}")
    print(f"MemPalace Extraction Cleanup")
    print(f"{'='*60}")
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE'}")
    if rebuild_only:
        print(f"Sub-mode: --rebuild-only (skip archive, rebuild FAISS from all raw content)")
    print()

    if not rebuild_only:
        # Step 1: Scan raw store
        print("Step 1: Scanning raw store...")
        extraction, meaningful, errors, total_size = scan_raw_store()
        extraction_count = count_events_in_entries(extraction)
        meaningful_count = count_events_in_entries(meaningful)
        print(f"  Extraction noise events: {extraction_count}")
        print(f"  Meaningful events: {meaningful_count}")
        print(f"  Parse errors: {len(errors)}")
        print(f"  Extraction data size: {total_size / 1024:.1f} KB")

        if not extraction:
            print("\n  No extraction noise found. Proceeding to FAISS rebuild only.")
            rebuild_only = True
        else:
            # Step 2: Archive extraction files
            print("\nStep 2: Archiving extraction files...")
            moved = archive_files(extraction, dry_run)
            print(f"  {'Would archive' if dry_run else 'Archived'}: {moved} files")

    # Step 3: Rebuild FAISS index
    print("\nStep 3: Rebuilding FAISS index from raw store...")
    ok = rebuild_faiss_index(dry_run)
    if not ok:
        print("  FAISS rebuild failed!")
        return 1

    # Step 4: Check for stale FAISS entries
    if not dry_run:
        print("\nStep 4: Checking for stale FAISS entries...")
        stale = detect_stale_faiss_entries()
        if stale:
            print(f"  Stale FAISS entries: {len(stale)} (pointing to archived/deleted content)")
            for fid, mid in stale[:5]:
                print(f"    [{fid}] -> {mid}")
            if len(stale) > 5:
                print(f"    ... and {len(stale) - 5} more")
        else:
            print("  Stale FAISS entries: 0 (all point to live content)")

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    if not rebuild_only:
        print(f"  Extraction events processed")
    print(f"  FAISS index rebuilt from raw store")
    print(f"{'='*60}")

    if dry_run:
        print("\nTo apply: run without --dry-run")
        print(f"  python3 cleanup_extractions.py")

    print_faiss_verify_cmd()
    return 0


if __name__ == '__main__':
    sys.exit(main())
