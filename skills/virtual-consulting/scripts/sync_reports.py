#!/usr/bin/env python3
"""
MIFECO Consulting — Report Sync Script
=======================================
Syncs generated PDF reports from local machine to DreamHost via SFTP.
Run this after report generation to make files available for download.

Usage:
    python3 sync_reports.py

Prerequisites:
    - paramiko: pip install paramiko
    - DREAMHOST_PASS environment variable set
    - Environment variables: DB_HOST, DB_USER, DB_PASS, DB_NAME
"""

import os
import sys
import json
import paramiko
from pathlib import Path

DREAMHOST_USER = "dh_mwpxuu"
DREAMHOST_HOST = "mifeco.com"
DREAMHOST_REPORTS_PATH = "/home/dh_mwpxuu/mifeco.com/consult/reports"
LOCAL_REPORTS_DIR = Path.home() / ".hermes" / "consulting-reports"

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'mysql.mifeco.com'),
    'user': os.environ.get('DB_USER', ''),
    'password': os.environ.get('DB_PASS', ''),
    'database': os.environ.get('DB_NAME', 'mifeco_com_1'),
}


def get_pending_uploads():
    try:
        import pymysql
        db = pymysql.connect(**DB_CONFIG, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        with db.cursor() as cur:
            cur.execute("""
                SELECT d.id, d.survey_id, d.type, d.filename, d.file_path, d.status, s.user_id
                FROM consulting_documents d
                JOIN consulting_surveys s ON d.survey_id = s.id
                WHERE d.status = 'ready'
                ORDER BY d.created_at DESC LIMIT 50
            """)
            docs = cur.fetchall()
        db.close()
        return docs
    except Exception as e:
        print(f"DB error: {e}")
        return []


def sync_to_dreamhost(local_path, remote_filename):
    password = os.environ.get('DREAMHOST_PASS', '')
    if not password:
        print("ERROR: DREAMHOST_PASS not set")
        return False
    try:
        transport = paramiko.Transport((DREAMHOST_HOST, 22))
        transport.connect(username=DREAMHOST_USER, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        try:
            sftp.stat(DREAMHOST_REPORTS_PATH)
        except FileNotFoundError:
            sftp.mkdir(DREAMHOST_REPORTS_PATH)
        remote_path = f"{DREAMHOST_REPORTS_PATH}/{remote_filename}"
        sftp.put(str(local_path), remote_path)
        sftp.close()
        transport.close()
        return True
    except Exception as e:
        print(f"SFTP error: {e}")
        return False


def update_document_path(doc_id, new_path):
    try:
        import pymysql
        db = pymysql.connect(**DB_CONFIG, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        with db.cursor() as cur:
            cur.execute("UPDATE consulting_documents SET file_path = %s WHERE id = %s", (new_path, doc_id))
            db.commit()
        db.close()
    except Exception as e:
        print(f"DB update error: {e}")


def main():
    print("=== MIFECO Consulting Report Sync ===\n")
    if not LOCAL_REPORTS_DIR.exists():
        print(f"Local reports directory not found: {LOCAL_REPORTS_DIR}")
        sys.exit(1)
    docs = get_pending_uploads()
    if not docs:
        print("No documents pending sync.")
        sys.exit(0)
    print(f"Found {len(docs)} documents to sync.\n")
    synced = 0
    failed = 0
    for doc in docs:
        local_path = Path(doc['file_path'])
        if not local_path.exists():
            local_path = LOCAL_REPORTS_DIR / doc['filename']
        if not local_path.exists():
            print(f"  Survey {doc['survey_id']} / {doc['type']}: File not found locally")
            failed += 1
            continue
        remote_filename = f"survey_{doc['survey_id']}_{doc['type']}.pdf"
        success = sync_to_dreamhost(local_path, remote_filename)
        if success:
            new_path = f"{DREAMHOST_REPORTS_PATH}/{remote_filename}"
            update_document_path(doc['id'], new_path)
            print(f"  Survey {doc['survey_id']} / {doc['type']}: Synced ({local_path.stat().st_size // 1024}KB)")
            synced += 1
        else:
            print(f"  Survey {doc['survey_id']} / {doc['type']}: Upload failed")
            failed += 1
    print(f"\nDone: {synced} synced, {failed} failed")


if __name__ == '__main__':
    main()
