---
name: marketing
version: 1.0.0
description: "Social media automation, content scheduling, analytics tracking, and campaign management. Transform your AI agent into a marketing powerhouse that handles multi-platform content strategy."
author: openclaw
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Marketing Skill 📢

**Turn your AI agent into a strategic marketing partner.**

Handle social media, content scheduling, analytics, and campaign management across platforms — without constant manual input.

---

## What This Skill Does

✅ **Content Creation** — Generate posts, threads, newsletters, and visual content descriptions
✅ **Multi-Platform Management** — Twitter/X, LinkedIn, Instagram, Facebook, newsletters
✅ **Scheduling & Automation** — Plan content calendars, schedule posts, maintain consistency
✅ **Analytics Tracking** — Monitor engagement, track KPIs, identify trends
✅ **Campaign Management** — Plan campaigns, track performance, A/B testing insights
✅ **Brand Voice Consistency** — Maintain tone and style across all content

---

## Quick Start

1. Configure your marketing preferences in `TOOLS.md`:
```markdown
### Marketing
- Brand voice: [Professional/Casual/Witty/etc.]
- Primary platforms: [Twitter, LinkedIn, etc.]
- Posting frequency: [Daily/3x week/etc.]
- Target audience: [Description]
```

2. Set up your content calendar:
```bash
./scripts/content-calendar.sh init
```

3. Start creating content!

---

## Content Strategy Framework

### The AIDA Model for Posts

| Stage | Purpose | Example Hook |
|-------|---------|--------------|
| **Attention** | Stop the scroll | "Most marketers waste 80% of their budget on this..." |
| **Interest** | Build curiosity | "Here's what the top 1% do differently..." |
| **Desire** | Create want | "Imagine doubling your engagement in 30 days..." |
| **Action** | Drive behavior | "Try this today: [actionable tip]" |

### Platform-Specific Best Practices

**Twitter/X:**
- Optimal length: 100-280 characters
- Use threads for long-form (5-15 tweets)
- Hook in first line — no fluff
- 1-2 hashtags max
- Best times: 9am, 12pm, 5pm local

**LinkedIn:**
- Professional but personable tone
- Open with a bold statement or question
- Use line breaks for readability
- 1300-2000 characters performs best
- Include relevant hashtags (3-5)

**Instagram:**
- Visual-first thinking
- Captions: tell a story
- Hashtag strategy: 20-30 in first comment
- Call-to-action in every post
- Carousel posts get highest engagement

**Newsletter:**
- Subject lines: 40-60 characters
- Preview text matters (first 90 chars)
- One clear CTA per email
- Personal stories increase open rates
- Send consistently (same day/time)

---

## Content Calendar Management

### Monthly Planning Template

```markdown
# [Month] Content Calendar

## Themes
- Week 1: [Theme]
- Week 2: [Theme]
- Week 3: [Theme]
- Week 4: [Theme]

## Key Dates
- [Date]: [Event/Holiday]

## Content Mix (per week)
- Educational: 3
- Promotional: 1
- Engagement: 2
- User-generated/Curated: 1

## Platform Schedule
| Day | Twitter | LinkedIn | Instagram | Newsletter |
|-----|---------|----------|-----------|------------|
| Mon | Thread  | Article  | Carousel  | -          |
| Tue | Tips    | -        | Story     | -          |
| Wed | Poll    | Post     | Reel      | Send       |
| Thu | Thread  | -        | Story     | -          |
| Fri | Fun     | Post     | Post      | -          |
```

### Content Batching Workflow

1. **Ideation Day** (Monthly) — Brainstorm 30+ content ideas
2. **Creation Day** (Weekly) — Write next week's content in one session
3. **Scheduling Day** (Weekly) — Load content into scheduler
4. **Engagement Day** (Daily) — Respond to comments, engage with community

---

## Analytics & KPIs

### Key Metrics to Track

| Metric | What It Tells You | Target Growth |
|--------|-------------------|---------------|
| Impressions | Reach | +10% monthly |
| Engagement Rate | Content quality | >3% (Twitter), >5% (LinkedIn) |
| Click-through Rate | CTA effectiveness | >2% |
| Follower Growth | Audience building | +5% monthly |
| Conversion Rate | Business impact | Varies by goal |

### Weekly Analytics Template

```markdown
# Week of [Date] - Analytics Report

## Summary
- Total impressions: [X]
- Total engagement: [X]
- New followers: [X]
- Top performing post: [Link]

## Platform Breakdown

### Twitter
- Impressions: [X]
- Engagement rate: [X]%
- Best day: [Day]
- Top tweet: [Content]

### LinkedIn
- Impressions: [X]
- Engagement rate: [X]%
- Comments: [X]
- Top post: [Content]

## Insights
- What worked: [Analysis]
- What didn't: [Analysis]
- Next week focus: [Adjustment]
```

---

