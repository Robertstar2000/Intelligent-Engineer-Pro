#!/usr/bin/env python3
"""
content-generator.py — MIFECO Content Generation Engine
Generates social media posts and blog posts from pipeline data.

Usage:
    python3 content-generator.py                    # Generate all content for qualified leads
    python3 content-generator.py --pipeline books    # Books-only
    python3 content-generator.py --social only       # Social only, no blog
    python3 content-generator.py --blog only         # Blog only
    python3 content-generator.py --report            # Show what would be generated

Output:
    data/generated-social-content.json
    data/generated-blog-posts.json
"""

import json
import os
import sys
import random
from datetime import datetime, timezone
from textwrap import wrap

# ─── Path Configuration ──────────────────────────────────────────────────────

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(WORKSPACE, "data")
SEQUENCES_DIR = os.path.join(WORKSPACE, "sequences")
OUTPUT_DIR = os.path.join(WORKSPACE, "data")

UNIFIED_PIPELINE_PATH = os.path.join(DATA_DIR, "unified-pipeline.json")
LEADS_REGISTRY_PATH = os.path.join(DATA_DIR, "leads-registry.json")
SOCIAL_CONTENT_BOOKS_PATH = os.path.join(DATA_DIR, "social-content-books.json")
NURTURE_SEQUENCES_PATH = os.path.join(SEQUENCES_DIR, "nurture-sequences.json")

SOCIAL_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "generated-social-content.json")
BLOG_OUTPUT_PATH = os.path.join(OUTPUT_DIR, "generated-blog-posts.json")

QUALIFIED_SCORE_THRESHOLD = 15

# ─── Data Loader ─────────────────────────────────────────────────────────────

def load_json(path, default=None):
    """Load a JSON file, returning default on error/missing."""
    if default is None:
        default = {}
    if not os.path.exists(path):
        print(f"  ⚠  Warning: {path} not found, using defaults")
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ⚠  Warning: Could not load {path}: {e}")
        return default


def load_all_data():
    """Load all input data sources into a dictionary."""
    print("📂 Loading pipeline data...")
    data = {
        "unified_pipeline": load_json(UNIFIED_PIPELINE_PATH, default=[]),
        "leads_registry": load_json(LEADS_REGISTRY_PATH, default={}),
        "social_content_books": load_json(SOCIAL_CONTENT_BOOKS_PATH, default=[]),
        "nurture_sequences": load_json(NURTURE_SEQUENCES_PATH, default=[]),
    }
    print(f"   ✓  Leads in pipeline: {len(data['unified_pipeline'])}")
    print(f"   ✓  Registry entries: {len(data.get('leads_registry', {}).get('pipelines', {}))}")
    print(f"   ✓  Existing book social posts: {len(data['social_content_books'])}")
    print(f"   ✓  Nurture sequences: {len(data['nurture_sequences'])}")
    return data


# ─── Pipeline Filtering ──────────────────────────────────────────────────────

def get_qualified_leads(data, pipeline_filter=None):
    """Filter leads by total_score >= 15 and optional pipeline filter."""
    leads = data["unified_pipeline"]
    if not isinstance(leads, list):
        print("  ⚠  Pipeline data is not a list")
        return []

    qualified = []
    for lead in leads:
        if not isinstance(lead, dict):
            continue
        if lead.get("total_score", 0) >= QUALIFIED_SCORE_THRESHOLD:
            if pipeline_filter and lead.get("pipeline") != pipeline_filter:
                continue
            qualified.append(lead)

    return qualified


def get_pipeline_stats(data, pipeline_filter=None):
    """Get statistics about the pipeline for report mode."""
    all_leads = data["unified_pipeline"]
    if not isinstance(all_leads, list):
        all_leads = []

    by_pipeline = {}
    for lead in all_leads:
        if not isinstance(lead, dict):
            continue
        pipe = lead.get("pipeline", "unknown")
        if pipeline_filter and pipe != pipeline_filter:
            continue
        by_pipeline.setdefault(pipe, {"total": 0, "qualified": 0, "avg_score": 0.0})
        by_pipeline[pipe]["total"] += 1
        by_pipeline[pipe]["avg_score"] = (
            (by_pipeline[pipe]["avg_score"] * (by_pipeline[pipe]["total"] - 1) + lead.get("total_score", 0))
            / by_pipeline[pipe]["total"]
        )
        if lead.get("total_score", 0) >= QUALIFIED_SCORE_THRESHOLD:
            by_pipeline[pipe]["qualified"] += 1

    return by_pipeline


# ─── Content Templates — Social Posts ────────────────────────────────────────

BOOK_LINKEDIN_TEMPLATES = [
    {
        "angle": "What if we never went back?",
        "template": (
            "What if you couldn't go home?\n\n"
            "Not because the door was locked. But because home was a planet you left behind "
            "and no ship could make the return journey.\n\n"
            "That's the premise of the No Blue Sky series — a five-book exploration of what "
            "happens when humanity permanently leaves Earth. No rescue missions. No return trips. "
            "Just the cold, beautiful reality of building a new world from scratch.\n\n"
            "Each generation born off-world faces a different question:\n"
            "• First Generation: What do we carry with us?\n"
            "• Moon Base One: What does it take to survive?\n"
            "• Second Generation: What do we owe our children?\n"
            "• Third Generation: What happens when Earth is just a story?\n"
            "• The Unwritten Future: What comes after?\n\n"
            "These aren't just science fiction questions. They're the questions every "
            "pioneer, every innovator, every builder has to answer.\n\n"
            "What would you carry with you if you couldn't come back?"
        ),
        "hashtags": ["#NoBlueSky", "#ScienceFiction", "#SpaceExploration", "#FutureOfHumanity", "#MIFECOBks"],
        "graphic": (
            "Cinematic book cover montage of five space-themed novels arranged in a "
            "V-formation against a starfield background, each cover glowing with a distinct "
            "color: warm gold, silver, deep blue, crimson, and cosmic purple, 16:9 aspect ratio"
        ),
    },
    {
        "angle": "Leadership lessons from space",
        "template": (
            "The most difficult leadership lesson I ever learned didn't come from a boardroom.\n\n"
            "It came from watching Apollo astronauts train for missions they might not survive.\n\n"
            "The difference between a good leader and a great one is the same as the difference "
            "between a good astronaut and a great one: they make decisions under uncertainty "
            "with incomplete information, and they take responsibility for the outcomes.\n\n"
            "In my work with {company_name}, I've seen this principle play out in real time. "
            "The leaders who succeed aren't the ones with perfect information. They're the ones "
            "who can make a call, adjust course, and keep the team moving forward.\n\n"
            "My book 'Tomorrow Is Still Open' tells the story of a career spent learning this lesson — "
            "from NASA to Silicon Valley to the frontiers of AI.\n\n"
            "What's the best leadership lesson you've learned outside the boardroom?"
        ),
        "hashtags": ["#Leadership", "#DecisionMaking", "#SpaceExploration", "#LessonsFromNASA", "#MIFECO"],
        "graphic": (
            "Split composition showing Apollo mission control (1960s) on the left and a modern "
            "startup war room on the right, connected by a timeline of innovation, warm vintage "
            "tone transitioning to modern blue, 16:9"
        ),
    },
    {
        "angle": "How curiosity changes everything",
        "template": (
            "Curiosity has a compound interest problem.\n\n"
            "Most people treat curiosity as a personality trait — either you're curious or you're not. "
            "But I've found it's more like a muscle. The more you exercise it, the stronger it gets. "
            "And over time, the returns compound dramatically.\n\n"
            "A curious person asks one more question. That leads to one more insight. "
            "That leads to one better decision. Every day. For decades.\n\n"
            "I started with questions about how boats float in my father's garage in Michigan. "
            "Those questions led to NASA. NASA led to Silicon Valley. Silicon Valley led to AI. "
            "And now they've led to five books about humanity's future in space.\n\n"
            "Tomorrow Is Still Open isn't just a memoir. It's a case study in what happens "
            "when you never stop asking 'why.'\n\n"
            "What question are you asking right now that might change everything?"
        ),
        "hashtags": ["#Curiosity", "#LifelongLearning", "#Innovation", "#STEM", "#PersonalGrowth"],
        "graphic": (
            "A winding path from a child's hand building a model boat to an adult hand typing "
            "on a holographic keyboard, surrounded by floating question marks that turn into "
            "lightbulbs, gradient from warm wood tones to cool tech blue, 16:9"
        ),
    },
]

