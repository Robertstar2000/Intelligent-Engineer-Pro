#!/usr/bin/env python3
"""
dedup-check.py — Duplicate lead checker against the master registry.

3-layer dedup logic:
  Layer 1: Exact lead_key match (normalized name|org|email)
  Layer 2: Same email address (regardless of org)
  Layer 3: Same email domain + same name
  Same company, DIFFERENT person = NOT a duplicate.

Usage:
  Single check:  python3 dedup-check.py "Name" "Org" "email@example.com"
  Batch check:   cat new-leads.json | python3 dedup-check.py
"""

import json
import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(SCRIPT_DIR, "leads-registry.json")


PIPELINE_FILES = {
    "books": "pipeline-books.json",
    "consulting": "pipeline-consulting.json",
    "saas": "pipeline-saas.json",
}

UNIFIED_PATH = os.path.join(SCRIPT_DIR, "unified-pipeline.json")


def load_registry():
    """Load leads-registry.json; return list of lead dicts or None if missing/broken.

    Handles two registry formats:
      - Aggregate (pipelines.{pipeline}.leads = [lead IDs]) → builds dedup
        index from unified-pipeline.json (or individual pipeline JSONs as fallback).
      - Individual (flat list of dicts with lead_key/name/email/org) → as-is.
    """
    if not os.path.isfile(REGISTRY_PATH):
        return None
    try:
        with open(REGISTRY_PATH, "r") as fh:
            data = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None

    # Individual format — flat list of dicts with lead_key/name/email/org
    leads = data.get("leads")
    if isinstance(leads, list):
        return leads

    # Aggregate format — has "pipelines" key with grouped lead IDs
    if "pipelines" in data:
        return _build_index_from_unified()

    return []


def _build_index_from_unified():
    """Build a dedup-friendly lead list from unified-pipeline.json enrichment data.

    Fall back to individual pipeline JSONs if unified file is missing or broken.
    """
    unified = _load_json(UNIFIED_PATH)
    if unified is not None and isinstance(unified, list):
        return _extract_leads_from_unified(unified)

    # Fallback: iterate individual pipeline JSONs
    leads = []
    for pipeline_name, filename in PIPELINE_FILES.items():
        path = os.path.join(SCRIPT_DIR, filename)
        data = _load_json(path)
        if data is None:
            continue
        pipeline = data.get("pipeline", data)
        pipeline_leads = pipeline.get("leads", [])
        leads.extend(_normalize_pipeline_leads(pipeline_leads, pipeline_name))
    return leads


def _load_json(path):
    """Safely load a JSON file, returning None on any failure."""
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None


def _extract_leads_from_unified(unified):
    """Build a dedup index from the unified-pipeline.json format.

    unified is a list of entries like:
      {"lead_id": "lead-001", "pipeline": "books", "enrichment": {
        "contact_name": "...", "company_name": "...", "email": "...", ...}}
    """
    leads = []
    for entry in unified:
        enrichment = entry.get("enrichment", {}) or {}
        name = enrichment.get("contact_name", "") or ""
        org = enrichment.get("company_name", "") or ""
        email = enrichment.get("email", "") or ""
        lead_key = "|".join([normalize(name), normalize(org), normalize(email)])

        leads.append({
            "lead_key": lead_key,
            "name": name,
            "organization": org,
            "email": email,
            "source_pipeline": entry.get("pipeline", ""),
            "original_id": entry.get("lead_id", ""),
        })

    return leads


def _normalize_pipeline_leads(pipeline_leads, pipeline_name):
    """Extract name/org/email from a pipeline JSON's lead entries.

    Handles the different field naming conventions across pipelines:

        SaaS:      {"name", "company", "email"}
        Books:     {"contact": {"name", "organization", "email"}}
        Consulting: {"contact_name", "company_name", "contact_email"}
    """
    results = []
    for lead in pipeline_leads:
        if not isinstance(lead, dict):
            continue

        # Books format: {"contact": {"name": ..., "organization": ..., "email": ...}}
        contact = lead.get("contact")
        if isinstance(contact, dict):
            name = contact.get("name", "") or ""
            org = contact.get("organization", "") or ""
            email = contact.get("email", "") or ""
        else:
            # SaaS: name/company/email
            name = lead.get("name", "") or ""
            org = lead.get("company", "") or ""
            email = lead.get("email", "") or ""
            # Consulting: contact_name/company_name/contact_email
            if not name and "contact_name" in lead:
                name = lead.get("contact_name", "") or ""
            if not org and "company_name" in lead:
                org = lead.get("company_name", "") or ""
            if not email and "contact_email" in lead:
                email = lead.get("contact_email", "") or ""

        lead_key = "|".join([normalize(name), normalize(org), normalize(email)])

        # Map pipeline IDs (S-001, B-001, C-001) to the org's registry prefix
        lead_id = lead.get("id", "")

        results.append({
            "lead_key": lead_key,
            "name": name,
            "organization": org,
            "email": email,
            "source_pipeline": pipeline_name,
            "original_id": lead_id,
        })

    return results