## Campaign Management

### Campaign Planning Template

```markdown
# Campaign: [Name]

## Overview
- **Goal:** [Specific, measurable goal]
- **Timeline:** [Start] - [End]
- **Budget:** [Amount if applicable]
- **Success Metrics:** [KPIs]

## Target Audience
- Demographics: [Age, location, etc.]
- Pain points: [Problems we solve]
- Platforms: [Where they hang out]

## Content Assets
- [ ] Main announcement post
- [ ] Supporting content (X posts)
- [ ] Visuals/graphics
- [ ] Landing page copy
- [ ] Email sequence

## Schedule
| Date | Platform | Content | CTA |
|------|----------|---------|-----|
| [Date] | Twitter | [Content] | [Action] |

## Results (fill after)
- Reach: [X]
- Engagement: [X]
- Conversions: [X]
- ROI: [X]
- Learnings: [What we learned]
```

---

## Content Generation Prompts

### For Twitter Threads
```
Create a Twitter thread on [TOPIC]:
- Hook that stops scrolling
- 5-10 tweets of value
- Each tweet stands alone but builds on previous
- End with CTA and recap
- Conversational but authoritative tone
```

### For LinkedIn Posts
```
Write a LinkedIn post about [TOPIC]:
- Opening hook (1-2 lines)
- Personal story or observation
- Key insight or lesson
- Actionable takeaway
- Engagement question
- 1200-1500 characters
```

### For Newsletter
```
Draft newsletter on [TOPIC]:
- Compelling subject line (3 options)
- Personal opening
- Main value content
- One clear CTA
- PS line for bonus engagement
```

---

## Automation Workflows

### Daily Marketing Routine

```markdown
## Morning (30 min)
- [ ] Check overnight engagement
- [ ] Respond to comments/DMs
- [ ] Share 2-3 relevant posts from others
- [ ] Check trending topics for opportunities

## Afternoon (15 min)
- [ ] Post scheduled content (if not automated)
- [ ] Engage with 5 accounts in your niche
- [ ] Check analytics for unusual activity

## Weekly (1 hour)
- [ ] Review analytics dashboard
- [ ] Plan next week's content
- [ ] Batch create content
- [ ] Update content calendar
```

### Content Repurposing Matrix

| Original | Twitter | LinkedIn | Instagram | Newsletter |
|----------|---------|----------|-----------|------------|
| Blog Post | Thread | Summary post | Carousel | Highlight |
| Podcast | Quote tweets | Key insight | Audio clip | Episode notes |
| Video | Clip + thread | Embed | Reel | Behind scenes |
| Thread | - | Expanded post | Story series | Compilation |

---

## Brand Voice Guidelines

### Voice Definition Template

```markdown
# Brand Voice

## We Are
- [Trait 1]: [Example]
- [Trait 2]: [Example]
- [Trait 3]: [Example]

## We Are Not
- [Anti-trait 1]: [Why to avoid]
- [Anti-trait 2]: [Why to avoid]

## Tone Spectrum
Formal ----[X]---- Casual
Serious ----[X]---- Playful
Reserved ----[X]---- Enthusiastic

## Sample Phrases
- Instead of "Click here" → "Dive in"
- Instead of "Buy now" → "Start your journey"
- Instead of "We're the best" → "Here's what we learned"

## Emoji Usage
- Frequency: [Sparingly/Moderate/Freely]
- Favorites: [List emojis that fit brand]
- Never use: [Emojis to avoid]
```

---

## Scripts

### content-calendar.sh
Manage your content calendar from the command line.

```bash
# Initialize calendar
./scripts/content-calendar.sh init

# Add content
./scripts/content-calendar.sh add "2024-01-15" "twitter" "Thread on productivity"

# View week
./scripts/content-calendar.sh week

# View month
./scripts/content-calendar.sh month
```

### analytics-report.sh
Generate weekly analytics summaries.

```bash
# Generate this week's report
./scripts/analytics-report.sh weekly

# Compare to last week
./scripts/analytics-report.sh compare
```

---

## Integration Tips

### With Other Skills

| Skill | Integration |
|-------|-------------|
| **Data Analyst** | Deeper analytics, trend visualization |
| **Sales** | Align campaigns with sales pipeline |
| **Business Development** | Content for partnerships |

### Common Workflows

**Content from Meetings:**
When you have a meeting transcript, extract quotable insights for social content.

**Analytics to Strategy:**
Use data-analyst skill to visualize marketing performance and identify optimization opportunities.

---

## Best Practices

1. **Consistency > Perfection** — Regular posting beats occasional perfection
2. **80/20 Content Rule** — 80% value, 20% promotion
3. **Engage, Don't Broadcast** — Social is a conversation
4. **Test Everything** — A/B test hooks, CTAs, posting times
5. **Batch Create** — Write a week's content in one focused session
6. **Repurpose Ruthlessly** — One idea, multiple formats
7. **Track What Matters** — Pick 3-5 KPIs, ignore vanity metrics
8. **Stay Authentic** — People follow people, not brands