CONSULTING_LINKEDIN_TEMPLATES = [
    {
        "angle": "AI isn't magic — it's math",
        "template": (
            "Here's what nobody tells you about AI adoption:\n\n"
            "The technology is the easy part.\n\n"
            "In my consulting work with {company_name} and dozens of other organizations, "
            "I've found that AI projects fail for three reasons — and none of them are technical:\n\n"
            "1. Fuzzy problem definition — teams buy AI tools before they understand what "
            "problem they're solving\n"
            "2. Cultural resistance — people fear AI will replace them, not augment them\n"
            "3. No feedback loop — models get deployed but nobody measures whether they're working\n\n"
            "The fix is simple but not easy: start with the business problem, not the technology. "
            "Involve your team from day one. Measure everything.\n\n"
            "90% of AI proof-of-concepts never make it to production. But when they do, the "
            "average ROI is 3.5x within the first year.\n\n"
            "The difference between success and failure isn't better algorithms. It's better preparation.\n\n"
            "What's the biggest barrier you've faced with AI adoption?"
        ),
        "hashtags": ["#AIAdoption", "#DigitalTransformation", "#AIStrategy", "#BusinessGrowth", "#MIFECOConsult"],
        "graphic": (
            "Data visualization showing three concentric rings labeled 'Problem Definition', "
            "'Cultural Readiness', 'Feedback Loops' with a glowing success metric in the center, "
            "modern business infographic style, blue and orange color scheme, 16:9"
        ),
    },
    {
        "angle": "The 4-phase AI framework",
        "template": (
            "After implementing AI systems across healthcare, finance, logistics, and aerospace, "
            "I've settled on a framework that works every time:\n\n"
            "Assess → Choose → Implement → Optimize\n\n"
            "Here's what that actually means:\n\n"
            "ASSESS: Spend two weeks auditing your operations. Which tasks are repetitive? "
            "Which decisions follow patterns? Where do your people spend time that robots could spend better?\n\n"
            "CHOOSE: Match the problems to the tools. Not every problem needs a $100k ML pipeline. "
            "Sometimes a simple rules-based automation solves 80% of the pain.\n\n"
            "IMPLEMENT: Work with your team, not around them. The best AI system in the world "
            "is worthless if nobody uses it.\n\n"
            "OPTIMIZE: Set up measurement from day one. What gets measured gets improved.\n\n"
            "This isn't theoretical. I've used this framework with {company_name} and seen "
            "40-60% reductions in manual processing time within a quarter.\n\n"
            "What phase is your organization in?"
        ),
        "hashtags": ["#AIImplementation", "#BusinessStrategy", "#OperationalExcellence", "#TechLeadership", "#MIFECO"],
        "graphic": (
            "Flow diagram showing four sequential phases: Assess (magnifying glass icon), "
            "Choose (target icon), Implement (gears icon), Optimize (chart going up icon), "
            "connected by glowing arrows, clean modern design with dark background, 16:9"
        ),
    },
    {
        "angle": "Why compliance is the killer AI use case",
        "template": (
            "If you're struggling to find your first AI use case, look at compliance.\n\n"
            "Why? Three reasons:\n\n"
            "1. It's high-volume — regulations generate thousands of pages of documentation "
            "that need review\n"
            "2. It's pattern-based — compliance checks follow rules, which is exactly what "
            "AI is good at\n"
            "3. It's measurable — you can quantify accuracy improvements and time savings immediately\n\n"
            "At {company_name}, we implemented AI-assisted compliance review that:\n"
            "• Reduced review time by 60%\n"
            "• Improved accuracy from 94% to 99.7%\n"
            "• Cut compliance costs by 35% in the first quarter\n\n"
            "Compliance might not be glamorous. But it's where AI delivers the fastest, "
            "most measurable ROI.\n\n"
            "What's your organization's compliance pain point?"
        ),
        "hashtags": ["#Compliance", "#AI", "#RegTech", "#OperationalEfficiency", "#RiskManagement"],
        "graphic": (
            "Dashboard-style infographic showing compliance metrics with AI overlay: before/after "
            "comparison bars, 60% reduction arrow, accuracy improvement gauge, professional "
            "dark theme with green accent colors, 16:9"
        ),
    },
]

