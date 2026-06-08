#!/usr/bin/env python3
"""
MIFECO Pipeline Data API — server-side handler for advancing lead stages,
mock inbox, and email sending.

Called by the dashboard's HTTPS server on POST endpoints.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path.home() / ".hermes" / "pipeline-engine" / "data"
MOCK_INBOX_FILE = DATA_DIR / "mock-inbox.json"

# Stage mapping: 1→2 advancement
STAGE_ADVANCE = {
    "books": {"from_stage": 1, "from_name": "Lead Inbox", "to_stage": 2, "to_name": "Contacted"},
    "saas": {"from_stage": 1, "from_name": "Identified", "to_stage": 2, "to_name": "Contacted"},
    "consulting": {"from_stage": 1, "from_name": "lead", "to_stage": 2, "to_name": "contacted"},
}

PIPELINE_FILES = {
    "books": DATA_DIR / "pipeline-books.json",
    "saas": DATA_DIR / "pipeline-saas.json",
    "consulting": DATA_DIR / "pipeline-consulting.json",
}

WP_REST_URL = "https://mifeco.com/wp-json/mifeco/v1/send-email"
WP_UNSUBSCRIBE_URL = "https://mifeco.com/wp-json/mifeco/v1/unsubscribe"
WP_SECRET = "JY2pcWpfu1*JeubsVBpm"

# Shared Gmail account — the ONLY email account available on DreamHost
# Used by all applications. DO NOT change password without coordinating.
FROM_EMAIL = "MIFECOinc@gmail.com"
FROM_NAME = "MIFECO"

# CAN-SPAM compliance constants
PHYSICAL_ADDRESS = "147 Bathclub Cir, N. Redington Beach, FL 33708"
ABUSE_EMAIL = "MIFECOinc@gmail.com"
ABUSE_SUBJECT_KEYWORD = "ABUSE"
SENDER_NAME = "Bob Mills"  # Standardized across all pipelines

# Subject tag for shared-account identification
SUBJECT_TAG = "[MIFECO]"

# Commercial pipelines get AD: prefix
COMMERCIAL_PIPELINES = {"saas", "consulting"}


def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return True


def find_lead(pipeline_file, lead_name):
    """Find a lead in a pipeline JSON by name."""
    data = load_json(pipeline_file)
    if not data:
        return None, None

    if "pipeline" in data:
        leads = data["pipeline"].get("leads", [])
        for lead in leads:
            # Check various name fields
            name = lead.get("contact", {}).get("name", "") or lead.get("name", "") or lead.get("contact_name", "")
            if name and lead_name.lower() in name.lower():
                return data, lead
            # Also match by company
            company = lead.get("contact", {}).get("organization", "") or lead.get("company", "") or lead.get("company_name", "")
            if company and lead_name.lower() in company.lower():
                return data, lead
    return None, None


def advance_lead_stage(pipeline, lead_name):
    """
    Advance a lead from stage 1 to stage 2 in the pipeline JSON.
    Returns (success, message).
    """
    if pipeline not in PIPELINE_FILES:
        return False, f"Unknown pipeline: {pipeline}"

    pf = PIPELINE_FILES[pipeline]
    if not pf.exists():
        return False, f"Pipeline file not found: {pf}"

    data, lead = find_lead(pf, lead_name)
    if data is None:
        return False, f"Pipeline data not found for {pipeline}"
    if lead is None:
        return False, f"Lead '{lead_name}' not found in {pipeline} pipeline"

    stages = STAGE_ADVANCE[pipeline]
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Different pipelines use different field names
    if pipeline == "books":
        if lead.get("current_stage") != stages["from_stage"]:
            pass
        lead["current_stage"] = stages["to_stage"]
        lead["current_stage_name"] = stages["to_name"]
        lead["entered_stage"] = now_iso
        lead["days_in_stage"] = 0
        if "stage_history" not in lead:
            lead["stage_history"] = []
        lead["stage_history"].append({
            "stage_id": stages["to_stage"],
            "stage_name": stages["to_name"],
            "entered": now_iso,
            "exited": None,
            "duration_days": 0,
            "notes": f"Email sent via Outreach Dashboard on {now_iso[:10]}"
        })
        lead["next_action"] = f"Awaiting response. Contacted {now_iso[:10]}."
        lead["last_contact"] = now_iso

    elif pipeline == "consulting":
        if int(lead.get("stage", 1)) != stages["from_stage"]:
            pass
        lead["stage"] = stages["to_stage"]
        lead["status"] = stages["to_name"]
        lead["notes"] = (lead.get("notes", "") + f"\nCONTACTED {now_iso[:10]}: Email sent via Outreach Dashboard.").strip()

    elif pipeline == "saas":
        if int(lead.get("stage", 1)) != stages["from_stage"]:
            pass
        lead["stage"] = stages["to_stage"]
        lead["notes"] = (lead.get("notes", "") + f"\nContacted {now_iso[:10]}: Email sent.").strip()
        lead["advanced_at"] = now_iso

    save_json(pf, data)
    return True, f"Lead '{lead_name}' advanced to '{stages['to_name']}' in {pipeline} pipeline"


def write_mock_inbox(lead_name, email, pipeline, subject, body):
    """Write sent email to mock inbox for test mode review."""
    mock_inbox = load_json(MOCK_INBOX_FILE) or []
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mock_inbox.append({
        "id": f"mock-{len(mock_inbox)+1}",
        "sent_at": now_iso,
        "pipeline": pipeline,
        "to_name": lead_name,
        "to_email": email,
        "subject": subject,
        "body": body,
        "mode": "test"
    })
    save_json(MOCK_INBOX_FILE, mock_inbox)
    return True


def build_can_spam_footer(unsubscribe_url=None):
    """Build CAN-SPAM compliant footer with physical address and unsubscribe link."""
    footer = f"\n\n---\nMIFECO — {PHYSICAL_ADDRESS}\n"
    if unsubscribe_url:
        footer += f"To unsubscribe: {unsubscribe_url}\n"
    else:
        footer += "To unsubscribe, reply with \"UNSUBSCRIBE\" in the subject or body.\n"
    footer += f"For abuse/violation reports, reply to {ABUSE_EMAIL} with the word \"{ABUSE_SUBJECT_KEYWORD}\" in the subject line.\n"
    return footer


def apply_subject_tag(subject):
    """Apply [MIFECO] subject tag for shared-account identification."""
    if not subject.startswith(SUBJECT_TAG):
        subject = SUBJECT_TAG + " " + subject
    return subject


def apply_ad_prefix(subject, pipeline):
    """Prepend AD: to commercial/sales pipeline subjects."""
    if pipeline in COMMERCIAL_PIPELINES:
        if not subject.startswith("AD:"):
            subject = "AD: " + subject
    return subject


def send_via_wordpress(lead_name, email, pipeline, subject, body):
    """Send email via WordPress REST endpoint (production mode)."""
    # Apply AD: prefix for commercial pipelines
    subject = apply_ad_prefix(subject, pipeline)

    # Apply shared-account subject tag
    subject = apply_subject_tag(subject)

    # Build CAN-SPAM footer
    footer = build_can_spam_footer(WP_UNSUBSCRIBE_URL)
    full_body = body + footer

    payload = {
        "secret": WP_SECRET,
        "email": {
            "to": email,
            "subject": subject,
            "body": full_body,
            "pipeline": pipeline
        }
    }
    try:
        import urllib.request
        req = urllib.request.Request(
            WP_REST_URL,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            if result.get("success"):
                return True, "Email sent successfully via WordPress"
            else:
                return False, result.get("message", "Unknown WordPress error")
    except Exception as e:
        return False, str(e)


# ==== Request handlers for the HTTP server ====

def handle_request(method, path, body):
    """
    Main dispatcher. Returns (status_code, response_dict).
    """
    if method != "POST":
        return 405, {"error": "Method not allowed"}

    # POST /api/advance-lead
    if path == "/api/advance-lead":
        pipeline = body.get("pipeline", "").lower()
        lead_name = body.get("lead_name", "")
        mode = body.get("mode", "test")
        email = body.get("email", "")
        subject = body.get("subject", f"[{pipeline.capitalize()}] Outreach")
        message_body = body.get("body", "")

        if not pipeline or not lead_name:
            return 400, {"error": "pipeline and lead_name are required"}

        # 1. Advance lead stage
        ok, msg = advance_lead_stage(pipeline, lead_name)
        if not ok:
            return 500, {"error": msg}

        # 2. Handle email based on mode
        if mode == "production":
            ok2, msg2 = send_via_wordpress(lead_name, email, pipeline, subject, message_body)
            if not ok2:
                return 500, {"error": f"Stage advanced but email failed: {msg2}"}
            return 200, {
                "success": True,
                "message": f"Lead advanced + email sent. {msg}",
                "mode": "production"
            }
        else:
            # Test mode — write to mock inbox
            write_mock_inbox(lead_name, email, pipeline, subject, message_body)
            return 200, {
                "success": True,
                "message": f"Lead advanced + email written to mock inbox. {msg}",
                "mode": "test"
            }

    # POST /api/mock-inbox
    elif path == "/api/mock-inbox":
        inbox = load_json(MOCK_INBOX_FILE) or []
        return 200, {"success": True, "items": inbox}

    # POST /api/clear-mock-inbox
    elif path == "/api/clear-mock-inbox":
        save_json(MOCK_INBOX_FILE, [])
        return 200, {"success": True, "message": "Mock inbox cleared"}

    return 404, {"error": "Not found"}


if __name__ == "__main__":
    # CLI test: pipeline lead_name [mode]
    if len(sys.argv) >= 3:
        pipeline = sys.argv[1]
        lead_name = " ".join(sys.argv[2:])
        ok, msg = advance_lead_stage(pipeline, lead_name)
        print(f"{'✅' if ok else '❌'} {msg}")
    else:
        print("Usage: pipeline-data-api.py <pipeline> <lead_name>")
        print("  pipelines: books, saas, consulting")
