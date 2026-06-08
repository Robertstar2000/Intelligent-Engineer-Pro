#!/usr/bin/env python3
"""Run dedup-check.py tests"""
import subprocess, json, sys, os

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dedup-check.py")
REGISTRY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads-registry.json")

# Write initial registry
with open(REGISTRY, "w") as f:
    json.dump({"leads": [{
        "lead_key": "alice smith|acme corp|alice@acme.com",
        "source_pipeline": "web", "original_id": "1", "name": "Alice Smith",
        "organization": "Acme Corp", "email": "alice@acme.com",
        "current_stage": 1, "status": "active"
    }]}, f)

registry_data = json.load(open(REGISTRY))

def t(label, args=None, stdin=None):
    print(f"\n=== {label} ===")
    cmd = [sys.executable, SCRIPT] + (args or [])
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True, timeout=5, cwd=os.path.dirname(SCRIPT))
    if not p.stdout:
        print("NO OUTPUT - STDERR:", p.stderr)
        return {}
    r = json.loads(p.stdout)
    print(json.dumps(r, indent=2))
    return r

# 1 - Exact key match
r = t("1. Exact key match", ["Alice Smith", "Acme Corp", "alice@acme.com"])
assert r.get("is_duplicate") and r.get("layer") == "exact_key_match"

# 2 - Email match diff org
r = t("2. Email match (diff org)", ["Alice Smith", "Other Org", "alice@acme.com"])
assert r.get("is_duplicate")

# 3 - Same company, different person = NOT dup
r = t("3. Same co, diff person (NOT dup)", ["Bob Jones", "Acme Corp", "bob@acme.com"])
assert not r.get("is_duplicate")

# 4 - No match
r = t("4. No match", ["Charlie Brown", "Other Co", "charlie@other.com"])
assert not r.get("is_duplicate")

# 5 - Batch mode
bi = json.dumps([
    {"name":"Alice Smith","organization":"Acme Corp","email":"alice@acme.com"},
    {"name":"Bob Jones","organization":"Acme Corp","email":"bob@acme.com"},
    {"name":"New Person","organization":"Fresh Co","email":"new@fresh.com"}
])
r = t("5. Batch mode", stdin=bi)
assert r.get("duplicates_found") == 1 and r.get("total_checked") == 3

# 6 - Batch with leads wrapper
bi2 = json.dumps({"leads": [{"name":"Alice Smith","organization":"Acme Corp","email":"alice@acme.com"}]})
r = t("6. Batch with wrapper", stdin=bi2)
assert r.get("duplicates_found") == 1

# 7 - No registry CLI
os.unlink(REGISTRY)
r = t("7. No registry CLI", ["Alice Smith","Acme Corp","alice@acme.com"])
assert not r.get("is_duplicate")

# 8 - No registry batch
r = t("8. No registry batch", stdin=bi)
assert r.get("duplicates_found") == 0 and r.get("total_checked") == 3

# Restore
with open(REGISTRY, "w") as f: json.dump(registry_data, f)

# 9 - Domain+name match
r = t("9. Domain+name match", ["Alice Smith", "NewCo", "alice.smith@acme.com"])
assert r.get("is_duplicate") and r.get("layer") == "domain_plus_name_match"

# 10 - Case insensitivity
r = t("10. Case insensitivity", ["ALICE SMITH","ACME CORP","ALICE@ACME.COM"])
assert r.get("is_duplicate")

print("\n🎉 ALL 10 TESTS PASSED.")
