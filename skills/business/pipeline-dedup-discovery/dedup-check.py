#!/usr/bin/env python3
"""Dedup Checker — Pipeline Discovery Step.

Usage: python3 dedup-check.py <pipeline> <name> [organization] [email]

Checks if a lead already exists in the master registry.
Returns: {"is_duplicate": true/false, "match": {...} or null}

Also supports batch mode: reads new leads from stdin JSON array.
"""
import json, sys, os

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "leads-registry.json")

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        with open(REGISTRY_PATH) as f:
            return json.load(f)
    return {"leads": []}

def make_key(name, org, email):
    n = (name or "").strip().lower()
    o = (org or "").strip().lower()
    e = (email or "").strip().lower()
    return f"{n}|{o}|{e}"

def check_duplicate(name, org, email):
    key = make_key(name, org, email)
    registry = load_registry()
    for lead in registry["leads"]:
        if lead["lead_key"] == key:
            return True, lead
        # Also check by email alone (same email = same person)
        if email and lead.get("email","").lower() == email.lower():
            return True, lead
        # Check email domain match (same domain = same company, different person = OK)
        if email and lead.get("email",""):
            email_domain = email.split("@")[-1].lower() if "@" in email else ""
            lead_domain = lead.get("email","").split("@")[-1].lower() if "@" in lead.get("email","") else ""
            if email_domain and email_domain == lead_domain and len(email_domain) > 3:
                # Same domain - check if same person name too
                name_key = (name or "").strip().lower()
                lead_name = (lead.get("name","") or "").strip().lower()
                if name_key and lead_name and name_key == lead_name:
                    return True, lead
                # Different person at same company — not a duplicate
                pass
    return False, None

def check_batch(new_leads):
    results = []
    for lead in new_leads:
        name = lead.get("contact_name") or lead.get("name") or ""
        org = lead.get("company") or lead.get("organization_name") or ""
        email = lead.get("contact_email") or lead.get("email") or ""
        is_dup, match = check_duplicate(name, org, email)
        results.append({
            "input": lead,
            "is_duplicate": is_dup,
            "match": match
        })
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Batch mode — read JSON array from stdin
        new_leads = json.load(sys.stdin)
        results = check_batch(new_leads)
        print(json.dumps({"results": results, "duplicates_found": sum(1 for r in results if r["is_duplicate"])}, indent=2))
    else:
        # Single lead check
        name = sys.argv[1] if len(sys.argv) > 1 else ""
        org = sys.argv[2] if len(sys.argv) > 2 else ""
        email = sys.argv[3] if len(sys.argv) > 3 else ""
        is_dup, match = check_duplicate(name, org, email)
        result = {"is_duplicate": is_dup}
        if match:
            result["match"] = match
        print(json.dumps(result, indent=2))
