#!/usr/bin/env python3
"""
MemPalace System Verification Script
Performs comprehensive checks on MemPalace long-term memory layer.
Includes FAISS stale-vector detection and ID map cross-reference.
"""

import os
import subprocess
import sys
import json
from datetime import datetime


def print_header(text):
    print(f"\n{text}")
    print("=" * len(text))


def print_status(check, passed, details=""):
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"  {status}: {check}")
    if details and not passed:
        print(f"    {details}")


def count_chars_safe(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return len(f.read())
    except:
        return 0


def detect_stale_faiss_entries(mempalace_dir):
    """Cross-reference FAISS ID map against live raw store content."""
    raw_dir = os.path.join(mempalace_dir, 'raw')
    index_path = os.path.join(mempalace_dir, 'indexes', 'faiss.index')
    id_map_path = os.path.join(mempalace_dir, 'indexes', 'id_map.json')

    if not os.path.exists(index_path) or not os.path.exists(id_map_path):
        return None, "FAISS index or ID map missing"

    try:
        import faiss
        idx = faiss.read_index(index_path)
        with open(id_map_path) as f:
            id_map = json.load(f)
    except Exception as e:
        return None, f"FAISS read error: {e}"

    # Collect all live memory IDs from raw store
    live_ids = set()
    if os.path.exists(raw_dir):
        for fname in os.listdir(raw_dir):
            if fname == 'archive':
                continue
            fpath = os.path.join(raw_dir, fname)
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

    return {
        'total': idx.ntotal,
        'map_entries': len(id_map),
        'live_ids': len(live_ids),
        'stale_count': len(stale),
        'consistent': idx.ntotal == len(id_map),
        'stale_entries': stale[:10],
    }, None


def main():
    print_header("MEMPALACE SYSTEM VERIFICATION")
    print(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    # Paths
    mempalace_dir = os.path.expanduser('~/.hermes/mempalace')
    scripts_dir = os.path.join(mempalace_dir, 'scripts')
    memory_dir = os.path.expanduser('~/.hermes/memories')
    memory_file = os.path.join(memory_dir, 'MEMORY.md')
    user_file = os.path.join(memory_dir, 'USER.md')
    indexes_dir = os.path.join(mempalace_dir, 'indexes')
    faiss_index = os.path.join(indexes_dir, 'faiss.index')
    id_map_path = os.path.join(indexes_dir, 'id_map.json')

    all_passed = True

    # 1. Check MemPalace package
    print_header("1. SYSTEM INITIALIZATION")
    init_file = os.path.join(mempalace_dir, '__init__.py')
    init_exists = os.path.exists(init_file)
    print_status("MemPalace package initialized", init_exists,
                 f"File: {init_file}" if not init_exists else "")
    all_passed &= init_exists

    # 2. Check directory structure
    print_header("2. DIRECTORY STRUCTURE")
    dirs_to_check = ['raw', 'semantic', 'episodic', 'procedural', 'preferences', 'indexes', 'palace']
    for d in dirs_to_check:
        dir_path = os.path.join(mempalace_dir, d)
        exists = os.path.exists(dir_path)
        print_status(f"{d.capitalize()} directory exists", exists,
                     f"Path: {dir_path}" if not exists else "")
        all_passed &= exists

    # 3. Check component files
    print_header("3. COMPONENT FILES")
    components = ['capture', 'tag', 'score', 'consolidate', 'retrieve',
                  'reinforce', 'prune', 'explain', 'embed']
    for comp in components:
        comp_file = os.path.join(mempalace_dir, f'{comp}.py')
        exists = os.path.exists(comp_file)
        print_status(f"{comp.capitalize()} component", exists,
                     f"File: {comp_file}" if not exists else "")
        all_passed &= exists

    # 4. Check memory store usage
    print_header("4. HERMES MEMORY STORE STATUS")
    memory_chars = count_chars_safe(memory_file)
    user_chars = count_chars_safe(user_file)
    total_chars = memory_chars + user_chars
    capacity = 2200
    usage_percent = (total_chars / capacity) * 100

    print(f"  MEMORY.md: {memory_chars} characters")
    print(f"  USER.md: {user_chars} characters")
    print(f"  TOTAL: {total_chars} characters")
    print(f"  CAPACITY: {capacity} characters")
    print(f"  USAGE: {usage_percent:.1f}%")

    if usage_percent > 90:
        print_status("Memory store usage", False,
                     "Approaching capacity limit (>90%)")
        all_passed = False
    elif usage_percent > 75:
        print_status("Memory store usage", True,
                     "Moderate usage (75-90%) - consider monitoring")
    else:
        print_status("Memory store usage", True,
                     "Healthy usage (<75%)")

    # 5. Check FAISS index and ID map (with stale-vector detection)
    print_header("5. FAISS VECTOR STORE")
    index_exists = os.path.exists(faiss_index)
    id_map_exists = os.path.exists(id_map_path)
    print_status("FAISS index file exists", index_exists,
                 f"File: {faiss_index}" if not index_exists else "")
    print_status("ID map file exists", id_map_exists,
                 f"File: {id_map_path}" if not id_map_exists else "")
    all_passed &= index_exists and id_map_exists

    if index_exists and id_map_exists:
        try:
            import faiss
            index = faiss.read_index(faiss_index)
            with open(id_map_path, 'r') as f:
                id_map_data = json.load(f)

            print(f"  Index type: {type(index).__name__}")
            print(f"  Dimension: {index.d}")
            print(f"  Vectors in index: {index.ntotal}")
            print(f"  Entries in ID map: {len(id_map_data)}")

            # Check consistency
            consistent = index.ntotal == len(id_map_data)
            print_status("FAISS index and ID map consistency", consistent,
                         f"Index vectors ({index.ntotal}) != ID map entries ({len(id_map_data)})"
                         if not consistent else "")
            all_passed &= consistent

            # Check for stale FAISS entries
            print()
            print(f"  Checking FAISS stale-vector cross-reference...")
            stale_result, stale_error = detect_stale_faiss_entries(mempalace_dir)
            if stale_error:
                print_status("FAISS stale-vector detection", False, stale_error)
                all_passed = False
            else:
                stale_ok = stale_result['stale_count'] == 0
                print(f"  Live raw records: {stale_result['live_ids']}")
                print(f"  Stale FAISS entries: {stale_result['stale_count']}")
                print_status("No stale FAISS vectors", stale_ok,
                             f"{stale_result['stale_count']} entries point to deleted/archived content" if not stale_ok else "")
                if stale_result['stale_entries']:
                    for fid, mid in stale_result['stale_entries']:
                        print(f"    [{fid}] -> {mid}")
                all_passed &= stale_ok

        except Exception as e:
            print_status("FAISS index validation", False, f"Error: {e}")
            all_passed = False

    # 6. Run maintenance check
    print_header("6. MAINTENANCE FUNCTIONALITY")
    cron_maintenance = os.path.join(scripts_dir, 'cron_maintenance.py')
    if os.path.exists(cron_maintenance):
        try:
            result = subprocess.run([sys.executable, cron_maintenance],
                                    capture_output=True, text=True, timeout=30)
            maint_success = result.returncode == 0
            print_status("Cron maintenance execution", maint_success,
                         f"Exit code: {result.returncode}" if not maint_success else "")
            if not maint_success:
                print(f"  STDERR: {result.stderr[:200]}")
            all_passed &= maint_success
        except Exception as e:
            print_status("Cron maintenance execution", False, f"Error: {e}")
            all_passed = False
    else:
        print_status("Cron maintenance script", False, f"File not found: {cron_maintenance}")
        all_passed = False

    # 7. Check recent logs
    print_header("7. RECENT ACTIVITY")
    logs_dir = os.path.join(mempalace_dir, 'logs')
    if os.path.exists(logs_dir):
        log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
        if log_files:
            latest_log = sorted(log_files)[-1]
            log_path = os.path.join(logs_dir, latest_log)
            try:
                with open(log_path, 'r') as f:
                    lines = f.readlines()
                    recent_lines = lines[-2:] if len(lines) >= 2 else lines
                print_status("Log files accessible", True,
                             f"Latest log: {latest_log}")
                for line in recent_lines:
                    print(f"  {line.rstrip()}")
            except Exception as e:
                print_status("Log files accessible", False, f"Error reading log: {e}")
                all_passed = False
        else:
            print_status("Log files available", False, "No log files found")
    else:
        print_status("Logs directory", False, f"Directory not found: {logs_dir}")

    print_header("VERIFICATION SUMMARY")
    if all_passed:
        print("✓ ALL CHECKS PASSED - MemPalace system is operational")
        return 0
    else:
        print("✗ SOME CHECKS FAILED - See details above")
        print("")
        print("Action items:")
        print("  1. If stale FAISS vectors detected: run cleanup_extractions.py --rebuild-only")
        print("  2. If memory store >90%: run Memory-Full Offload Procedure")
        print("  3. See references/faiss-stale-vectors.md for recovery steps")
        return 1


if __name__ == "__main__":
    sys.exit(main())