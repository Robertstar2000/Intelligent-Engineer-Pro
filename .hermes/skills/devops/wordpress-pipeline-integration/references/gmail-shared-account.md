# Gmail Shared Account Configuration for MIFECO

## Account Details

- Email: MIFECOinc@gmail.com
- Password: Rm2214ri#
- SMTP Host: smtp.gmail.com
- SMTP Port: 587 (STARTTLS)
- From Name: MIFECO
- From Email: MIFECOinc@gmail.com
- Reply-To: MIFECOinc@gmail.com

⚠️ This is the ONLY email account on DreamHost. Shared across ALL applications. DO NOT change password without coordinating all app owners.

## Subject Tagging Convention

All outbound emails through the shared account are prefixed with [MIFECO] so replies can be identified:

Format: [MIFECO] → AD: (commercial only) → [Pipeline] → Subject

Examples:
- [MIFECO] Welcome to the No Blue Sky series
- [MIFECO] AD: [SaaS] Your demo link inside
- [MIFECO] [Books] Free chapter from The No Blue Sky Series

## Abuse Contact

- Email: MIFECOinc@gmail.com
- Recipients reply with "ABUSE" in the subject line
- Footer text: "For abuse/violation reports, reply to MIFECOinc@gmail.com with the word ABUSE in the subject line."

## CAN-SPAM Footer

Every outbound email body ends with:

---
MIFECO — 147 Bathclub Cir, N. Redington Beach, FL 33708
To unsubscribe: https://mifeco.com/unsubscribe
For abuse/violation reports, reply to MIFECOinc@gmail.com with the word "ABUSE" in the subject line.

## WP Mail SMTP Settings

- Mailer: Other SMTP
- From Email: MIFECOinc@gmail.com
- From Name: MIFECO
- Force From Email: ON (critical)
- SMTP Host: smtp.gmail.com
- SMTP Port: 587
- Encryption: STARTTLS
- SMTP Username: MIFECOinc@gmail.com
- SMTP Password: Rm2214ri#

## Pipeline Data API Constants (pipeline_data_api.py)

- FROM_EMAIL: MIFECOinc@gmail.com
- FROM_NAME: MIFECO
- ABUSE_EMAIL: MIFECOinc@gmail.com
- ABUSE_SUBJECT_KEYWORD: ABUSE
- SUBJECT_TAG: [MIFECO]
- COMMERCIAL_PIPELINES: {saas, consulting} — get AD: prefix
- PHYSICAL_ADDRESS: 147 Bathclub Cir, N. Redington Beach, FL 33708

## Subject Line Format

All outbound emails go through send_via_wordpress() which applies:
1. apply_ad_prefix() — prepends "AD:" for saas/consulting pipelines
2. apply_subject_tag() — prepends "[MIFECO]" if not already present
3. build_can_spam_footer() — appends physical address + unsubscribe + abuse contact

Final subject format: [MIFECO] AD: [Pipeline] Original Subject

## WordPress REST API (mifeco-mailer.php v1.2.0)

- REST secret: JY2pcWpfu1*JeubsVBpm
- Send: POST /wp-json/mifeco/v1/send-email
- Unsubscribe: POST /wp-json/mifeco/v1/unsubscribe (public)
- Suppress check: POST /wp-json/mifeco/v1/suppress (requires secret)
- Suppression list: wp-content/mifeco-suppression-list.txt
- List-Unsubscribe header: Set on all outbound emails
