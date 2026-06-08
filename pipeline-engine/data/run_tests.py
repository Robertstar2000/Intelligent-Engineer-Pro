#!/usr/bin/env python3
"""Test runner for dedup-check.py"""
import subprocess, json, sys, os

DIR = "/home/bob/.hermes/.openclaw/workspace/pipeline-engine/data"
SCRIPT = os.path.join(DIR, "dedup-check.py")
REG = os.path.join(DIR, "leads-registry.json")

REG_DATA = {"leads":[{"lead_key":"alice smith|acme corp|alice@acme.com","source_pipeline":"web","original_id":"1","name":"Alice Smith","organization":"Acme Corp","email":"alice@acme.com","current_stage":1,"status":"active"}]}

def write_reg():
    with open(REG, "w") as f:
        json.dump(REG_DATA, f)

write_reg()

results = {"passed": 0, "failed": 0}

def run(args=None, stdin=None):
    cmd = [sys.executable, SCRIPT] + (args or [])
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=5, cwd=DIR)
    if p.stderr:
        print("STDERR:", p.stderr.strip())
    if p.stdout:
        return json.loads(p.stdout)
    print("EMPTY STDOUT, exit:", p.returncode)
    return {}

def check(label, r, assertion):
    try:
        assertion(r)
        results["passed"] += 1
        print(f"{results['passed']}. {label} ✅")
    except AssertionError as e:
        results["failed"] += 1
        print(f"FAIL {label}: {e}")

check("Exact key match",
    run(["Alice Smith","Acme Corp","alice@acme.com"]),
    lambda r: r.get("is_duplicate") and r.get("layer")=="exact_key_match")

check("Email match",
    run(["Alice Smith","Other Org","alice@acme.com"]),
    lambda r: r.get("is_duplicate"))

check("Same co diff person NOT dup",
    run(["Bob Jones","Acme Corp","bob@acme.com"]),
    lambda r: not r.get("is_duplicate"))

check("No match",
    run(["Charlie Brown","Other Co","charlie@other.com"]),
    lambda r: not r.get("is_duplicate"))

check("Domain+name match",
    run(["Alice Smith","NewCo","alice.smith@acme.com"]),
    lambda r: r.get("is_duplicate") and r.get("layer")=="domain_plus_name_match")

bi = json.dumps([{"name":"Alice Smith","organization":"Acme Corp","email":"alice@acme.com"},{"name":"Bob Jones","organization":"Acme Corp","email":"bob@acme.com"}])

check("Batch mode",
    run(stdin=bi),
    lambda r: r.get("duplicates_found")==1 and r.get("total_checked")==2)

check("Batch wrapper",
    run(stdin=json.dumps({"leads":[{"name":"Alice Smith","organization":"Acme Corp","email":"alice@acme.com"}]})),
    lambda r: r.get("duplicates_found")==1)

os.unlink(REG)

check("No registry CLI",
    run(["Alice Smith","Acme Corp","alice@acme.com"]),
    lambda r: not r.get("is_duplicate"))

check("No registry batch",
    run(stdin=bi),
    lambda r: r.get("duplicates_found")==0 and r.get("total_checked")==2)

write_reg()

check("Case insensitivity",
    run(["ALICE SMITH","ACME CORP","ALICE@ACME.COM"]),
    lambda r: r.get("is_duplicate"))

print(f"\n{'🎉' if results['failed']==0 else '💥'} {results['passed']} passed, {results['failed']} failed")
sys.exit(results['failed'])
