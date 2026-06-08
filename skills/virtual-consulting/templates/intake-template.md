# MIFECO Virtual Consulting — Initial Intake Template

**Framework Source:** *AI That Works for Small Business* (Bob Mills)
**Methodology:** Assess → Choose → Implement → Optimize
**Purpose:** This template structures the first conversation with a client to gather essential business context, identify pain points, assess readiness, and establish a foundation for the consulting engagement.

---

## SECTION 1 — Business Profile

**Purpose:** Establish baseline context about who the client is, what they do, and their current technology environment.

### Questions

1. **What is your business name, and can you describe in one sentence what you do?**
   - *Follow-up:* What industry or industries do you serve? (e.g., retail, manufacturing, professional services, healthcare, hospitality)

2. **How many employees does your business have (full-time equivalents)? What is your approximate annual revenue?**
   - *Structured options:* ___ Sole proprietor / ___ 2-5 / ___ 6-20 / ___ 21-50 / ___ 50+ employees
   - *Revenue range:* ___ Under $250K / ___ $250K-$1M / ___ $1M-$5M / ___ $5M-$10M / ___ $10M+

3. **How many years has your business been in operation?**
   - *Structured options:* ___ Less than 1 year / ___ 1-3 years / ___ 4-10 years / ___ 10+ years

4. **What software, tools, or platforms do you and your team use on a daily or weekly basis?**
   - *Probe for:* Accounting/ERP, CRM, email, calendar, POS, project management, helpdesk, communication tools (Slack, Teams, etc.)
   - *Note completeness:* Are they using integrated suites or disconnected point solutions?

5. **Describe your current digital presence:**
   - Do you have a website? (If yes: is it static, e-commerce-enabled, or a custom platform?)
   - What social media channels do you actively maintain?
   - Do you sell products/services online? Through what platform?

### What to Look For / Red Flags
- **Tech debt warning:** Heavy reliance on paper, spreadsheets, or disconnected tools without integration
- **Digital gap:** No website or an outdated one (suggests fundamental digital readiness issues)
- **Growth misalignment:** Using tools designed for solo operators while managing a team of 10+
- **Over-customization:** Custom-built systems that create dependency and integration challenges

### Dynamic Follow-up Generation
*Use these prompts to generate additional questions based on client responses:*
- If the client mentions a specific industry pain point (e.g., "healthcare compliance"): generate questions about HIPAA readiness, patient data handling, and regulatory exposure.
- If the client lists no CRM: generate questions about how they track leads, follow-ups, and customer history.
- If the client reports rapid growth (recent hire surge, revenue jump): generate questions about systems scaling challenges.
- If the client mentions a legacy/on-premise system: generate questions about migration appetite, timeline, and budget.

---

## SECTION 2 — Pain Points & Time Audit

**Purpose:** Uncover the specific operational friction points and quantify where time is being lost — the primary targets for AI intervention.

### Questions

