---
name: social-direct-publisher
description: Publish approved agent-generated social media posts to LinkedIn, Facebook Pages, and Instagram Business/Creator accounts using official OAuth and API flows. Use when the user wants to create, review, schedule, approve, or directly publish business-safe social posts, especially when platform-specific formatting, OAuth token handling, API adapters, approval gates, audit logs, and compliance checks are required.
---

# Social Direct Publisher

## Purpose

Enable a Hermes agent to safely generate, format, approve, and publish social media posts to LinkedIn, Facebook Pages, and Instagram Business/Creator accounts through official APIs only — no browser automation or scraping.

## Core Operating Rule

The agent must **never** publish directly from raw LLM output.

**Required flow:**
```
Generate → Validate → Format → Store Draft → Approve → Publish via API → Audit Log → Return result
```

**Default mode:** `approve_then_publish`
**Auto-publish mode:** Only after owner explicitly enables `auto_publish_low_risk`

## When to Use This Skill

- User wants to publish a social media post to LinkedIn, Facebook, or Instagram
- User wants to create a draft for review before posting
- User wants to manage connected social accounts (OAuth tokens, page IDs, etc.)
- User wants to audit past publish attempts
- User wants to approve or reject pending posts

## Project Location

The backend service lives at: `/mnt/usb_4tb/books/social_agent/`

For full project structure, Alembic setup, and async SQLAlchemy patterns, see:
[`references/project-setup.md`](references/project-setup.md)

For the pipeline-engine integration pattern (client script, cron runner, multi-skill updates), see:
[`references/pipeline-engine-integration.md`](references/pipeline-engine-integration.md)

## Setup

### 1. Install dependencies

```bash
cd /mnt/usb_4tb/books/social_agent
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your database URL and encryption key
```

Generate a Fernet key:
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

### 3. Run database migrations

```bash
alembic upgrade head
```

### 4. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

## API Endpoints

### Health Check
```
GET /health
```

### Register a Connected Account
```
POST /social/accounts
```
Body: `owner_user_id`, `platform` (linkedin|facebook|instagram), `display_name`, `platform_account_id`, `access_token`, plus platform-specific fields (`platform_actor_urn` for LinkedIn, `page_id` for Facebook, `instagram_user_id` for Instagram).

### Create a Social Post
```
POST /social/posts
```
Body: `owner_user_id`, `created_by`, `base_message`, `platforms[]`, `account_ids[]`, optional `campaign`, `media[]`, `link_url`, `approval_mode`.

Returns post with `status: pending_approval` (default) or `status: draft`.

### Approve a Post
```
POST /social/posts/{post_id}/approve
```
Body: `approved_by`

### Publish a Post
```
POST /social/posts/{post_id}/publish
```
Body: `actor`, `force` (bool, default false)

Only works if post status is `approved` or `failed` (with `force: true`).

## Platform-Specific Rules

### LinkedIn
- **Endpoint:** `POST https://api.linkedin.com/rest/posts`
- **Headers:** `Authorization: Bearer <token>`, `LinkedIn-Version: YYYYMM`, `X-Restli-Protocol-Version: 2.0.0`
- **Author:** Must be a URN — `urn:li:person:<id>` or `urn:li:organization:<id>`
- **Max length:** 3000 characters
- **Permissions:** `w_organization_social` (org) or `w_member_social` (person)
- **Post ID:** Returned in `x-restli-id` header

### Facebook Page
- **Endpoint:** `POST https://graph.facebook.com/{version}/{page_id}/feed`
- **Payload:** `message`, `link` (optional), `access_token`
- **Permissions:** `pages_manage_posts`
- **Post ID:** Returned as `id` in JSON response

### Instagram Business/Creator
- **Flow:** Create media container → Poll until `FINISHED` → Publish container
- **Endpoints:**
  - `POST /{ig_user_id}/media` (create container)
  - `GET /{creation_id}?fields=status_code` (poll status)
  - `POST /{ig_user_id}/media_publish` (publish)
- **Requires:** At least one public image URL
- **Max caption length:** 2200 characters
- **Links:** Cannot be clickable in captions — append "Link in bio."

## Hermes Agent Behavior Rules

1. **Always ask** whether the post should be draft-only, approval-required, or auto-publish — unless the user has configured a default.
2. **Refuse** to publish content that fails policy checks (blocked terms, excessive length).
3. **Never expose** access tokens, refresh tokens, client secrets, or encrypted token blobs.
4. **Prefer draft + approval** for new users and new campaigns.
5. **Format each platform separately** — character limits and link handling differ.
6. **Require at least one public media URL** before Instagram feed publishing.
7. **Use LinkedIn URNs** for LinkedIn author fields.
8. **Use Facebook Page IDs and Page access tokens** for Facebook Page publishing.
9. **Use Instagram Business/Creator IDs and media container flow** for Instagram publishing.
10. **Log every attempted publish**, including failures.
11. **Return clear per-platform status** in responses.

## Policy Checker

The built-in policy checker blocks:
- "guaranteed profit", "inside information", "confidential customer"
- "password", "api key", "ssn", "social security number"
- Posts over 10,000 characters

Risk score: 30 points per violation, threshold at 80 (blocked if ≥ 80).

## Pipeline-Engine Integration

### Quick Reference

- **Client script**: `~/.hermes/pipeline-engine/scripts/social_publisher_client.py`
- **Cron runner**: `~/.hermes/pipeline-engine/scripts/run-social-publisher.sh`
- **Drafts file**: `~/.hermes/pipeline-engine/data/social-publisher-drafts.json`
- **Pipeline ID**: `social-media` (10th pipeline in pipeline-state.json)
- **Cron schedule**: `0 9 * * *` (9 AM daily, after pipeline sync)

### Trigger Points

| Pipeline Event | Campaign Tag | Platforms |
|---|---|---|
| Book gets ASIN (published) | `book-launch-[key]` | LinkedIn, Facebook, Instagram |
| Blog post published | `blog-[slug]` | LinkedIn, Facebook, Instagram |
| SaaS product deployed | `saas-promo` | LinkedIn, Facebook, Instagram |
| Consulting engagement won | `consulting-promo` | LinkedIn, Facebook, Instagram |

### Integration Pattern

For the complete integration pattern (how to connect a new external service to pipeline-engine), see:
[`references/pipeline-engine-integration.md`](references/pipeline-engine-integration.md)

## Running Tests

```bash
cd /mnt/usb_4tb/books/social_agent
source .venv/bin/activate
pytest tests/ -v
```

## Production Checklist

Before enabling real publishing:
- [ ] Confirm API product/permission in each developer console
- [ ] Complete LinkedIn access approval if required
- [ ] Complete Meta App Review if required
- [ ] Store tokens encrypted (Fernet)
- [ ] Rotate secrets regularly
- [ ] Add token refresh jobs
- [ ] Add rate-limit handling
- [ ] Add retries with exponential backoff
- [ ] Add idempotency keys
- [ ] Add dead-letter queue for failed publishes
- [ ] Add human approval UI
- [ ] Add customer/confidential-info detector
- [ ] Add brand voice checker
- [ ] Add legal/compliance claim checker
- [ ] Add per-platform preview
- [ ] Add post delete/takedown workflow
- [ ] Add audit export

## Deferred (Post-MVP)

- LinkedIn image/video asset uploads
- Instagram Reels
- Instagram carousels
- Facebook videos
- Scheduling queue
- Auto-publish without approval