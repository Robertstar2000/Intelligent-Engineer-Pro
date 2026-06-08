---
template: virtual-consulting-client-email
description: Custom email sent to client after Phase 0 pre-engagement research, containing a survey link with pre-filled questions.
---

# Client Email Template

## Subject Line

```
Your MIFECO AI Readiness Assessment — Let's Get Started
```

**Alternatives by trigger:**
- If client is a referral: `[Referrer Name] recommended we connect — your AI readiness survey is ready`
- If client expressed urgency: `Your AI Readiness Assessment — I've already started researching [Company]`
- If client is skeptical: `No commitment needed — just a comprehensive survey to see if AI fits your business`

---

## Email Body

```
Dear [Client First Name],

Thank you for trusting MIFECO Virtual Consulting with your AI readiness assessment. I've already begun researching [Client Company].

[PERSONALIZED INSIGHT — one line from Phase 0 research]

I've prepared a comprehensive survey that covers everything I need to build your two custom reports:

📋 Quality Assessment — 30-page deep analysis of your readiness, opportunities, and risks
📋 Deployment Plan — 30-page phased implementation roadmap with tools, training, and ROI

The survey covers 12 areas of your business and adapts to your answers. You can:
• Complete it at your own pace — just type "save" and come back anytime
• Skip any question
• Pick up exactly where you left off

Ready to begin? Reply to this message and I'll walk you through the first section.

Best regards,
Bob Mills
MIFECO Virtual Consulting
```

---

## Survey Content (Sent as Link or Inline)

### Section 1: Business Profile — Confirmation

The following is what I found from public sources. Please confirm or correct:

1. **Your business name is:** [Pre-filled: Company Name]
   - ✅ Correct
   - ✏️ It's actually: ___________

2. **Your industry appears to be:** [Pre-filled: Industry]
   - ✅ Correct
   - ✏️ It's actually: ___________

3. **Your team size appears to be around:** [Pre-filled: Employee range]
   - ✅ Correct
   - ✏️ We're actually about: ___________ employees

4. **Your website is:** [Pre-filled: URL]
   - ✅ Correct
   - ✏️ It's actually: ___________

### Section 2: Time & Pain Points

5. **What are the top 3 tasks that consume most of your time each week?**
   - [Open text — 3 lines]

6. **On a scale of 1-5, how frustrated are you with how much time these tasks take?**
   - 1 (Not frustrated — it's fine)
   - 2
   - 3 (Moderately frustrating)
   - 4
   - 5 (Extremely — I need a solution)

7. **What's the ONE thing you'd automate tomorrow if you could?**
   - [Open text]

### Section 3: Data & Technology

8. **What software/tools do you currently use for daily operations?** (Check all that apply)
   - ☐ Email (which platform? ___________)
   - ☐ Calendar/scheduling
   - ☐ CRM (which one? ___________)
   - ☐ Accounting/bookkeeping (which one? ___________)
   - ☐ Project management (which one? ___________)
   - ☐ Social media management
   - ☐ E-commerce platform
   - ☐ Customer support tools
   - ☐ Other: ___________

9. **How is your customer/sales data currently stored?**
   - ☐ Spreadsheets
   - ☐ CRM system
   - ☐ Paper/files
   - ☐ Various places (no central system)
   - ☐ Not sure
   - ☐ Other: ___________

### Section 4: Goals & Budget

10. **What's your most important business goal for the next 6-12 months?**
    - [Open text]

11. **If you could save 10 hours per week, where would you reinvest that time?**
    - [Open text]

12. **What's your approximate monthly budget for new software/tools?**
    - ☐ Under $100/month
    - ☐ $100-$500/month
    - ☐ $500-$2,000/month
    - ☐ $2,000+/month
    - ☐ Not sure / need to discuss

### Section 5: AI Attitudes

13. **Have you tried AI tools before?**
    - ☐ Yes, and it was positive
    - ☐ Yes, but it didn't work well
    - ☐ No, but I'm curious
    - ☐ No, and I'm skeptical

14. **What concerns you most about adopting AI?** (Select top 2)
    - ☐ Cost
    - ☐ Complexity / too technical
    - ☐ My team won't use it
    - ☐ Security / data privacy
    - ☐ It won't work for my type of business
    - ☐ I don't know where to start
    - ☐ Other: ___________

### Section 6: Change Readiness

15. **How would you describe your team's attitude toward new technology?**
    - 1 (Very resistant — they hate change)
    - 2
    - 3 (Neutral — they'll try it)
    - 4
    - 5 (Very open — they love new tools)

16. **Is there anything else you'd like me to know before we dive deeper?**
    - [Open text]

---

## Delivery Instructions

1. **Create state directory** — `mkdir -p ~/.hermes/skills/virtual-consulting/state/`
2. **Generate survey state file** — Initialize JSON with all 12 sections, question IDs, pre-filled answers, and confidence levels
3. **Generate email** — Personalize with client name, company, and one research insight
4. **Send opening message** via Telegram DM (default):
   - First message: The overview of what's happening (2 reports, 12 sections, save/resume)
   - Second message: The opening question — "Ready to begin?"
5. **On "yes"** → Begin Section A, present one question at a time
6. **On "not now"** → Save state, say "Come back anytime — type 'resume' to continue"
7. **On "send me the questions"** → Send the full survey as a document, then process answers as they arrive
8. **On every response** → Validate, store, auto-save every 5 questions
9. **On "save"** → Persist state, show progress summary, confirm resume command
10. **On "resume"** → Load state file, show current section, re-display current question
11. **On "skip"** → Log to assumptions file with grade E, move to next question
12. **On survey complete** → Generate both 30-page reports and deliver
13. **Track response** — Set a reminder to follow up if no activity within 48 hours
