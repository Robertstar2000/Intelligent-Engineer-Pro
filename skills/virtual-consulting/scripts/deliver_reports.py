#!/usr/bin/env python3
"""
MIFECO Consulting — Report Delivery Script
==========================================
Called after PDF reports are generated. Sends email to client with download links.

Usage:
    python3 deliver_reports.py --survey-id 123

Prerequisites:
    - DreamHost SMTP access (localhost:25)
    - PDF reports generated and stored in consulting_documents table
    - Environment variables: DB_HOST, DB_USER, DB_PASS, DB_NAME
"""

import argparse
import json
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# DreamHost SMTP config
SMTP_HOST = "localhost"
SMTP_PORT = 25
FROM_EMAIL = "noreply@mifeco.com"
FROM_NAME = "MIFECO Virtual Consulting"
SITE_URL = "https://mifeco.com/consult"


def get_db():
    """Get database connection matching PHP config."""
    import pymysql
    import os
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'mysql.mifeco.com'),
        user=os.environ.get('DB_USER', ''),
        password=os.environ.get('DB_PASS', ''),
        database=os.environ.get('DB_NAME', 'mifeco_com_1'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def deliver_reports(survey_id: int) -> bool:
    """Send report delivery email to client."""
    db = get_db()
    try:
        with db.cursor() as cur:
            cur.execute("""
                SELECT s.id as survey_id, s.user_id, s.initial_responses,
                       u.email, u.full_name, u.business_name
                FROM consulting_surveys s
                JOIN consulting_users u ON s.user_id = u.id
                WHERE s.id = %s
            """, (survey_id,))
            survey = cur.fetchone()
            if not survey:
                print(f"Survey {survey_id} not found")
                return False

            cur.execute("""
                SELECT type, filename FROM consulting_documents
                WHERE survey_id = %s AND status = 'ready'
            """, (survey_id,))
            docs = cur.fetchall()

            if not docs:
                print(f"No ready documents for survey {survey_id}")
                return False

            download_links = ""
            for doc in docs:
                url = f"{SITE_URL}/download.php?survey={survey_id}&type={doc['type']}"
                label = "AI Readiness Assessment" if doc['type'] == 'assessment' else "Strategic Action Plan"
                download_links += f'<li><a href="{url}">{label} ({doc["filename"]})</a></li>\n'

            client_name = survey['full_name'] or 'there'
            business_name = survey['business_name'] or 'your business'

            html_body = f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:'Inter',sans-serif;">
<table width="600" cellpadding="0" cellspacing="0" style="margin:0 auto;background:#fff;">
    <tr><td style="background:linear-gradient(135deg,#0a1628,#1a365d);padding:40px 30px;text-align:center;">
        <h1 style="color:#fff;font-size:24px;margin:0;">MIFECO Virtual Consulting</h1>
        <p style="color:#94a3b8;font-size:14px;margin:8px 0 0;">AI Readiness Assessment — Complete</p>
    </td></tr>
    <tr><td style="padding:40px 30px;">
        <p style="font-size:18px;font-weight:700;color:#0a1628;">Hi {client_name},</p>
        <p style="font-size:15px;line-height:1.7;color:#4a5568;">Your <strong>AI Readiness Assessment</strong> and <strong>Strategic Action Plan</strong> are ready for {business_name}.</p>
        <div style="background:#f7fafc;border-left:4px solid #3b82f6;padding:16px 20px;margin:20px 0;border-radius:0 8px 8px 0;">
            <strong>Your reports include:</strong>
            <ul style="margin:8px 0 0;padding-left:20px;">
                {download_links}
            </ul>
        </div>
        <p style="text-align:center;margin:24px 0;">
            <a href="{SITE_URL}/download.php?survey={survey_id}&type=assessment" style="display:inline-block;padding:16px 40px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:#fff;text-decoration:none;border-radius:12px;font-size:16px;font-weight:700;">Download Your Reports</a>
        </p>
        <p style="font-size:14px;color:#94a3b8;">Reports are confidential. Questions? Reply to this email.</p>
        <p style="font-size:15px;color:#4a5568;">— Bob Mills<br><em>Founder, MIFECO</em></p>
    </td></tr>
    <tr><td style="background:#f7fafc;padding:24px 30px;text-align:center;border-top:1px solid #e2e8f0;">
        <p style="font-size:12px;color:#94a3b8;margin:0;"><strong>MIFECO Virtual Consulting</strong> — <a href="https://mifeco.com" style="color:#3b82f6;">mifeco.com</a></p>
    </td></tr>
</table>
</body>
</html>"""

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Your MIFECO Assessment Is Ready - {business_name}"
            msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
            msg['To'] = survey['email']
            msg.attach(MIMEText(html_body, 'html'))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
                smtp.send_message(msg)

            cur.execute(
                "INSERT INTO consulting_activity_log (user_id, action, details) VALUES (%s, 'report_delivered', %s)",
                (survey['user_id'], json.dumps({'survey_id': survey_id, 'email': survey['email']}))
            )
            db.commit()
            print(f"Reports delivered to {survey['email']} for survey {survey_id}")
            return True

    except Exception as e:
        print(f"Delivery error: {e}")
        return False
    finally:
        db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deliver MIFECO consulting reports')
    parser.add_argument('--survey-id', type=int, required=True, help='Survey ID to deliver')
    args = parser.parse_args()
    success = deliver_reports(args.survey_id)
    sys.exit(0 if success else 1)
