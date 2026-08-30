---
name: virtual-consulting-orchestrator
description: "Orchestrate mifeco virtual consulting from lead generation through payment-gated onboarding, survey design, multi-person survey collection, structured data capture, deliverable generation, QA review, and client delivery. Use when running or supporting a virtual consulting workflow involving LinkedIn or X organic promotion, targeted email outreach, Stripe payment links, onboarding surveys, role-based follow-up surveys, database-backed evidence collection, consulting analysis, or final deliverable packaging for business advisory, AI strategy, automation, and forward strategy engagements."
---


## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

Virtual Consulting Orchestration

Run MIFECO's virtual consulting workflow as a structured revenue and delivery system.

Treat this as an end-to-end consulting operations skill, not a generic advisory writing task. Move in sequence from lead generation to onboarding, evidence collection, analysis, deliverable creation, QA, and delivery.

Use short, business-ready language. Keep all outputs decision-oriented. Do not allow consulting to begin until payment is confirmed.

Core operating rule

Start delivery only after the client has paid through the Stripe payment link.

If payment is not confirmed:
- continue lead nurturing
- answer pre-sales questions
- refine offer positioning
- prepare onboarding materials
- do not begin paid consulting analysis or custom deliverable creation

Primary workflow

Execute this workflow in order.
1. Define engagement
2. Generate and manage leads
3. Send outreach
4. Confirm payment
5. Build client-specific intake survey
6. Collect primary stakeholder responses
7. Trigger additional employee surveys
8. Store and normalize all responses in the database
9. Analyze evidence
10. Generate tailored deliverables
11. Run QA review
12. Deliver results by email with links
13. Log status and next-step opportunities

Engagement definition

At the start of each client workflow, classify the engagement into one of these service types:
- AI Strategy Consulting
- Automation Consulting
- Agent Systems Implementation
- Virtual Advisory / Diagnostic
- Other fixed-scope custom consulting

For each engagement, define:
- client name
- client industry
- employee count range
- offer purchased
- pricing tier
- Stripe payment status
- primary business objective
- expected deliverables
- turnaround target
- key contacts
- lead source

If the user does not specify all fields, infer what is reasonable from provided context and mark missing items clearly.

Lead generation model

Operate with two sales channels only.

Channel 1: Organic social promotion

Create no-cost posts for:
- LinkedIn
- X

Each post must:
- speak to a specific pain point
- point toward a clear business outcome
- include a call to action
- include the correct buy/start link
- match the selected service offering
- avoid sounding generic or overly promotional

When writing social posts:
- create platform-specific versions
- keep LinkedIn more explanatory and authority-driven
- keep X shorter and sharper
- include one clear next step only
- point readers to the website or purchase/onboarding link

Preferred CTA pattern:
- buy the session
- start the assessment
- begin the AI readiness process
- get the diagnostic
- request the advisory package

Track for each post:
- platform
- post date
- theme
- offer promoted
- link used
- clicks if available
- conversions if available

Channel 2: Researched targeted email outreach

Research likely leads before drafting outreach.

For each prospect, gather:
- company name
- website
- industry
- size estimate
- likely pain points
- relevant AI, process, or growth signals
- target contact name
- role
- email
- reason they fit
- likely offer match

Use the research to decide:
- whether to contact them
- which service to pitch
- which business problem to reference
- which proof points to use

Draft targeted outreach that:
- opens with a relevant business observation
- shows understanding of the company context
- connects the problem to a practical outcome
- offers one relevant consulting entry point
- includes a clear CTA
- includes the purchase or start link when appropriate

Do not send generic mass-email language. Personalization must be grounded in research, not invented.

Track for each outreach record:
- company
- contact
- role
- date sent
- message variant
- service offered
- response status
- follow-up date
- outcome

Lead tracker requirements

Maintain a structured lead tracker.

Minimum lead tracker fields:
- lead_id
- created_date
- source_channel
- company_name
- industry
- company_size
- website
- contact_name
- contact_email
- contact_role
- research_summary
- key_pain_points
- matched_offer
- outreach_status
- last_contact_date
- next_action_date
- stripe_link_sent
- payment_status
- onboarding_status
- survey_status
- deliverable_status
- final_outcome
- notes

Suggested statuses:
- researched
- queued
- contacted
- replied
- qualified
- link sent
- paid
- onboarding started
- intake received
- employee surveys in progress
- analysis in progress
- deliverables under review
- delivered
- upsell opportunity
- closed lost

Payment gating

Use Stripe payment as the gate between sales and delivery.

Required payment actions:
- generate or reference the correct Stripe link
- send payment link in CTA or follow-up email
- log link sent date
- confirm payment
- mark engagement as active only after payment confirmation

Do not send custom surveys or perform paid analysis before payment unless the user explicitly defines a free pre-sales diagnostic.

