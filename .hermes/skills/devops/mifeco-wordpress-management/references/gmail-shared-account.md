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

Examples:
- [MIFECO] Welcome to the No Blue Sky series
- [MIFECO] AD: [SaaS] Your demo link inside
- [MIFECO] [Books] Free chapter from The No Blue Sky Series

Format: [MIFECO] → AD: (commercial only) → [Pipeline] → Subject

## Abuse Contact

- Email: MIFECOinc@gmail.com
- Recipients reply with "ABUSE" in the subject line
- Footer text: "For abuse/violation reports, reply to MIFECOinc@gmail.com with the word ABUSE in the subject line."

## CAN-SPAM Footer

Every outbound email body ends with this footer:

---
MIFECO — 147 Bathclub Cir, N. Redington Beach, FL 33708
To unsubscribe: https://mifeco.com/unsubscribe
For abuse/violation reports, reply to MIFECOinc@gmail.com with the word "ABUSE" in the subject line.

## WP Mail SMTP Settings (WordPress Admin)

- Mailer: Other SMTP
- From Email: MIFECOinc@gmail.com
- From Name: MIFECO
- Force From Email: ON (critical — overrides plugin From headers)
- SMTP Host: smtp.gmail.com
- SMTP Port: 587
- Encryption: STARTTLS
- Authentication: ON
- SMTP Username: MIFECOinc@gmail.com
- SMTP Password: Rm2214ri#

## DNS Records for Gmail Deliverability

@ TXT "v=spf1 include:_spf.google.com ~all"
_dmarc TXT "v=DMARC1; p=none; rua=mailto:MIFECOinc@gmail.com"

Also enable DKIM in Google Workspace admin console.

## WordPress REST API (mifeco-mailer.php v1.2.0)

- Plugin file: mifeco-mailer.php
- REST secret: JY2pcWpfu1*JeubsVBpm
- Send endpoint: POST /wp-json/mifeco/v1/send-email
- Unsubscribe endpoint: POST /wp-json/mifeco/v1/unsubscribe (public, no secret)
- Suppress check: POST /wp-json/mifeco/v1/suppress (requires secret)
- Suppression list: wp-content/mifeco-suppression-list.txt

## What Changed (2026-05-31 Migration)

1. From address: rmills@mifeco.com → MIFECOinc@gmail.com (forward-only alias → real mailbox)
2. SMTP: smtp.dreamhost.com → smtp.gmail.com
3. Subject tagging: [MIFECO] prefix on all outbound subjects
4. Abuse contact: abuse@rmills.com → MIFECOinc@gmail.com with "ABUSE" subject instruction
5. AD: prefix: Added to SaaS/Consulting commercial email subjects
6. List-Unsubscribe header: Added to all outbound emails
7. Suppression list: wp-content/mifeco-suppression-list.txt
8. Plugin: v1.0.1 → v1.2.0