1. **What are your top 3 most time-consuming tasks each week?**
   - *For each:* Approximately how many hours per week do you spend on this?
   - *For each:* On a scale of 1-5, how much do you dread doing this task? (1 = don't mind it, 5 = absolutely hate it)

2. **What is your single biggest operational frustration right now — the thing that, if solved, would make the biggest difference in your day?**
   - *Open-ended, listen for emotional weight and frequency of mention*

3. **How do you handle customer service today?**
   - Roughly how many customer inquiries do you receive per day/week?
   - What channels do they come through? (phone, email, chat, social media, in-person)
   - Do you have a helpdesk or ticketing system?
   - What percentage of inquiries are repetitive/FAQ-type questions?
   - What happens to inquiries that come in after hours?

4. **Walk me through your sales and marketing process from start to finish.**
   - How do you find/attract new customers?
   - How do you track leads and follow-ups?
   - What does your typical sales cycle look like (timeframe, touchpoints)?
   - Where do leads most commonly fall through the cracks?

5. **On a typical day, what percentage of your time do you spend on high-value work (revenue-generating, strategic, creative) vs. low-value administrative work?**

### What to Look For / Red Flags
- **High dread scores (4-5) on repetitive tasks:** Prime candidates for automation
- **No lead tracking system:** Likely significant revenue leakage from missed follow-ups
- **Manual multi-channel customer service with no ticketing:** Customer experience risk, likely overwhelmed team
- **Vague descriptions of process:** Suggests undocumented, ad-hoc workflows that are harder to automate
- **Owner doing everything themselves:** Scalability ceiling, burnout risk

### Dynamic Follow-up Generation
*Use these prompts to generate additional questions based on client responses:*
- If the client mentions specific manual data entry: generate questions about error rates, reconciliation time, and duplicate work.
- If the client mentions being overwhelmed by customer inquiries: generate questions about peak times, average handle time, and abandoned inquiry rate.
- If the client has no defined marketing process: generate questions about current customer acquisition cost and reliance on word-of-mouth.
- If the client mentions hiring challenges: generate questions about onboarding time, training documentation, and knowledge retention.

---

## SECTION 3 — Data Readiness

**Purpose:** Evaluate the quality, accessibility, and structure of the client's data — the fuel for any AI implementation.

### Questions

1. **What customer or operational data does your business currently collect?**
   - *Prompt examples:* Contact information, purchase history, support interactions, inventory levels, financial transactions, website analytics, employee data
   - *For each:* Is this collected consistently or only occasionally?

2. **How is your data currently stored?**
   - *Structured options:* ___ Spreadsheets (Excel/Google Sheets) / ___ Database / ___ CRM system / ___ Paper/notebooks / ___ POS system / ___ Accounting software / ___ Cloud storage (Google Drive, Dropbox) / ___ No central system
   - *Probe for:* Is data stored in one place, or scattered across multiple tools?

3. **How would you rate the quality of your data?**
   - Are there duplicates, outdated entries, or incomplete records you're aware of?
   - How confident are you in the accuracy of your reports and numbers?
   - When was the last time you did a data cleanup?

4. **Who has access to your data, and how is it shared across your team?**
   - Do you have defined permissions or is it open access?
   - Can multiple people edit the same data simultaneously without version confusion?

5. **Do you currently generate any regular reports or dashboards from your data?**
   - If yes: What do you track? How frequently? Who uses them?
   - If no: What information would be most valuable to have at a glance?

### What to Look For / Red Flags
- **Paper-based records:** Requires digitization before any AI implementation — significant foundational investment needed
- **Spreadsheet-only data management:** Version control issues, error-prone, hard to integrate with AI tools
- **"We don't really track that" response:** Data gap that needs to be addressed before AI can be effective
- **No backups or security concerns raised:** Data vulnerability risk
- **Owner unsure about data accuracy:** Foundation trust issue — GIGO (garbage in, garbage out)

### Dynamic Follow-up Generation
*Use these prompts to generate additional questions based on client responses:*
- If the client uses spreadsheets for critical data: generate questions about version management, who updates them, frequency of errors.
- If the client mentions customer data scattered across tools: generate questions about data reconciliation efforts and customer experience consistency.
- If the client collects data but doesn't use it: generate questions about awareness of what's possible and motivation for change.
- If the client handles sensitive data (health, financial, children's): generate questions about compliance requirements and security protocols immediately.

---

## SECTION 4 — Goals & Constraints

**Purpose:** Align the consulting engagement with the client's business objectives and establish realistic parameters for the deployment plan.

### Questions

1. **What is your primary business goal for the next 6-12 months?**
   - *Examples to prompt:* Increase revenue / reduce costs / improve customer satisfaction / scale operations / improve work-life balance / launch new product/service / prepare the business for sale
   - *For each goal:* On a scale of 1-5, how urgent is this? (1 = nice to have, 5 = must achieve to survive)

2. **What budget range do you have in mind for AI investment (tools, implementation, training)?**
   - *Structured options:* ___ Under $100/month / ___ $100-$500/month / ___ $500-$2,000/month / ___ $2,000-$5,000/month / ___ $5,000+/month / ___ Unsure / ___ Willing to invest based on ROI case
   - *Note:* Distinguish between ongoing subscription costs and one-time implementation/setup costs

3. **On a scale of 1-5, how would you rate your personal comfort level with new technology?**
   - 1 = "I avoid technology whenever possible"
   - 3 = "I can learn new tools with some support"
   - 5 = "I actively explore and adopt new technology"
   - *Follow-up:* How would you rate your team's average comfort level using the same scale?

4. **What is your timeline urgency?**
   - *Structured options:* ___ Immediate (we need help this week) / ___ Short-term (within 1 month) / ___ Medium-term (within 3 months) / ___ Long-term (3-6+ months) / ___ Exploring (no fixed timeline)
   - *Follow-up:* Is there a specific event driving this timeline? (e.g., busy season coming, new competitor, owner health, investor pressure)

5. **What concerns or hesitations do you have about adopting AI?**
   - *Open-ended — listen for:* Job displacement fears, data security concerns, cost worries, time commitment, complexity, past negative experiences, skepticism about results

### What to Look For / Red Flags
- **Unrealistic budget expectations:** Expecting enterprise-grade AI for $50/month
- **Pressure without commitment:** "I need this solved yesterday" but no budget allocated
- **Tech-averse leadership (score 1-2):** Requires significant change management and hand-holding — may not be ready
- **Goal ambiguity:** "I want to grow" without specificity — needs coaching to define measurable objectives
- **Fear-based resistance:** Proactively address to prevent engagement derailment

### Dynamic Follow-up Generation
*Use these prompts to generate additional questions based on client responses:*
- If the client gives a very low budget: generate questions about willingness to do DIY implementation, open-source comfort, phased approach.
- If the client gives a very high urgency but low readiness: generate questions about acceptable risk tolerance and expectations for speed vs. quality.
- If the client mentions a specific event driving urgency: generate deeper questions about the stakes of failure and pressure sources.
- If the client expresses fear about job displacement: generate questions about team composition, their view on employee roles, and communication strategy.

---

## SECTION 5 — Risk Awareness

**Purpose:** Identify regulatory, security, and compliance requirements that will shape the AI architecture and tool selection.

### Questions

1. **What are your current security practices?**
   - Do you use password managers, two-factor authentication, or VPNs?
   - How are customer/employee data protected?
   - Do you have a data breach response plan?
   - Are your systems regularly updated and patched?

2. **Does your business operate in a regulated industry or handle regulated data?**
   - *Structured checklist:* ___ GDPR (EU customers) / ___ CCPA/CPRA (California customers) / ___ HIPAA (health data) / ___ PCI-DSS (payment card data) / ___ SOC 2 / ___ FINRA/SEC (financial services) / ___ COPPA (children's data) / ___ Other: __________ / ___ None of these apply
   - *Follow-up:* Are you currently compliant with these regulations? How do you maintain compliance?

3. **Has your business or any team member had previous experience with AI tools?**
   - *Structured options:* ___ Extensive experience / ___ Some experience (tried a few tools) / ___ Minimal (heard about it) / ___ None
   - *If yes:* What tools did you try, and what was the outcome (positive or negative)? What did you learn?

4. **How do you currently handle data privacy with your customers?**
   - Do you have a published privacy policy?
   - How do you obtain consent for data collection?
   - Can customers request their data be deleted (right to be forgotten)?

5. **Are there any reputational considerations around using AI in your business?**
   - Would your customers care if you used AI to handle their inquiries or personalize their experience?
   - Is there any brand sensitivity around automation (e.g., high-touch service business, luxury brand, healthcare)?

### What to Look For / Red Flags
- **Multiple regulations but no compliance program:** High-risk client — AI solutions must be architected for compliance from day one
- **No security basics (no 2FA, no password manager):** Foundational security gaps need addressing before AI deployment
- **Negative AI experience in the past:** Likely skepticism — validate their experience and differentiate your approach
- **High-touch businesses with automation concerns:** May need disclosure strategies, hybrid human/AI approaches
- **"We don't need to worry about that" attitude on compliance:** Significant liability risk

### Dynamic Follow-up Generation
*Use these prompts to generate additional questions based on client responses:*
- If the client mentions HIPAA: generate questions about BAAs (Business Associate Agreements), PHI handling, and covered entity status.
- If the client mentions GDPR: generate questions about data processing basis, cross-border transfers, DPO appointments.
- If the client has no privacy policy: generate questions about their willingness to create one and their understanding of data rights.
- If the client had a bad AI experience: generate questions about what specifically went wrong, who was involved, and what they wish had been different.

---

## SECTION 6 — Stakeholders & Change Readiness

**Purpose:** Identify who will be affected by the changes, who the decision-makers are, and assess the organizational capacity for change.

### Questions

1. **Who are the key decision-makers for technology and process changes in your business?**
   - List names, roles, and their stance on AI adoption (if known):
     - *Champion (excited):* __________
     - *Neutral (open to being convinced):* __________
     - *Skeptic (resistant or concerned):* __________
     - *Decision-maker (final approval):* __________

2. **Who in your business will be most directly affected by AI-driven changes?**
   - What are their roles?
   - How do you think they will react?
   - Do any of them have concerns about job security that we should address proactively?

3. **How has your business typically handled major changes in the past?**
   - *Structured options:* ___ Embraced new systems quickly / ___ Gradual adoption with support / ___ Resistant — reverted to old ways / ___ Mixed — depends on the change
   - *Follow-up:* What made past tech adoptions succeed or fail?

4. **How are decisions about technology typically made?**
   - Is it a solo decision by the owner, a team discussion, or consensus-driven?
   - Who needs to be convinced for implementation to succeed?

5. **If we identified an AI solution that would save 10 hours per week but required 2 weeks of adjustment, how would your team respond?**
   - *Scenario-based — gauges practical change readiness*

### What to Look For / Red Flags
- **All decision-making centralized in one person (especially the owner):** Single point of failure for adoption; if the owner loses interest, the initiative stalls
- **No identified champion:** Lack of internal advocacy makes sustained adoption harder
- **History of failed tech implementations:** Build trust through smaller, guaranteed wins first
- **Fear of job loss mentioned explicitly:** Must be addressed directly and transparently in the deployment plan
- **"My team won't like this" without willingness to manage that resistance:** Leadership gap that will undermine implementation

### Dynamic Follow-up Generation
*Use these prompts to generate additional questions based on client responses:*
- If the owner is the sole decision-maker: generate questions about their availability for implementation support and contingency plans if they're unavailable.
- If a skeptic is identified: generate questions about the source of their skepticism (previous bad experience? personality type? specific concern?).
- If past implementations failed: generate questions about what went wrong, who was involved, and what was learned.
- If the team is described as "not tech-savvy": generate questions about previous training approaches, learning styles, and support structures.

---

## INTERVIEWER NOTES & OBSERVATIONS

### Overall Impressions
- Client energy/enthusiasm level (1-5): ___
- Clarity of communication about their business (1-5): ___
- Realistic expectations about AI (1-5): ___
- Likelihood of successful engagement (1-5): ___

### Key Themes Identified
1. ________________________________________________________
2. ________________________________________________________
3. ________________________________________________________

### Immediate Red Flags
1. ________________________________________________________
2. ________________________________________________________
3. ________________________________________________________

### Dynamic Follow-up Questions Generated During This Session
1. ________________________________________________________
2. ________________________________________________________
3. ________________________________________________________
4. ________________________________________________________
5. ________________________________________________________

### Recommended Next Steps for the Client
1. ________________________________________________________
2. ________________________________________________________
3. ________________________________________________________

---

*Template Version: 1.0 — MIFECO Virtual Consulting Framework*
*Based on "AI That Works for Small Business" by Bob Mills*