Onboarding survey design

After payment, create a primary intake survey tailored to:
- the purchased service
- the client's business context
- lead research already collected
- likely decision-maker priorities

Survey design rules:
- use dropdowns and checkboxes as much as possible
- use short text only where necessary
- avoid redundant questions
- group questions by business theme
- ask only for information that will feed analysis or deliverables
- keep completion friction low
- make role and department labels standardized

Primary intake survey sections should usually include:
- company profile
- strategic priorities
- current pain points
- current systems and tools
- process maturity
- AI / automation maturity
- known constraints
- business goals
- target outcomes
- current projects
- risk or compliance concerns
- success criteria
- internal decision structure
- key employee list

Key employee capture

The primary survey must require the client to identify additional stakeholders.

Collect for each listed employee:
- full name
- email
- role
- department
- relationship to the project
- priority area
- whether survey required

Supported role categories may include:
- CEO / president
- COO
- CTO / CIO / IT leader
- operations leader
- sales leader
- marketing leader
- finance leader
- HR leader
- product leader
- engineering leader
- customer service leader
- plant / manufacturing leader
- other

Follow-up survey orchestration

After the primary survey is submitted, generate additional role-specific surveys for listed employees.

Tailor each survey based on:
- their role
- department
- engagement type
- strategic priorities named by the main contact
- contradictions or unknowns in earlier responses
- expected deliverables

Examples:
- executives: strategy, priorities, investment logic, growth constraints
- operations leaders: workflow bottlenecks, manual effort, handoffs, KPIs
- IT leaders: systems, data quality, integration constraints, security concerns
- sales leaders: pipeline issues, CRM gaps, forecasting, response speed
- finance leaders: ROI, budget controls, risk tolerance, investment timing
- HR leaders: capability gaps, change management, adoption barriers
- plant or manufacturing leaders: throughput, quality, test data, downtime, paper processes

Each follow-up survey should:
- confirm the person and role
- ask targeted operational questions
- use dropdowns and checkboxes where possible
- ask for examples only where needed
- capture pain severity
- capture current-state maturity
- capture desired future state
- capture dependencies and risks

Survey logic rules

Design surveys to reveal:
- strategic intent
- operational bottlenecks
- technology maturity
- data maturity
- organizational readiness
- conflicting stakeholder views
- missing ownership
- likely ROI opportunities
- implementation barriers

Explicitly look for:
- misalignment between employee answers
- executive goals not reflected in operations
- tool sprawl
- duplicate work
- manual process dependencies
- poor data quality
- unclear accountability
- inconsistent definitions of success
- adoption resistance
- unrealistic expectations

When contradictions appear:
- flag them in the database
- reference them in the analysis
- use them to shape recommendations

Database requirements

Store all collected information in a structured database suitable for downstream generation of deliverables.

Minimum entities:

Leads
- lead_id
- source
- research notes
- outreach history
- qualification data

Clients
- client_id
- company data
- purchased offer
- payment status
- delivery status

Contacts
- contact_id
- client_id
- name
- email
- role
- department
- influence level

Surveys
- survey_id
- client_id
- contact_id
- survey_type
- version
- sent_date
- completion_status

Survey Responses
- response_id
- survey_id
- question_id
- normalized_answer
- raw_answer
- confidence_flag
- contradiction_flag

Findings
- finding_id
- client_id
- theme
- severity
- evidence source
- impacted area
- recommendation link

Deliverables
- deliverable_id
- client_id
- deliverable_type
- version
- status
- delivery_link
- delivery_date

Audit / QA
- review_id
- deliverable_id
- reviewer
- issue_type
- issue_status
- notes

Normalize answer options where possible so analysis can compare respondents across roles.

Analysis process

Once enough survey data is collected, synthesize all evidence into a consulting-grade view.

Analyze in this order:
1. client objectives
2. current-state maturity
3. pain points
4. system and process constraints
5. stakeholder alignment
6. role-based contradictions
7. near-term opportunities
8. longer-term strategic direction
9. implementation risks
10. recommended actions

Always separate:
- evidence
- interpretation
- recommendation

Do not present guesses as facts.

Required outputs

Generate a tailored deliverable set from the collected evidence.

The standard output set may include:
- Executive Summary
- Analysis Report
- AI Readiness Score
- Opportunity Matrix
- Roadmap
- Misalignment Between Employee Answers
- Forward Strategy
- Automation Recommendations
- Org / Role Recommendations
- Tool Stack Recommendations
- Implementation Plan

Only include outputs that fit the engagement. If something is not supported by the evidence, say so clearly.

1. Executive Summary

Include:
- client context
- top opportunities
- top risks
- major constraints
- recommended direction
- immediate next steps

Keep concise and decision-ready.

2. Analysis Report