def normalize(s):
    """Trim, lowercase, collapse whitespace."""
    if not s:
        return ""
    return re.sub(r"\s+", " ", str(s).strip().lower())


def make_key(name, org, email):
    """Normalized, lowercased, trimmed name|org|email key."""
    parts = [normalize(name), normalize(org), normalize(email)]
    return "|".join(parts)


def email_domain(email):
    """Extract the domain portion of an email, lowercased."""
    e = normalize(email)
    at_idx = e.find("@")
    if at_idx == -1:
        return ""
    return e[at_idx + 1:]


def same_name(n1, n2):
    """Compare two name strings after normalization."""
    return normalize(n1) == normalize(n2)


def check_lead(name, org, email, leads):
    """Check a single lead against the registry. Returns dict with dedup result."""
    if leads is None:
        return {"is_duplicate": False}

    candidate_key = make_key(name, org, email)
    candidate_email = normalize(email)
    candidate_domain = email_domain(email)
    candidate_name = normalize(name)

    for lead in leads:
        # Layer 1: Exact lead_key match
        db_key = normalize(lead.get("lead_key", ""))
        if db_key == candidate_key:
            return {
                "is_duplicate": True,
                "match": lead,
                "layer": "exact_key_match"
            }

        # Layer 2: Same email address (regardless of org)
        db_email = normalize(lead.get("email", ""))
        if db_email and db_email == candidate_email:
            return {
                "is_duplicate": True,
                "match": lead,
                "layer": "email_match"
            }

        # Layer 3: Same email domain + same name
        db_domain = email_domain(lead.get("email", ""))
        db_name = normalize(lead.get("name", ""))
        if db_domain and candidate_domain and db_domain == candidate_domain:
            if db_name and candidate_name and db_name == candidate_name:
                return {
                    "is_duplicate": True,
                    "match": lead,
                    "layer": "domain_plus_name_match"
                }

    return {"is_duplicate": False}


def process_batch(new_leads, leads):
    """Process a list of new leads against the registry."""
    results = []
    duplicates_found = 0

    for item in new_leads:
        name = item.get("name", "")
        org = item.get("organization", "")
        email = item.get("email", "")
        result = check_lead(name, org, email, leads)
        entry = {
            "lead": item,
            "is_duplicate": result["is_duplicate"],
        }
        if result["is_duplicate"]:
            entry["match"] = result["match"]
            entry["layer"] = result["layer"]
            duplicates_found += 1
        results.append(entry)

    return {
        "results": results,
        "duplicates_found": duplicates_found,
        "total_checked": len(results)
    }


def main():
    leads = load_registry()

    # Mode 1: CLI args — single check
    if len(sys.argv) >= 4:
        name = sys.argv[1]
        org = sys.argv[2]
        email = sys.argv[3]
        result = check_lead(name, org, email, leads)
        print(json.dumps(result))
        return

    # Mode 2: Stdin batch
    try:
        raw = sys.stdin.read()
    except KeyboardInterrupt:
        print(json.dumps({"results": [], "duplicates_found": 0, "total_checked": 0}))
        return

    raw = raw.strip()
    if not raw:
        print(json.dumps({"results": [], "duplicates_found": 0, "total_checked": 0}))
        return

    try:
        new_leads = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input on stdin"}, indent=2))
        sys.exit(1)

    # Accept either a list directly or {"leads": [...]}
    if isinstance(new_leads, dict):
        new_leads = new_leads.get("leads", [])

    if not isinstance(new_leads, list):
        print(json.dumps({"error": "Expected a JSON array or object with 'leads' key"}, indent=2))
        sys.exit(1)

    result = process_batch(new_leads, leads)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
