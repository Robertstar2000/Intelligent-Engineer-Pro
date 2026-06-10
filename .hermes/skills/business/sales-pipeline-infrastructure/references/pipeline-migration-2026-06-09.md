# Migration: 9 to 5 Product Pipelines (2026-06-09)

See SKILL.md for the full 5 pipeline definitions with stage details, products, email, and nurture info.

## Lead Stage Remapping Summary

- Consulting C-leads: old 8-stage mapped 1:1 to new 8-stage (Lead→Contact→Qualified→Intent→Strategy Session→Proposal→Negotiation→Closed Won)
- SaaS S-leads: old 8-stage mapped 1:1 to new 8-stage (Identified→Contacted→Qualified→Process→Demo/Trial→Transaction→Followup→Upsell)
- Books B-leads: remapped to Books Marketing 8-stage

## Dead Leads Removed
- C-005 (Summit Nonprofit Alliance) - fictional company
- C-008 (Golden Gate Tech Incubator) - fictional company

## Files Replaced
- unified-pipeline.json - 5 pipeline definitions
- pipeline-state.json - 5 pipeline statuses
- pipeline-books.json - catalog + marketing leads
- pipeline-saas.json - products + leads (stages remapped)
- pipeline-consulting.json - services + leads (Human + Virtual)
- flows/*.svg - 5 new diagrams (9 old deleted)
- pipeline-dashboard.html - new tabbed 5-pipeline UI