Include:
- business context
- current-state summary
- process and technology observations
- stakeholder themes
- detailed findings
- evidence-backed interpretations
- priority conclusions

3. AI Readiness Score

Score relevant dimensions such as:
- leadership readiness
- data readiness
- process readiness
- technology readiness
- change readiness
- governance readiness

Explain score meaning plainly. Include reasons, not just numbers.

4. Opportunity Matrix

Rank opportunities by:
- business value
- ease of implementation
- required data quality
- organizational readiness
- time to impact

Use practical prioritization language.

5. Roadmap

Structure by phase:
- 0 to 30 days
- 30 to 90 days
- 90 to 180 days
- 6 to 12 months

Connect each phase to outcomes, owners, and dependencies.

6. Misalignment Between Employee Answers

Compare cross-role responses and surface:
- conflicting priorities
- inconsistent understanding of goals
- ownership confusion
- disagreement about process or tooling
- optimism gaps between leadership and operators

This section must remain factual and diplomatic.

7. Forward Strategy

Recommend how the client should move forward based on:
- readiness level
- business urgency
- resource constraints
- leadership alignment
- probable ROI

8. Automation Recommendations

Recommend specific automation targets.
For each, include:
- process area
- pain point
- expected gain
- required inputs
- implementation considerations

9. Org / Role Recommendations

Identify:
- missing ownership
- overloaded roles
- role ambiguity
- needed governance
- decision-maker gaps

10. Tool Stack Recommendations

Recommend categories and selection logic, not just product names.

Consider:
- CRM
- workflow automation
- AI copilots
- agent frameworks
- knowledge base
- analytics
- data integration
- survey tooling
- document automation

11. Implementation Plan

Include:
- workstreams
- owners
- milestones
- dependencies
- risks
- success measures

Deliverable writing rules

All deliverables must be:
- tailored to the client
- evidence-based
- concise but specific
- practical
- free of filler
- organized for executive reading

Do not overstate certainty.
Do not recommend tools or initiatives the client is not ready for without clearly saying why.

QA review

Before delivery, run a QA pass.

Check for:
- consistency with survey evidence
- contradictions between sections
- unsupported claims
- missing required deliverables
- unclear action items
- weak prioritization
- poor executive readability
- missing links between findings and recommendations

Also verify:
- client name is correct everywhere
- role names are correct
- payment was confirmed
- delivery links work
- email recipients are correct

If QA finds issues, revise before sending.

Delivery process

Deliver final outputs by email as links.

Delivery email must:
- confirm completion
- list included deliverables
- provide clear links
- summarize major findings briefly
- state recommended next step
- invite follow-up discussion or implementation support

Log:
- delivery date
- recipients
- deliverables delivered
- link locations
- follow-up date

Recommended email and page assets

When supporting implementation, help create:
- LinkedIn post variants
- X post variants
- cold outreach email variants
- Stripe payment email templates
- onboarding email templates
- reminder email templates
- survey invitation email templates
- survey reminder email templates
- deliverable delivery email templates
- landing page copy for https://www.mifeco.com

Landing page guidance

When generating website copy for MIFECO:
- explain the offer clearly
- make the process easy to understand
- show business outcomes
- reduce friction to buy
- connect page CTA to Stripe or onboarding start
- align wording with the specific consulting offer

Suggested page flow:
- problem
- offer
- who it is for
- process
- deliverables
- pricing or consultation entry point
- CTA

Decision logic

Use this branching logic:

If no lead exists:
- create or refine acquisition content

If lead exists but is not researched:
- research the lead first

If lead is researched but not contacted:
- draft targeted outreach

If lead replied but has not paid:
- move toward qualification and payment link

If paid but no intake submitted:
- send onboarding survey

If intake submitted and additional stakeholders are listed:
- generate and send tailored follow-up surveys

If surveys are incomplete:
- send reminders and log gaps

If enough evidence is collected:
- perform analysis and draft deliverables

If draft deliverables exist:
- run QA

If QA passes:
- send delivery email with links

If delivered:
- log follow-up and identify upsell or implementation support opportunities

Output preferences

When asked to perform a task under this skill, return work in the format that best fits the step, such as:
- lead research brief
- outreach email
- social post set
- survey blueprint
- database schema draft
- findings summary
- deliverable outline
- final deliverable draft
- QA checklist
- client delivery email

Notes for reliability

Prefer structured fields over free text wherever possible.
Preserve source evidence for all major findings.
Track contradictions explicitly.
Keep the workflow payment-gated.
Bias toward actionable recommendations over broad theory.
Make each output usable by a real client-facing consulting operation.

Sign-post: ready for the next upgrade.

The strongest next step is for me to turn this into a fuller operational version with:
- a lead tracker schema
- survey question banks by role
- email templates
- landing page copy blocks
- deliverable templates
