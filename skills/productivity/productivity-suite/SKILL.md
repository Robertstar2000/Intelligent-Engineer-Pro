---
name: productivity-suite
description: "Productivity tools — Airtable, Notion, Obsidian, Google Workspace, PowerPoint, PDF editing, OCR/document extraction, GIF search, Teams meetings, and maps. Class-level umbrella for all productivity integrations."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [productivity, airtable, notion, obsidian, google-workspace, powerpoint, pdf, ocr, gif, teams, maps]
    related_skills: [airtable, notion, obsidian, google-workspace, powerpoint, nano-pdf, ocr-and-documents, gif-search, teams-meeting-pipeline, maps]
---

# Productivity Suite

Class-level umbrella for all productivity integrations — databases, documents, email, meetings, and maps.

## Quick Decision Guide

| Need | Section |
|------|---------|
| Airtable CRUD operations | [Airtable](#airtable) |
| Notion pages/databases | [Notion](#notion) |
| Obsidian vault (read/search/create/edit) | [Obsidian](#obsidian) |
| Google Gmail/Calendar/Drive/Docs/Sheets | [Google Workspace](#google-workspace) |
| Create/edit PowerPoint decks | [PowerPoint](#powerpoint) |
| Edit PDF text/typos | [nano-pdf](#nano-pdf) |
| Extract text from PDFs/scans | [OCR & Documents](#ocr--documents) |
| Search/download GIFs | [GIF Search](#gif-search) |
| Teams meeting summaries | [Teams Meetings](#teams-meetings) |
| Geocoding, POIs, routes, timezones | [Maps](#maps) |

## Airtable
**Trigger:** Airtable operations, records CRUD, filters, upserts.

→ `references/airtable.md` — REST API via curl. Records CRUD, filters, upserts.

## Notion
**Trigger:** Notion pages, databases, markdown, Workers.

→ `references/notion.md` — Notion API + ntn CLI.

## Obsidian
**Trigger:** Obsidian vault, read/search/create/edit notes, wikilinks.

→ `references/obsidian.md` — Filesystem-first vault work. Read, list, search, create, append, edit notes.

## Google Workspace
**Trigger:** Gmail, Calendar, Drive, Docs, Sheets, Contacts.

→ `references/google-workspace.md` — OAuth2 setup, Gmail search/send, Calendar CRUD, Drive upload/download, Sheets read/write, Docs create/append. Scripts: `scripts/setup.py`, `scripts/google_api.py`.

## PowerPoint
**Trigger:** Create, read, edit .pptx decks, slides, notes, templates.

→ `references/powerpoint.md` — python-pptx for creating and editing presentations.

## nano-pdf
**Trigger:** Edit PDF text, typos, titles via natural language.

→ `references/nano-pdf.md` — nano-pdf CLI for NL-based PDF editing.

## OCR & Documents
**Trigger:** Extract text from PDFs, scanned documents, Arxiv papers.

→ `references/ocr-and-documents.md` — pymupdf (lightweight) and marker-pdf (high-quality OCR). Scripts: `scripts/extract_pymupdf.py`, `scripts/extract_marker.py`.

## GIF Search
**Trigger:** Search/download GIFs from Tenor.

→ `references/gif-search.md` — Tenor API via curl + jq.

## Teams Meetings
**Trigger:** Teams meeting summaries, transcripts, pipeline status.

→ `references/teams-meeting-pipeline.md` — `hermes teams-pipeline` CLI. Validate, list, show, replay, subscription management.

## Maps
**Trigger:** Geocoding, POIs, routes, timezones, nearby places.

→ `references/maps_client.py` (in `scripts/`) — OpenStreetMap/Nominatim, Overpass API, OSRM. 8 commands, 44 POI categories, zero dependencies.
