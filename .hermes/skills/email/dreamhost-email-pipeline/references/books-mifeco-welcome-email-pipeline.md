# books.mifeco.com — Welcome Email Pipeline

## Overview

A standalone Python-based email automation system for the books.mifeco.com author site. Not part of the WordPress/DreamHost MIFECO mailer plugin — it runs independently on the agent host.

**Location:** `/home/bob/cindy-lou-series/books-mifeco-website/api/send_welcome.py`

## Trigger

The `subscribe.php` endpoint at `/api/subscribe.php` on books.mifeco.com handles new signups:

1. Saves subscriber to `data/subscribers.csv` (email, source, series, timestamp, status, IP)
2. Calls `send_welcome.py <email> <series>` in the background (exec'd with `> /dev/null 2>&1 &`)
3. The script sends **Email 1** immediately and schedules **Emails 2–4** in `data/email-state.json`

## 4-Email Welcome Sequence

| Step | Timing     | Subject                                                     | Template File            |
|------|------------|-------------------------------------------------------------|--------------------------|
| 1    | Immediate  | "Your free story from Bob J Mills is here"                  | `email-templates/welcome-email.html`    |
| 2    | Day 2      | "A quick thank you from Bob J Mills"                        | `email-templates/welcome-email-2.html`  |
| 3    | Day 5      | "Continue the journey: {Series Name}"                       | `email-templates/welcome-email-3.html`  |
| 4    | Day 8      | "More worlds to explore"                                    | `email-templates/welcome-email-4.html`  |

## State File: `data/email-state.json`

```json
{
  "sent_emails": [
    { "email": "user@example.com", "series": "cindy-lou", "step": 1, "sent_at": "2026-06-05T..." }
  ],
  "pending": [
    { "email": "user@example.com", "series": "cindy-lou", "step": 2, "scheduled": "2026-06-07T..." }
  ]
}
```

- `sent_emails`: history of all sent emails
- `pending`: future emails with ISO-8601 scheduled timestamps

## Cron Processing

The `--process-pending` flag processes any overdue scheduled emails:

```bash
python3 send_welcome.py --process-pending
```

**⚠️ Argparse gotcha (fixed):** The argparse originally required positional `email` and `series` args even in `--process-pending` mode, causing cron jobs to fail. Both were changed to `nargs="?"` with a conditional branch so `--process-pending` works standalone. If the script errors about missing arguments, check that `nargs="?"` is set on both `email` and `series` arguments.

## Series Configuration

Four supported series (defined in `SERIES_INFO` dict in `send_welcome.py`):

| Series Key        | Series Name              | Magnet Title                    |
|-------------------|--------------------------|---------------------------------|
| `cindy-lou`       | The Cindy Lou Legal Capers | Cindy Lou and the Case of the Missing Retainer |
| `no-blue-sky`     | No Blue Sky              | Before the Dust                 |
| `lunar-foundation`| The Lunar Foundation     | Moonbase One: First Light       |
| `lightships`      | The Age of Lightships    | The Last Transmission           |

Each series has 3 books with title, description, and Amazon URL configured in the script.

## Template System

Email templates live in `email-templates/` as HTML files. Template variables use `{{VARIABLE_NAME}}` syntax:

- `{{SERIES_NAME}}`, `{{MAGNET_EPUB_URL}}`, `{{MAGNET_PDF_URL}}`
- `{{BOOK_1_TITLE}}`, `{{BOOK_1_DESCRIPTION}}`, `{{BOOK_1_AMAZON_URL}}`
- `{{BOOK_2_TITLE}}`, `{{BOOK_2_DESCRIPTION}}`, `{{BOOK_2_AMAZON_URL}}`
- `{{BOOK_3_TITLE}}`, `{{BOOK_3_DESCRIPTION}}`, `{{BOOK_3_AMAZON_URL}}`
- `{{UNSUBSCRIBE_URL}}`

## Delivery Mechanism

Uses Himalaya CLI (`~/.local/bin/himalaya`) with `himalaya template send` — emails are piped as raw MIME with HTML content-type. Sender: `Bob J Mills <mifecoinc@gmail.com>`.

## Series Mapping in subscribe.php

The subscribe endpoint maps incoming `series` parameter to a magnet series:

| Input `series` | Magnet Delivery    |
|----------------|--------------------|
| `all`          | `cindy-lou` (default) |
| `cindy-lou`    | `cindy-lou`        |
| `no-blue-sky`  | `no-blue-sky`      |
| `lunar-foundation` | `lunar-foundation` |
| `lightships`   | `lightships`       |
| `age-of-lightships` | `lightships`   |