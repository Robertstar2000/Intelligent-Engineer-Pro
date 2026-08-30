---
name: project-management
description: "Project Management skill for MIFECO's Project Management SaaS product — AI-driven workflow orchestration, task coordination, and execution management. Third in the SaaS stack (Science → Engineering → Project Management). Use when building, deploying, or operating PM tooling: task management, resource allocation, milestone tracking, dependency mapping, sprint planning, and delivery coordination."
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Project Management SaaS — Product Skill

## Overview

Project Management is the **third SaaS product** in MIFECO's product stack:
- **Science** (1st) — AI research synthesis and scientific analysis
- **Engineering** (2nd) — AI-augmented software development
- **Project Management** (3rd) — AI-driven workflow orchestration and execution management

Project Management SaaS receives output from Engineering (development tasks) and orchestrates execution across teams.

**ARR target:** Contributes to $280K ARR target at 24 months (alongside Science and Engineering, sold separately).

---

## Core PM Functions

### Workflow Orchestration
- Define and manage project workflows
- Automate task handoffs between teams and stages
- Route work based on dependencies and capacity
- Trigger downstream actions when upstream completes

### Task Coordination
- Create, assign, and track tasks across projects
- Set priorities, deadlines, and owners
- Monitor task status in real-time
- Identify and resolve blockers

### Resource Allocation
- Track team capacity and availability
- Assign work based on skills and bandwidth
- Balance workloads across concurrent projects
- Optimize resource utilization

### Milestone & Dependency Mapping
- Define project milestones and key dates
- Map task dependencies (what blocks what)
- Track critical path and slack
- Alert on at-risk dependencies

### Sprint & Delivery Management
- Plan sprints and release cycles
- Track velocity and burndown
- Manage scope changes and tradeoffs
- Coordinate delivery handoffs

### AI-Augmented Features
- Auto-schedule tasks based on priorities and capacity
- Predict delivery dates from historical velocity
- Surface risks before they become blockers
- Generate status reports from live data

---

## Product Specifications

### Target Users
- Operations-heavy organizations
- Software development teams
- Project-based businesses (consulting, agencies)
- Multi-team coordination scenarios

### Integration Points
- Receives input from **Engineering SaaS** (completed development tasks → PM execution)
- Outputs to delivery and client reporting
- Connects to Science SaaS for data-driven planning
- All three products share a common data layer

### Pricing
- Sold separately (per board Decision 10: no bundle)
- Entry tier, professional tier, enterprise tier
- Annual and monthly options

---

## Operating Rules

- PM SaaS launches **third** (after Science and Engineering validated)
- First priority: internal validation before external sale
- Beta customers from consulting engagements get early access
- Route all PM SaaS updates to topic ID 13 (SaaS / AaaS product line)

---

## PM Framework Applied

### Phase 1: Initiation
- Define project scope, objectives, and success criteria
- Identify stakeholders and decision-makers
- Establish governance and reporting cadence
- Capture constraints (budget, timeline, resources)

### Phase 2: Planning
- Break down work into actionable tasks
- Sequence tasks by dependency
- Estimate effort and duration
- Assign owners and set deadlines
- Identify risks and mitigation strategies

### Phase 3: Execution
- Track task completion in real-time
- Monitor dependency health
- Manage scope changes via change control
- Conduct standups and status reviews
- Resolve blockers quickly

### Phase 4: Monitoring & Control
- Track KPIs: velocity, burndown, on-time delivery rate
- Monitor critical path health
- Surface at-risk tasks early
- Generate automated status reports
- Trigger alerts on milestone misses

### Phase 5: Closure
- Validate all deliverables completed
- Conduct retrospective
- Document lessons learned
- Archive project data
- Transition to ongoing operations

---

## Metric Tracking

| Metric | Target |
|---|---|
| On-time delivery rate | > 85% |
| Task completion rate | > 90% |
| Blocker resolution time | < 24 hours |
| Sprint velocity variance | < 15% |
| Resource utilization | 70–85% |
| Customer satisfaction | > 4.5/5 |

---

## Escalation

Escalate to CEO for:
- Major product decisions
- Customer complaints or churn signals
- Pricing changes
- Feature scope changes
- Integration blockers with Science or Engineering

Escalate to saas-operations for:
- Subscription management issues
- Billing problems
- Customer support requests

---

## Integration with MIFECO Product Lines

- **Science** → Research outputs feed PM planning (data-driven scheduling)
- **Engineering** → Development tasks flow into PM for execution tracking
- **Books** → Not directly integrated (authority assets)
- **Consulting** → PM tools used in delivery engagements; consulting clients = early PM SaaS customers