SAAS_LINKEDIN_TEMPLATES = [
    {
        "angle": "Spreadsheets aren't project management",
        "template": (
            "Still managing projects in spreadsheets?\n\n"
            "I see this all the time with growing companies. You start with a simple tracker. "
            "Then you add a second sheet. Then a third. Then you're emailing 20 versions back and forth.\n\n"
            "The hidden cost isn't the software. It's the cognitive overhead.\n\n"
            "Every minute your team spends updating a spreadsheet is a minute they're not: "
            "• Solving client problems\n"
            "• Collaborating with teammates\n"
            "• Moving the business forward\n\n"
            "When we spoke with {company_name}, they were managing 40+ projects across "
            "spreadsheets and whiteboards. After switching to the Project Management Accelerator:\n"
            "• Project delivery times improved by 30%\n"
            "• Team reported 8+ hours saved per week\n"
            "• Client satisfaction scores increased by 22%\n\n"
            "Your tools should serve your team. Not the other way around.\n\n"
            "Are your tools working for you — or against you?"
        ),
        "hashtags": ["#ProjectManagement", "#Productivity", "#TeamCollaboration", "#SaaS", "#PMA"],
        "graphic": (
            "Split screen: left side shows chaotic spreadsheet grid with red error markers, "
            "right side shows clean kanban board with green checkmarks, transformation arrow "
            "in center, modern flat design, 16:9"
        ),
    },
    {
        "angle": "The real cost of tool sprawl",
        "template": (
            "The average company uses 112 SaaS applications.\n\n"
            "Most of them do the same thing.\n\n"
            "We see this pattern constantly with potential clients like {company_name}: "
            "• A project management tool (that nobody uses consistently)\n"
            "• A separate communication tool\n"
            "• A file sharing platform\n"
            "• A billing system\n"
            "• A time tracker\n"
            "• A client portal (or worse — email)\n\n"
            "The average employee switches between apps 1,100 times per day. "
            "Each switch costs 23 minutes to refocus.\n\n"
            "Do the math: that's 4+ hours of lost productivity per person per day.\n\n"
            "The solution isn't more tools. It's fewer, better-integrated ones.\n\n"
            "How many apps does your team use to manage a single project?"
        ),
        "hashtags": ["#ToolSprawl", "#Productivity", "#WorkflowEfficiency", "#SaaSOptimization", "#DigitalWorkspace"],
        "graphic": (
            "Collage of app icons (Slack, Asana, Google Drive, QuickBooks, etc.) swirling "
            "into a vortex, with a single unified dashboard emerging at the bottom, bold "
            "typography overlay reading '112 apps. One solution.', 16:9"
        ),
    },
    {
        "angle": "Transparency drives performance",
        "template": (
            "The single biggest productivity killer in organizations?\n\n"
            "Not laziness. Not incompetence.\n\n"
            "It's lack of visibility.\n\n"
            "When team members can't see how their work fits into the bigger picture, "
            "they disengage. When managers can't see what their teams are working on, "
            "they micromanage. When clients can't see project progress, they send anxious emails.\n\n"
            "The fix is radical transparency:\n"
            "• Real-time dashboards that everyone can see\n"
            "• Automated status updates that replace status meetings\n"
            "• Client portals that give stakeholders visibility without adding overhead\n\n"
            "{company_name} implemented this approach and eliminated their weekly "
            "status meetings entirely — saving 6 hours per week for a team of 20.\n\n"
            "What's one thing you could make visible today that would change everything?"
        ),
        "hashtags": ["#Transparency", "#TeamProductivity", "#ProjectManagement", "#RemoteWork", "#Leadership"],
        "graphic": (
            "Glass-walled office metaphor showing transparent project boards visible to all, "
            "data streams showing real-time progress, warm professional lighting emphasizing "
            "clarity and openness, 16:9"
        ),
    },
]

X_BOOK_TEMPLATES = [
    "Five books. One universe. No way home.\n\nThe No Blue Sky series — complete and waiting for you.",
    "Some questions can't be answered from Earth.\n\nThat's why the No Blue Sky series starts with leaving it behind.",
    "We spend our whole lives looking up.\n\nWhat happens when we finally go?",
    "The Moon doesn't belong to anyone.\n\nYet.\n\nWhat happens when Earth's nations start claiming territory in space?",
    "My grandfather built boats in a garage.\n\nI build AI systems.\n\nSame curiosity. Different century.",
    "You don't need to go to space to think like an explorer.\n\nYou just need to ask the right questions.",
    "The best stories aren't about the destination.\n\nThey're about who you become on the way.",
    "Everything I know about innovation I learned in my father's garage.\n\nThe tools change. The mindset doesn't.",
]

X_CONSULTING_TEMPLATES = [
    "90% of AI proofs-of-concept never make it to production.\n\nThe 10% that do? 3.5x average ROI.\n\nThe difference isn't technology. It's preparation.",
    "AI projects fail for 3 reasons:\n\n1. Fuzzy problem definition\n2. Cultural resistance\n3. No feedback loops\n\nNone of them are technical.",
    "You don't need a $100k ML pipeline.\n\nYou need someone who knows which problems AI can actually solve. Start there.",
    "The best AI system in the world is worthless if nobody uses it.\n\nImplementation = 80% of the work. Technology = 20%.",
    "Compliance isn't sexy. But it's where AI delivers the fastest ROI.\n\n60% faster reviews. 99.7% accuracy. 35% cost reduction.",
    "Don't automate everything. Automate the things your people hate doing.\n\nThat's where the real ROI lives.",
    "Every minute your team spends updating a spreadsheet is a minute they're not serving clients.\n\nThe hidden cost of bad tools isn't the subscription fee.",
    "The 4-phase AI framework:\n\nAssess → Choose → Implement → Optimize\n\nWorks every time. Across every industry.",
]

X_SAAS_TEMPLATES = [
    "The average employee switches between apps 1,100 times per day.\n\nEach switch costs 23 minutes to refocus.\n\nThat's 4+ hours lost per person per day.",
    "Your team doesn't need more tools.\n\nThey need fewer, better-integrated ones.",
    "Status meetings are a tax on productivity.\n\nReplace them with dashboards and save 6 hours/week.",
    "Spreadsheets are not project management tools.\n\nThey're just really good at hiding how chaotic your process is.",
    "The best thing you can do for your team's productivity: make everything visible.\n\nNo more searching. No more guessing. No more status emails.",
    "If you're still emailing status reports in 2026, you're not managing projects.\n\nYou're managing anxiety.",
    "Project management isn't about tracking tasks.\n\nIt's about giving people the clarity they need to do their best work.",
    "Your clients shouldn't have to ask for updates.\n\nGive them a portal and watch your email volume drop by 50%.",
]


def get_company_name(lead):
    """Safely extract company name from a lead."""
    enrichment = lead.get("enrichment", {})
    if isinstance(enrichment, dict):
        return enrichment.get("company_name", "your organization")
    return "your organization"


def get_contact_name(lead):
    """Safely extract contact name from a lead."""
    enrichment = lead.get("enrichment", {})
    if isinstance(enrichment, dict):
        return enrichment.get("contact_name", "there")
    return "there"


def get_industry(lead):
    """Safely extract industry from a lead."""
    enrichment = lead.get("enrichment", {})
    if isinstance(enrichment, dict):
        return enrichment.get("industry", "your industry")
    return "your industry"


