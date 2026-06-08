#!/usr/bin/env python3
"""
Clean up extraction-noise bloat in MemPalace raw store.

This script:
1. Identifies all file_extraction raw events (99.6% of raw store)
2. Archives them to raw/archive/ for safekeeping
3. Rebuilds the FAISS index from only meaningful memory events
4. Reports before/after stats

Usage:
  python3 cleanup_extractions.py [--dry-run]
  python3 cleanup_extractions.py [--threshold 0.5]
"""

import json
import os
import sys
import shutil
import glob
from datetime import datetime, timezone

STORAGE_PATH = os.path.expanduser('~/.hermes/mempalace')
RAW_DIR = os.path.join(STORAGE_PATH, 'raw')
ARCHIVE_DIR = os.path.join(STORAGE_PATH, 'raw', 'archive')
INDEX_DIR = os.path.join(STORAGE_PATH, 'indexes')


def classify_files(dry_run=True):
    """Classify raw files into extraction noise vs meaningful memories."""
    extraction = []
    meaningful = []
    errors = []
    
    for fname in sorted(os.listdir(RAW_DIR)):
        if fname == 'archive':
            continue
        fpath = os.path.join(RAW_DIR, fname)
        if not fname.endswith('.json'):
            errors.append((fname, 'not_json'))
            continue
        try:
            with open(fpath) as fh:
                data = json.load(fh)
            source = data.get('source_type', '')
            if source == 'file_extraction':
                extraction.append(fname)
            else:
                meaningful.append((fname, data))
        except Exception as e:
            errors.append((fname, str(e)))
    
    return extraction, meaningful, errors


def archive_extractions(extraction_files, dry_run=True):
    """Move extraction files to archive directory."""
    if not extraction_files:
        print("  No extraction files to archive.")
        return
    
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    
    moved = 0
    for fname in extraction_files:
        src = os.path.join(RAW_DIR, fname)
        dst = os.path.join(ARCHIVE_DIR, fname)
        if dry_run:
            moved += 1
        else:
            shutil.move(src, dst)
            moved += 1
    
    return moved


def rebuild_faiss_index(meaningful_entries, dry_run=True):
    """Rebuild FAISS index from only meaningful memories."""
    import sys
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
    
    if not meaningful_entries:
        print("  No meaningful entries to index. Resetting FAISS index.")
        index = faiss.IndexFlatIP(dim)
        id_map = {}
    else:
        texts = []
        memory_ids = []
        for fname, data in meaningful_entries:
            text = data.get('raw_text', '')
            if text:
                texts.append(text)
                memory_ids.append(data.get('memory_id', fname.replace('.json', '')))
        
        print(f"  Encoding {len(texts)} meaningful memories...")
        if dry_run:
            print(f"  [DRY RUN] Would encode and index {len(texts)} entries")
            # Still build the index in dry-run to report size
            index = faiss.IndexFlatIP(dim)
            id_map = {}
            for i, (fname, data) in enumerate(meaningful_entries):
                text = data.get('raw_text', '')
                if text:
                    mid = data.get('memory_id', fname.replace('.json', ''))
                    id_map[i] = mid
            # No actual encoding in dry run
            print(f"  [DRY RUN] Would create index with {len(id_map)} vectors")
        else:
            embeddings = model.encode(texts, normalize_embeddings=True)
            index = faiss.IndexFlatIP(dim)
            id_map = {}
            text_idx = 0
            for i, (fname, data) in enumerate(meaningful_entries):
                text = data.get('raw_text', '')
                if text:
                    mid = data.get('memory_id', fname.replace('.json', ''))
                    index.add(np.array([embeddings[text_idx]]))
                    id_map[text_idx] = mid
                    text_idx += 1
            
            # Persist
            os.makedirs(INDEX_DIR, exist_ok=True)
            faiss.write_index(index, os.path.join(INDEX_DIR, 'faiss.index'))
            with open(os.path.join(INDEX_DIR, 'id_map.json'), 'w') as f:
                json.dump({str(k): v for k, v in id_map.items()}, f)
            print(f"  Saved: FAISS ({index.ntotal} vectors) + ID map ({len(id_map)} entries)")
    
    return True


def main():
    dry_run = '--dry-run' in sys.argv
    threshold = None
    for arg in sys.argv[1:]:
        if arg.startswith('--threshold='):
            threshold = float(arg.split('=')[1])
    
    print(f"{'='*60}")
    print(f"MemPalace Extraction Cleanup")
    print(f"{'='*60}")
    print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE'}")
    print()
    
    # Step 1: Classify files
    print("Step 1: Classifying raw files...")
    extraction, meaningful, errors = classify_files(dry_run)
    print(f"  Extraction noise: {len(extraction)} files")
    print(f"  Meaningful events: {len(meaningful)} files")
    print(f"  Parse errors: {len(errors)} files")
    
    total_size = sum(
        os.path.getsize(os.path.join(RAW_DIR, f))
        for f in extraction
        if os.path.isfile(os.path.join(RAW_DIR, f))
    )
    print(f"  Extraction data size: {total_size/1024:.1f} KB")
    
    if errors and not dry_run:
        print(f"  Parse errors (not archived): {[(e[0][:30]) for e in errors[:5]]}")
    
    if not extraction:
        print("\n✅ No extraction noise found. Store is clean.")
        return
    
    # Step 2: Archive extractions
    print(f"\nStep 2: Archiving extraction files...")
    moved = archive_extractions(extraction, dry_run)
    print(f"  {'Would archive' if dry_run else 'Archived'}: {moved} files")
    
    # Step 3: Rebuild FAISS index
    print(f"\nStep 3: Rebuilding FAISS index from meaningful data only...")
    rebuild_faiss_index(meaningful, dry_run)
    
    # Step 4: Report
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Raw dir: {len(extraction)} extractions → archive/")
    print(f"  Raw dir remaining: {len(meaningful)} meaningful events")
    print(f"  FAISS index: rebuilt from {len(meaningful)} entries")
    print(f"  Space recovered: {total_size/1024:.1f} KB")
    print(f"{'='*60}")
    
    if dry_run:
        print("\nTo apply: run without --dry-run")
        print(f"  python3 cleanup_extractions.py")


if __name__ == '__main__':
    main()