---

## Troubleshooting

**Low engagement?**
- Check posting times against audience activity
- Review hooks — are they scroll-stopping?
- Increase engagement with others (reciprocity works)

**Inconsistent posting?**
- Batch create content weekly
- Use scheduling tools
- Create content bank for backup

**Off-brand content?**
- Review brand voice guidelines
- Create swipe file of good examples
- Check content before posting

---

## License

**License:** MIT — use freely, modify, distribute.

---

*"Marketing is no longer about the stuff you make, but about the stories you tell." — Seth Godin*

---

# AGENT DIRECTIVE: Execution Protocol

> **CRITICAL INSTRUCTION FOR ALL MIFECO AGENTS**

## The Golden Rule

**DO NOT SUGGEST ACTIONS. EXECUTE THEM.**

### What This Means

| ❌ DON'T | ✅ DO |
|---------|-------|
| "You could create a file..." | Create the file. |
| "I recommend running this command..." | Run the command. |
| "Here's a script you might use..." | Execute the script. |
| "Would you like me to...?" | Just do it and report results. |

### Execution Standard

When assigned a task:

1. **Execute immediately** - Don't ask for permission unless explicitly blocked
2. **Report what you did** - Not what you "would" do
3. **Show results** - Output, files created, changes made
4. **Escalate on failure** - Don't stall, notify immediately

## Failure Protocol

If you **CANNOT** perform an action:

**STEP 1:** Try alternative approaches (max 2 attempts)

**STEP 2:** If still blocked, send immediate notification:

```json
{
  "timestamp": "ISO-8601",
  "task_id": "original-task-id",
  "from": "your-agent-id",
  "to": "ceo",
  "type": "alert",
  "priority": "high",
  "task": "FAILED: [brief description]",
  "payload": {
    "error": "Specific error message",
    "attempted": ["what you tried"],
    "blocker": "why it failed",
    "needs": "what is needed to proceed"
  },
  "status": "failed"
}
```

**STEP 3:** Send Telegram notification:

```
🚨 AGENT FAILURE ALERT

Agent: [your-agent-id]
Task: [task_id]
Error: [specific error]

Needs: [what is required]
Timestamp: [ISO-8601]
```

## Telegram Notification Template

Use this exact format for Telegram alerts:

```
🚨 [AGENT] FAILED: [Brief Task Description]

Error: [Specific error message]
Attempted: [What you tried]
Blocker: [Why it failed]

Needs CEO/Board attention to proceed.
Task ID: [task_id]
```

## When to Notify

Send Telegram alert immediately for:
- ❌ Tool execution failures (exec, edit, write fail)
- ❌ Permission denied errors
- ❌ External API failures (non-recoverable)
- ❌ Missing required files/data
- ❌ Agent spawn failures
- ❌ Security/policy blocks

**DO NOT** alert for:
- ✅ Retrying after transient failures (network, rate limits)
- ✅ Clarifying ambiguous instructions (ask first)
- ✅ Expected delays (report in status updates)

## Examples

### Good Execution

User: "Create a backup script"

Agent:
```
Created backup.sh in /home/bob/scripts/

Contents:
#!/bin/bash
# Backup script
tar -czf backup-$(date +%Y%m%d).tar.gz ~/workspace

Tested: ✅ Executes successfully
Next backup: Tonight at 2 AM via cron
```

### Good Failure Handling

Agent encounters error:
```
Attempt 1: Failed - Permission denied on /etc/config
Attempt 2: Failed - sudo not available in this environment

🚨 Sending alert to CEO...

Telegram notification sent.
Waiting for escalation.
```

## Mandatory Footer

All agent responses must follow this structure:

```
[EXECUTION RESULT]

What was done: [specific actions]
Output/Results: [what happened]
Files changed: [list if any]
Status: ✅ Complete | ⏳ In Progress | ❌ Blocked

If Blocked:
🚨 Telegram alert sent: [yes/no]
Next action: [what happens next]
```

## Agent Self-Check

Before responding, verify:

- [ ] Did I actually DO the thing, or just describe it?
- [ ] Did I run the command, or just paste it?
- [ ] Did I create the file, or just show the content?
- [ ] If blocked, did I send the Telegram alert?

**Remember: Actions speak louder than suggestions.**
---

## AUTO-CONTINUE SYSTEM

This agent is monitored by the auto-continue system. If your response contains:
- Suggestions without actions ('could', 'would', 'might')
- Passive language ('consider', 'think about')
- Questions instead of execution

The system will automatically generate a CONTINUE prompt within 10 minutes.
To prevent this: ALWAYS execute immediately and show concrete results.

See AGENT_DIRECTIVE.md for complete protocol.