def generate_linkedin_post(lead, existing_posts):
    """Generate a LinkedIn post for a given lead based on pipeline."""
    pipeline = lead.get("pipeline", "books")
    company = get_company_name(lead)
    contact = get_contact_name(lead)
    industry = get_industry(lead)
    lead_id = lead.get("lead_id", "unknown")

    if pipeline == "books":
        templates = BOOK_LINKEDIN_TEMPLATES
        # Add book-specific context
        book_titles = [
            "No Blue Sky series",
            "Tomorrow Is Still Open",
            "AI That Works for Small Business",
            "First Generation",
            "Second Generation",
        ]
        book_title = random.choice(book_titles)
        templates[0]["template"] = templates[0]["template"].replace(
            "{company_name}", company
        ) if "{company_name}" in templates[0]["template"] else templates[0]["template"]
        templates[1]["template"] = templates[1]["template"].replace(
            "{company_name}", company
        ) if "{company_name}" in templates[1]["template"] else templates[1]["template"]
        templates[2]["template"] = templates[2]["template"].replace(
            "{company_name}", company
        ) if "{company_name}" in templates[2]["template"] else templates[2]["template"]

    elif pipeline == "consulting":
        templates = CONSULTING_LINKEDIN_TEMPLATES
        for t in templates:
            t["template"] = t["template"].replace("{company_name}", company)
            t["template"] = t["template"].replace("{industry}", industry)

    elif pipeline == "saas":
        templates = SAAS_LINKEDIN_TEMPLATES
        for t in templates:
            t["template"] = t["template"].replace("{company_name}", company)

    else:
        # Fallback: use books templates
        templates = BOOK_LINKEDIN_TEMPLATES
        for t in templates:
            t["template"] = t["template"].replace("{company_name}", company)

    template = random.choice(templates)
    copy = template["template"]
    hashtags = template["hashtags"]
    graphic = template["graphic"]

    # Ensure hashtags are proper format
    hashtag_str = " ".join(hashtags)

    # Build full copy with hashtags
    full_copy = copy + "\n\n" + hashtag_str

    return {
        "platform": "linkedin",
        "target_audience": "Professional network — industry peers, potential clients, partners",
        "copy": full_copy,
        "hashtags": hashtags,
        "graphic_prompt": graphic,
        "linked_lead_id": lead_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_x_post(lead):
    """Generate an X/Twitter post for a given lead based on pipeline."""
    pipeline = lead.get("pipeline", "books")
    lead_id = lead.get("lead_id", "unknown")
    company = get_company_name(lead)

    if pipeline == "books":
        templates = X_BOOK_TEMPLATES
        hashtags = ["#NoBlueSky", "#SciFi", "#Books"]
        graphic = (
            "Minimalist book-inspired graphic with celestial elements, "
            "stark typography on deep space background, 1:1 square format"
        )
    elif pipeline == "consulting":
        templates = X_CONSULTING_TEMPLATES
        hashtags = ["#AI", "#Business", "#Consulting"]
        graphic = (
            "Data-focused graphic with key statistic prominently displayed, "
            "professional blue and orange color scheme, clean typography, 1:1 square format"
        )
    elif pipeline == "saas":
        templates = X_SAAS_TEMPLATES
        hashtags = ["#ProjectManagement", "#Productivity", "#SaaS"]
        graphic = (
            "Productivity-focused infographic showing time savings metric, "
            "clean modern design with green accent, 1:1 square format"
        )
    else:
        templates = X_BOOK_TEMPLATES
        hashtags = ["#Books", "#Innovation"]
        graphic = (
            "Inspirational typography on gradient background, 1:1 square format"
        )

    # Pick a template
    copy = random.choice(templates)

    # Truncate for X/Twitter (280 chars)
    hashtag_str = " ".join(hashtags)
    full_text = copy + "\n\n" + hashtag_str
    if len(full_text) > 280:
        # Truncate copy portion to fit with hashtags
        max_copy_len = 280 - len(hashtag_str) - 3  # 3 for newline separators
        if max_copy_len > 20:
            copy = copy[:max_copy_len].rsplit(".", 1)[0] + "."
        else:
            copy = copy[:250]
        full_text = copy + "\n\n" + hashtag_str
        if len(full_text) > 280:
            full_text = full_text[:277] + "..."

    return {
        "platform": "x",
        "target_audience": "General public, genre fans, industry professionals",
        "copy": full_text,
        "hashtags": hashtags,
        "graphic_prompt": graphic,
        "linked_lead_id": lead_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ─── Blog Post Generation ───────────────────────────────────────────────────

BLOG_THEMES = {
    "ai_tech": {
        "tagline": "AI/tech consulting theme",
        "title_options": [
            "AI in {industry}: A Practical Guide to Implementation",
            "Why 90% of AI Projects Fail (And How to Be in the 10%)",
            "The 4-Phase Framework for AI Transformation",
            "From Pilot to Production: Scaling AI in Your Organization",
        ],
        "subtopics": [
            "assessing organizational readiness for AI",
            "building the business case for AI investment",
            "overcoming cultural resistance to AI adoption",
            "measuring ROI from AI initiatives",
            "AI governance and risk management frameworks",
            "case studies from {industry}",
        ],
        "category": "AI & Technology",
        "tags": ["AI", "Digital Transformation", "Technology Strategy", "Machine Learning"],
    },
    "saas_pm": {
        "tagline": "Project management SaaS theme",
        "title_options": [
            "The Hidden Cost of Tool Sprawl: Why Less Is More",
            "10 Signs Your Team Has Outgrown Spreadsheet Management",
            "How to Choose the Right Project Management Software",
            "Radical Transparency: The Productivity Hack That Actually Works",
        ],
        "subtopics": [
            "measuring productivity losses from tool fragmentation",
            "evaluating project management software features",
            "implementing cross-team visibility and accountability",
            "automating workflows to reduce manual overhead",
            "client portal best practices for service businesses",
            "building a productivity stack that scales",
        ],
        "category": "Productivity & SaaS",
        "tags": ["Project Management", "Productivity", "SaaS", "Workflow Automation"],
    },
    "books_space": {
        "tagline": "Book/space theme",
        "title_options": [
            "Why We Look Up: The Enduring Allure of Space Exploration",
            "From Apollo to AI: How Space Exploration Shaped Modern Technology",
            "Building Worlds: The Art and Science of Science Fiction Writing",
            "The Questions We Carry: What Leaving Earth Teaches Us About Ourselves",
        ],
        "subtopics": [
            "the history of space exploration and its impact on technology",
            "how science fiction inspires real-world innovation",
            "the psychology of exploration and human curiosity",
            "building believable worlds in science fiction",
            "the future of space colonization and governance",
            "what space exploration teaches us about leadership",
        ],
        "category": "Books & Space",
        "tags": ["Science Fiction", "Space Exploration", "Writing", "Innovation", "Books"],
    },
}


def generate_blog_post(theme_key, pipeline_data=None):
    """Generate a single blog post based on theme and optional pipeline data."""
    theme = BLOG_THEMES.get(theme_key)
    if not theme:
        return None

    # Use pipeline data to personalize
    industries = []
    leads_scores = []
    if pipeline_data:
        for lead in pipeline_data:
            enrichment = lead.get("enrichment", {})
            if isinstance(enrichment, dict):
                ind = enrichment.get("industry", "")
                if ind:
                    industries.append(ind)
                leads_scores.append(lead.get("total_score", 0))

    industry_focus = industries[0] if industries else "modern organizations"
    avg_score = sum(leads_scores) / max(len(leads_scores), 1)

    # Select title
    title_template = random.choice(theme["title_options"])
    title = title_template.replace("{industry}", industry_focus)

    # Generate slug
    slug = title.lower()
    slug = slug.replace(":", "")
    slug = slug.replace("'", "")
    slug = "".join(c if c.isalnum() or c == " " else "" for c in slug)
    slug = "-".join(slug.split())
    slug = slug[:80].rstrip("-")

    # Generate excerpt
    excerpt = (
        f"Explore how {industry_focus} can leverage {theme['tagline'].lower()} "
        f"to drive measurable results. This comprehensive guide covers best practices, "
        f"real-world case studies, and actionable strategies."
    )[:200]

    # Generate content (800-1500 words)
    content = generate_blog_html(title, theme, industry_focus, theme_key)

    # Generate featured image prompt
    image_prompts = {
        "ai_tech": (
            "Professional technology workspace with holographic AI interface, "
            "flowing data streams in blue and orange, modern office background, "
            "cinematic lighting, 16:9 aspect ratio, photorealistic"
        ),
        "saas_pm": (
            "Clean modern dashboard display on multiple screens, team collaboration "
            "visualization, kanban boards and analytics charts, professional office "
            "environment, bright professional lighting, 16:9 aspect ratio"
        ),
        "books_space": (
            "Cinematic view of Earth from space with bookshelf silhouette in foreground, "
            "Earth's atmosphere glowing blue, stars visible, contemplative mood, "
            "16:9 aspect ratio, photorealistic"
        ),
    }

    featured_image_prompt = image_prompts.get(
        theme_key,
        "Professional business environment with technology elements, 16:9 aspect ratio"
    )

    # Generate infographic prompt
    infographic_prompts = {
        "ai_tech": (
            "Flow chart showing AI implementation journey: Assess → Choose → Implement → Optimize, "
            "with key metrics at each stage, modern infographic style, dark background with "
            "accent lighting, 16:9 aspect ratio"
        ),
        "saas_pm": (
            "Comparison infographic: Spreadsheet vs Modern PM tool, side-by-side metrics "
            "showing time savings, error reduction, and team satisfaction, clean data "
            "visualization style, 16:9 aspect ratio"
        ),
        "books_space": (
            "Timeline infographic from 1969 Moon landing to 2026, highlighting key milestones "
            "in space exploration and technology, vintage and modern aesthetic blend, "
            "16:9 aspect ratio"
        ),
    }

    return {
        "title": title,
        "slug": slug,
        "excerpt": excerpt,
        "content": content,
        "tags": theme["tags"],
        "category": theme["category"],
        "seo_keywords": [industry_focus.lower()] + theme["tags"],
        "featured_image_prompt": featured_image_prompt,
        "infographic_prompt": infographic_prompts.get(theme_key, featured_image_prompt),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "word_count": len(content.split()),
    }


def generate_blog_html(title, theme, industry_focus, theme_key):
    """Generate full HTML content for a blog post (800-1500 words)."""
    sections = []

    # Introduction
    intro_templates = {
        "ai_tech": (
            f"<p>The promise of artificial intelligence is tantalizing: smarter operations, "
            f"faster decisions, lower costs, happier customers. But for most organizations, "
            f"the reality is different. AI projects stall. Pilots never scale. The promised "
            f"ROI never materializes.</p>"
            f"<p>This isn't because AI doesn't work. It's because most organizations approach "
            f"AI wrong. They start with the technology instead of the problem. They invest "
            f"in tools before they understand their own processes. They treat AI as a "
            f"science project instead of a business transformation.</p>"
            f"<p>In this guide, we'll walk through a proven framework for AI adoption that "
            f"has worked across healthcare, finance, logistics, and manufacturing. Whether "
            f"you're just starting your AI journey or looking to scale existing initiatives, "
            f"these principles will help you avoid the common pitfalls and build AI systems "
            f"that actually deliver value.</p>"
        ),
        "saas_pm": (
            f"<p>If your team is still managing projects in spreadsheets, you're not alone. "
            f"Thousands of growing organizations start this way — a simple tracker here, a "
            f"status update there, a shared folder for documents. It works until it doesn't.</p>"
            f"<p>The problem isn't that spreadsheets are bad. It's that they don't scale. "
            f"What starts as elegant simplicity becomes chaotic complexity as your team "
            f"grows, your project count increases, and your clients expect more transparency.</p>"
            f"<p>This guide will help you evaluate whether it's time to upgrade your project "
            f"management approach, what to look for in a solution, and how to make the "
            f"transition without disrupting your operations.</p>"
        ),
        "books_space": (
            f"<p>Why do we look up? It's a question that has fascinated philosophers, "
            f"scientists, and storytellers for millennia. From the first cave paintings "
            f"of celestial bodies to the latest Mars rover images, humanity has always "
            f"been drawn to the stars.</p>"
            f"<p>But the answer has changed. We no longer look up and wonder what's "
            f"there — we know. We've sent probes to every planet in the solar system. "
            f"We've walked on the Moon. We've built space stations that orbit our "
            f"planet continuously for decades.</p>"
            f"<p>Now the question has shifted from 'what's there?' to 'what will we "
            f"build there?' And that changes everything.</p>"
        ),
    }
    sections.append(intro_templates.get(theme_key, "<p>Introduction.</p>"))

    # Body section 1 — The Problem/Context
    body1 = {
        "ai_tech": (
            f"<h2>The AI Adoption Gap</h2>"
            f"<p>According to recent industry research, 90% of AI proofs-of-concept never "
            f"make it to production. That's a staggering failure rate — and it's not getting "
            f"better. The primary causes are consistent across industries:</p>"
            f"<ul>"
            f"<li><strong>Fuzzy problem definition:</strong> Teams invest in AI before they "
            f"clearly understand what problem they're solving.</li>"
            f"<li><strong>Cultural resistance:</strong> Employees fear AI will replace them, "
            f"leading to passive resistance or active sabotage.</li>"
            f"<li><strong>No feedback loops:</strong> AI systems are deployed without clear "
            f"metrics for success, making it impossible to optimize or justify the investment.</li>"
            f"</ul>"
            f"<p>For {industry_focus}, these challenges are compounded by industry-specific "
            f"regulations, legacy systems, and talent shortages. But they're not insurmountable.</p>"
        ),
        "saas_pm": (
            f"<h2>The Real Cost of Tool Sprawl</h2>"
            f"<p>Here's a number that should stop you in your tracks: the average employee "
            f"switches between applications 1,100 times per day. Each switch costs approximately "
            f"23 minutes to regain full focus. That's over 4 hours of lost productivity per "
            f"person, per day.</p>"
            f"<p>For {industry_focus}, where teams are already stretched thin managing "
            f"multiple projects and client expectations, this hidden tax on productivity "
            f"is devastating. It shows up in missed deadlines, burned-out team members, "
            f"and frustrated clients.</p>"
            f"<p>The solution isn't more tools. It's fewer, better-integrated ones that "
            f"reduce cognitive load instead of adding to it.</p>"
        ),
        "books_space": (
            f"<h2>The Power of the Frontier</h2>"
            f"<p>Every frontier — whether physical or intellectual — changes the people "
            f"who cross it. The Apollo astronauts who went to the Moon came back with a "
            f"new perspective on Earth. The settlers who crossed the American West "
            f"developed new forms of governance. The inventors of the internet created "
            f"a new way of being human.</p>"
            f"<p>Space is the next frontier, and it will change us just as profoundly. "
            f"But here's what's different this time: we can imagine the future before we build it. "
            f"Through science fiction, we can explore the possibilities, wrestle with the "
            f"ethical dilemmas, and decide what kind of future we want to create.</p>"
            f"<p>This is why stories matter. They're not just entertainment — they're "
            f"rehearsals for reality.</p>"
        ),
    }
    sections.append(body1.get(theme_key, "<h2>Body</h2><p>Content.</p>"))

    # Body section 2 — The Solution/Methodology
    body2 = {
        "ai_tech": (
            f"<h2>A Proven Framework: Assess → Choose → Implement → Optimize</h2>"
            f"<p>After implementing AI systems across dozens of organizations, we've "
            f"settled on a four-phase framework that consistently delivers results:</p>"
            f"<h3>Phase 1: Assess</h3>"
            f"<p>Spend two to four weeks auditing your operations. Which tasks are truly "
            f"repetitive? Which decisions follow clear patterns? Where do your highest-value "
            f"employees spend time on low-value activities? This phase requires honest, "
            f"unflinching observation of how work actually gets done — not how you think "
            f"it gets done.</p>"
            f"<h3>Phase 2: Choose</h3>"
            f"<p>Match problems to solutions. Not every problem needs a custom machine "
            f"learning pipeline. Sometimes a simple rules-based automation, an off-the-shelf "
            f"API, or even a well-configured workflow tool solves 80% of the pain. Save "
            f"your big guns for the problems that genuinely require them.</p>"
            f"<h3>Phase 3: Implement</h3>"
            f"<p>Work with your team, not around them. The best AI system in the world is "
            f"worthless if nobody uses it. Involve end users from day one. Train them. "
            f"Listen to their feedback. Iterate based on how the system performs in the "
            f"real world, not in a test environment.</p>"
            f"<h3>Phase 4: Optimize</h3>"
            f"<p>Set up measurement from day one. What gets measured gets improved. "
            f"Track adoption rates, time savings, error reduction, and user satisfaction. "
            f"Use this data to continuously refine your AI systems and build the case "
            f"for further investment.</p>"
        ),
        "saas_pm": (
            f"<h2>What to Look for in a Project Management Solution</h2>"
            f"<p>When evaluating project management software for {industry_focus}, "
            f"here are the key features that matter most:</p>"
            f"<ol>"
            f"<li><strong>Real-time visibility:</strong> Dashboards that show project "
            f"status, resource allocation, and bottlenecks at a glance.</li>"
            f"<li><strong>Automation engine:</strong> The ability to automate repetitive "
            f"tasks like status updates, task assignments, and deadline reminders.</li>"
            f"<li><strong>Client portal:</strong> Giving clients visibility into project "
            f"progress without adding overhead to your team.</li>"
            f"<li><strong>Integration capabilities:</strong> The tool should connect with "
            f"your existing stack, not replace it.</li>"
            f"<li><strong>Scalability:</strong> Can it handle 10 projects today and 100 "
            f"projects next year without a complete overhaul?</li>"
            f"</ol>"
            f"<p>But features aren't everything. The most important factor is adoption. "
            f"A tool with 80% of the features that your team actually uses is infinitely "
            f"better than a tool with 100% of the features that nobody touches.</p>"
        ),
        "books_space": (
            f"<h2>Building Worlds That Matter</h2>"
            f"<p>Writing science fiction is an exercise in world-building. But the best "
            f"science fiction doesn't just build worlds — it builds questions. The lunar "
            f"colonies, Martian settlements, and generational ships aren't just settings. "
            f"They're pressure chambers that force characters to confront fundamental "
            f"questions about identity, belonging, and what it means to be human.</p>"
            f"<p>When I wrote the No Blue Sky series, I started with a simple question: "
            f"what happens when you can't go home? Not because the door is locked, but "
            f"because home is a planet you left behind and no ship can make the return journey. "
            f"That question led to others. What do we carry with us when we leave? "
            f"What do we owe the children born off-world? What happens when Earth "
            f"is just a story you tell your grandchildren?</p>"
            f"<p>These aren't just science fiction questions. They're the questions "
            f"every pioneer has to answer — whether they're exploring space, starting "
            f"a company, or building a new life.</p>"
        ),
    }
    sections.append(body2.get(theme_key, "<h2>Methodology</h2><p>Details.</p>"))

    # Body section 3 — Case studies / Real-world application
    body3 = {
        "ai_tech": (
            f"<h2>Real Results Across Industries</h2>"
            f"<p>Consider {industry_focus}. Organizations in this space face unique "
            f"challenges — regulatory pressure, complex workflows, and the need for "
            f"high reliability. Yet they're also where AI delivers some of the most "
            f"impressive results.</p>"
            f"<p>One manufacturer implemented AI-powered predictive maintenance and "
            f"reduced unplanned downtime by 45% in the first six months. A financial "
            f"services firm automated 70% of their compliance review process, cutting "
            f"review time from days to hours while improving accuracy. A logistics "
            f"company used AI route optimization to reduce fuel costs by 18% and "
            f"improve on-time delivery from 89% to 97%.</p>"
            f"<p>These aren't outliers. They're the result of following a systematic "
            f"approach to AI adoption — starting with the problem, involving the team, "
            f"and measuring results relentlessly.</p>"
        ),
        "saas_pm": (
            f"<h2>The Transformation in Practice</h2>"
            f"<p>Let's look at what happens when {industry_focus} makes the switch "
            f"from spreadsheets to a proper project management platform.</p>"
            f"<p>Before the switch: A team of 20 manages 30+ projects across six "
            f"spreadsheets, three shared drives, and countless email threads. Status "
            f"meetings consume 6 hours per week. Client updates require manual compilation "
            f"that takes another 4 hours. Deadline misses are discovered too late to fix. "
            f"Team morale suffers from the constant context-switching.</p>"
            f"<p>After the switch: The same team manages 30+ projects from a single "
            f"dashboard. Automations handle status updates, task assignments, and client "
            f"notifications. Status meetings are eliminated — replaced by real-time dashboards "
            f"that everyone can access. Client satisfaction scores improve by 22%. "
            f"Teams report saving 8+ hours per week on administrative overhead.</p>"
            f"<p>This isn't hypothetical. This is what happens when you give teams "
            f"tools that work the way they do — not the way software vendors think they should.</p>"
        ),
        "books_space": (
            f"<h2>From Story to Strategy: What Space Teaches Business</h2>"
            f"<p>Here's something surprising: the principles that make great science "
            f"fiction also make great business strategy.</p>"
            f"<p>Consider the Apollo program. It wasn't just the greatest engineering "
            f"achievement in human history. It was the greatest project management "
            f"achievement. Thousands of contractors. Millions of components. A deadline "
            f"that couldn't slip. And a goal that seemed impossible until it wasn't.</p>"
            f"<p>The lessons from Apollo apply directly to modern business: break big "
            f"problems into small ones, test everything, embrace failure as data, and "
            f"keep the mission front and center even when the details get overwhelming.</p>"
            f"<p>In my books, I explore what happens when you apply these principles "
            f"to challenges beyond Earth. But the same principles work for any ambitious "
            f"endeavor — whether you're building a lunar colony or a growing business.</p>"
        ),
    }
    sections.append(body3.get(theme_key, "<h2>Applications</h2><p>Examples.</p>"))

    # Conclusion
    conclusion = {
        "ai_tech": (
            f"<h2>Getting Started</h2>"
            f"<p>The most important step is the first one. Don't wait for the perfect "
            f"plan, the perfect team, or the perfect technology. Start with a single "
            f"problem. Apply the Assess → Choose → Implement → Optimize framework. "
            f"Measure everything. Learn from every failure. Iterate relentlessly.</p>"
            f"<p>AI isn't magic. It's just math, done at scale, with good data. "
            f"And when you approach it systematically, it delivers results that "
            f"look like magic to everyone else.</p>"
            f"<p><em>Need help getting started? MIFECO Consulting specializes in "
            f"helping organizations navigate the AI adoption journey. Contact us for "
            f"a free AI Opportunity Assessment.</em></p>"
        ),
        "saas_pm": (
            f"<h2>Making the Switch</h2>"
            f"<p>Transitioning from spreadsheets to a proper project management platform "
            f"doesn't have to be painful. The key is to start small, involve your team, "
            f"and focus on the workflows that matter most.</p>"
            f"<p>Choose one team or one project type to pilot. Set clear success metrics. "
            f"Give your team time to adapt. And remember: the goal isn't perfect software "
            f"adoption. It's better project outcomes.</p>"
            f"<p><em>Ready to see what a proper project management platform can do for "
            f"your team? Schedule a demo of the Project Management Accelerator and see "
            f"it in action.</em></p>"
        ),
        "books_space": (
            f"<h2>The Story Continues</h2>"
            f"<p>Whether we're exploring space, building AI systems, or writing books, "
            f"the underlying drive is the same: the urge to push beyond the known, "
            f"to ask what's next, to leave something meaningful behind.</p>"
            f"<p>The No Blue Sky series is my contribution to that tradition — "
            f"five books that ask what happens when we take the next big step. "
            f"And the next one. And the one after that.</p>"
            f"<p>Because the future isn't something that happens to us. It's something "
            f"we build. Every day. With every choice we make.</p>"
            f"<p><em>Explore the No Blue Sky series and discover what happens when "
            f"humanity leaves Earth for good.</em></p>"
        ),
    }
    sections.append(conclusion.get(theme_key, "<h2>Conclusion</h2><p>Final thoughts.</p>"))

    # Assemble into full HTML
    full_html = f"""<article class="blog-post">
<header>
<h1>{title}</h1>
<div class="meta">
<time datetime="{datetime.now(timezone.utc).strftime('%Y-%m-%d')}">{datetime.now(timezone.utc).strftime('%B %d, %Y')}</time>
<span class="category">{theme['category']}</span>
</div>
</header>

<section class="content">
{''.join(sections)}
</section>

<footer class="tags">
<p>Tags: {', '.join(f'<a href="/tag/{t.lower().replace(chr(32), chr(45))}">{t}</a>' for t in theme['tags'])}</p>
</footer>
</article>"""

    # Ensure word count is in range
    word_count = len(full_html.split())
    if word_count < 800:
        # Add more content if needed
        extra_text = (
            f"<p>Beyond the core strategies discussed above, it's worth considering "
            f"the broader implications for {industry_focus}. As technology continues to "
            f"evolve at an accelerating pace, organizations that invest in the right "
            f"foundations today will be best positioned to capitalize on tomorrow's "
            f"opportunities. The key is not to predict the future, but to build systems "
            f"— whether technological, organizational, or cultural — that are resilient "
            f"enough to adapt to whatever the future brings.</p>"
            f"<p>This is the philosophy that guides everything we do at MIFECO. It's "
            f"why our consulting engagements focus on building capabilities, not just "
            f"delivering solutions. It's why our books explore not just what's possible, "
            f"but what's meaningful. And it's why our software is designed to amplify "
            f"human potential rather than replace it.</p>"
            f"<p>The future is not something we predict. It's something we build. "
            f"And we build it one decision at a time.</p>"
        )
        full_html = full_html.replace("</article>", extra_text + "\n</article>")

    return full_html


# ─── Output Writers ──────────────────────────────────────────────────────────

def write_json_output(path, data):
    """Write data to a JSON file with pretty formatting."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"   ✓  Written: {path}")


def create_output_header(description, stats=None):
    """Create a standard output header with timestamp and stats."""
    header = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "content-generator.py",
        "version": "1.0.0",
        "description": description,
    }
    if stats:
        header["stats"] = stats
    return header


# ─── Main Generation Logic ───────────────────────────────────────────────────

def generate_social_content(data, pipeline_filter=None):
    """Generate social media posts for qualified leads."""
    print("\n📱 Generating social media content...")
    qualified = get_qualified_leads(data, pipeline_filter)
    print(f"   Found {len(qualified)} qualified leads (score >= {QUALIFIED_SCORE_THRESHOLD})")

    if not qualified:
        print("   ⚠  No qualified leads to generate content for.")
        return []

    existing_posts = data.get("social_content_books", [])

    generated_posts = []
    for lead in qualified:
        lead_id = lead.get("lead_id", "unknown")
        pipeline = lead.get("pipeline", "unknown")
        company = get_company_name(lead)
        contact = get_contact_name(lead)
        score = lead.get("total_score", 0)

        print(f"   🎯 {lead_id} | {company} ({pipeline}, score: {score})")

        # Generate LinkedIn post
        linkedin_post = generate_linkedin_post(lead, existing_posts)
        generated_posts.append(linkedin_post)

        # Generate X/Twitter post
        x_post = generate_x_post(lead)
        generated_posts.append(x_post)

    print(f"   ✅ Generated {len(generated_posts)} social posts for {len(qualified)} leads")
    return generated_posts


def generate_blog_content(data, pipeline_filter=None):
    """Generate blog posts based on pipeline themes."""
    print("\n📝 Generating blog posts...")

    # Get pipeline data for personalization
    pipeline_data = data["unified_pipeline"]
    if pipeline_filter:
        pipeline_data = [l for l in pipeline_data if isinstance(l, dict) and l.get("pipeline") == pipeline_filter]

    blog_posts = []

    # Always generate 3 blog posts covering all themes
    themes = ["ai_tech", "saas_pm", "books_space"]
    filtered_themes = themes

    if pipeline_filter == "books":
        filtered_themes = ["books_space", "ai_tech"]
    elif pipeline_filter == "consulting":
        filtered_themes = ["ai_tech", "saas_pm"]
    elif pipeline_filter == "saas":
        filtered_themes = ["saas_pm", "ai_tech"]

    for theme_key in filtered_themes:
        print(f"   📖 Generating: {BLOG_THEMES[theme_key]['tagline']}")
        post = generate_blog_post(theme_key, pipeline_data)
        if post:
            blog_posts.append(post)
            print(f"      ✓ {post['title']} ({post['word_count']} words)")

    print(f"   ✅ Generated {len(blog_posts)} blog posts")
    return blog_posts


def generate_report(data, pipeline_filter=None):
    """Generate a report of what would be generated."""
    print("\n📊 GENERATION REPORT")
    print("=" * 60)

    stats = get_pipeline_stats(data, pipeline_filter)
    if pipeline_filter:
        print(f"\n  Pipeline Filter: {pipeline_filter}")

    print(f"\n  Qualified Threshold: {QUALIFIED_SCORE_THRESHOLD}")
    print(f"\n  Pipeline Breakdown:")

    total_qualified = 0
    for pipe, s in sorted(stats.items()):
        qualified_count = s["qualified"]
        total_qualified += qualified_count
        print(f"    {pipe:20s}  Total: {s['total']:2d}  Qualified: {qualified_count:2d}  Avg Score: {s['avg_score']:.1f}")

    print(f"\n  {'─' * 50}")
    print(f"  Total Qualified: {total_qualified}")
    print(f"  Social Posts to Generate: {total_qualified * 2} ({total_qualified} LinkedIn + {total_qualified} X/Twitter)")

    themes_to_generate = ["AI/Tech Consulting", "PM SaaS", "Books/Space"]
    if pipeline_filter == "books":
        themes_to_generate = ["Books/Space", "AI/Tech Consulting"]
    elif pipeline_filter == "consulting":
        themes_to_generate = ["AI/Tech Consulting", "PM SaaS"]
    elif pipeline_filter == "saas":
        themes_to_generate = ["PM SaaS", "AI/Tech Consulting"]

    print(f"  Blog Posts to Generate: {len(themes_to_generate)}")
    for t in themes_to_generate:
        print(f"    - {t}")

    print(f"\n  Output Files:")
    print(f"    {SOCIAL_OUTPUT_PATH}")
    print(f"    {BLOG_OUTPUT_PATH}")
    print(f"\n  {'=' * 60}")

    return total_qualified


# ─── CLI Entry Point ─────────────────────────────────────────────────────────

def parse_args():
    """Parse command-line arguments."""
    args = {
        "pipeline": None,
        "social_only": False,
        "blog_only": False,
        "report": False,
    }

    for arg in sys.argv[1:]:
        if arg.startswith("--pipeline="):
            args["pipeline"] = arg.split("=", 1)[1]
        elif arg == "--pipeline" and len(sys.argv) > sys.argv.index(arg) + 1:
            idx = sys.argv.index(arg)
            args["pipeline"] = sys.argv[idx + 1]
        elif arg == "--social" and len(sys.argv) > sys.argv.index(arg) + 1:
            idx = sys.argv.index(arg)
            if sys.argv[idx + 1] == "only":
                args["social_only"] = True
        elif arg == "--blog" and len(sys.argv) > sys.argv.index(arg) + 1:
            idx = sys.argv.index(arg)
            if sys.argv[idx + 1] == "only":
                args["blog_only"] = True
        elif arg == "--report":
            args["report"] = True
        elif arg == "--help" or arg == "-h":
            print(__doc__)
            sys.exit(0)

    return args


def main():
    """Main entry point."""
    print("╔════════════════════════════════════════════╗")
    print("║   MIFECO Content Generation Engine v1.0   ║")
    print("╚════════════════════════════════════════════╝")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")

    args = parse_args()

    if args["pipeline"]:
        print(f"Pipeline filter: {args['pipeline']}")
    if args["social_only"]:
        print("Mode: Social posts only")
    if args["blog_only"]:
        print("Mode: Blog posts only")
    if args["report"]:
        print("Mode: Report only (no generation)\n")

    # Load all data
    data = load_all_data()

    # Report mode
    if args["report"]:
        generate_report(data, args["pipeline"])
        return

    # Generate social content (unless blog-only)
    social_posts = []
    if not args["blog_only"]:
        social_posts = generate_social_content(data, args["pipeline"])
        if social_posts:
            header = create_output_header(
                "Social media posts generated from pipeline data",
                {"qualified_leads": len(get_qualified_leads(data, args["pipeline"])),
                 "total_posts": len(social_posts),
                 "linkedin_posts": sum(1 for p in social_posts if p["platform"] == "linkedin"),
                 "x_posts": sum(1 for p in social_posts if p["platform"] == "x")}
            )
            output_data = [header] + social_posts
            write_json_output(SOCIAL_OUTPUT_PATH, output_data)
            print(f"\n📱 Social content saved to: {SOCIAL_OUTPUT_PATH}")

    # Generate blog content (unless social-only)
    blog_posts = []
    if not args["social_only"]:
        blog_posts = generate_blog_content(data, args["pipeline"])
        if blog_posts:
            header = create_output_header(
                "Blog posts generated from pipeline themes",
                {"total_posts": len(blog_posts),
                 "categories": list(set(p["category"] for p in blog_posts))}
            )
            output_data = [header] + blog_posts
            write_json_output(BLOG_OUTPUT_PATH, output_data)
            print(f"\n📝 Blog content saved to: {BLOG_OUTPUT_PATH}")

    # Summary
    total = len(social_posts) + len(blog_posts)
    print(f"\n{'═' * 50}")
    print(f"✅ Generation Complete — {total} items total")
    if social_posts:
        print(f"   📱 Social posts: {len(social_posts)}")
    if blog_posts:
        print(f"   📝 Blog posts: {len(blog_posts)}")
    print(f"{'═' * 50}")


if __name__ == "__main__":
    main()
