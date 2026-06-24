#!/usr/bin/env python3
"""
Social Publisher API Client for Pipeline Engine.

Connects the pipeline-engine to the social-direct-publisher FastAPI service.
Provides functions to create social post drafts from pipeline events,
check approval status, and trigger publishing.

Usage:
    python3 social_publisher_client.py --action create_draft --pipeline book-pub --event book_published --book-key nbs-1
    python3 social_publisher_client.py --action list_drafts
    python3 social_publisher_client.py --action publish_approved
    python3 social_publisher_client.py --action status --post-id <uuid>

Environment:
    SOCIAL_PUBLISHER_URL — Base URL of the social publisher API (default: http://localhost:8000)
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx

# ── Configuration ──────────────────────────────────────────────────────────────

SOCIAL_PUBLISHER_URL = os.environ.get("SOCIAL_PUBLISHER_URL", "http://localhost:8000")
PIPELINE_DATA_DIR = Path.home() / ".hermes" / "pipeline-engine" / "data"
SOCIAL_DRAFTS_FILE = PIPELINE_DATA_DIR / "social-publisher-drafts.json"

# ── Platform formatting (mirrors the social-direct-publisher service) ─────────

PLATFORM_LIMITS = {
    "linkedin": 3000,
    "facebook": 63206,  # Facebook's actual limit
    "instagram": 2200,
}


def format_for_platform(platform: str, text: str, link_url: str | None = None) -> str:
    """Format post text for a specific platform."""
    text = text.strip()
    if platform == "linkedin":
        result = text
        if link_url:
            result += f"\n\n{link_url}"
        if len(result) > PLATFORM_LIMITS["linkedin"]:
            raise ValueError(f"LinkedIn post exceeds {PLATFORM_LIMITS['linkedin']} chars ({len(result)})")
        return result
    elif platform == "facebook":
        result = text
        if link_url:
            result += f"\n\n{link_url}"
        return result
    elif platform == "instagram":
        result = text
        if link_url:
            result += "\n\nLink in bio."
        if len(result) > PLATFORM_LIMITS["instagram"]:
            raise ValueError(f"Instagram caption exceeds {PLATFORM_LIMITS['instagram']} chars ({len(result)})")
        return result
    raise ValueError(f"Unsupported platform: {platform}")


# ── Content generation from pipeline events ────────────────────────────────────

def generate_book_launch_posts(book_title: str, book_key: str, asin: str | None = None,
                                series_name: str | None = None, genre: str = "Science Fiction") -> list[dict]:
    """Generate social media posts for a book launch."""
    amazon_url = f"https://www.amazon.com/dp/{asin}" if asin else f"https://www.mifeco.com/books/"
    campaign = f"book-launch-{book_key}"

    posts = []

    # LinkedIn — professional/author brand
    linkedin_text = format_for_platform("linkedin",
        f"Excited to announce that {book_title} is now live!"
        + (f"\n\nThe latest installment in the {series_name} series." if series_name else "")
        + f"\n\n{genre} that explores what happens when humanity reaches for the stars — and what we leave behind."
        + f"\n\nGrab your copy on Amazon: {amazon_url}"
        + "\n\n#SciFi #Books #Author #MIFECO" + (f" #{series_name.replace(' ', '')}" if series_name else ""),
        amazon_url
    )
    posts.append({
        "platform": "linkedin",
        "campaign": campaign,
        "text": linkedin_text,
        "link_url": amazon_url,
        "media_urls": [],  # Cover image URL would be added here
    })

    # Facebook — reader community
    facebook_text = format_for_platform("facebook",
        f"The wait is over! {book_title} is finally here. 🎉"
        + (f"\n\nBook {series_name}" if series_name else "")
        + f"\n\nA gripping {genre.lower()} tale that will keep you turning pages late into the night."
        + "\n\nGet your copy now — available on Amazon in Kindle and paperback.",
        amazon_url
    )
    posts.append({
        "platform": "facebook",
        "campaign": campaign,
        "text": facebook_text,
        "link_url": amazon_url,
        "media_urls": [],
    })

    # Instagram — visual/book cover
    instagram_text = format_for_platform("instagram",
        f"📚 {book_title} is LIVE!"
        + (f"\n\nThe latest in the {series_name} series." if series_name else "")
        + "\n\nSwipe to see the cover →"
        + "\n\n#SciFi #Books #BookLaunch #MIFECO" + (f" #{series_name.replace(' ', '')}" if series_name else ""),
        amazon_url
    )
    posts.append({
        "platform": "instagram",
        "campaign": campaign,
        "text": instagram_text,
        "link_url": None,  # Instagram uses "Link in bio"
        "media_urls": [],  # Cover image URL would be added here
    })

    return posts


def generate_blog_crosspost(blog_title: str, blog_slug: str, blog_url: str,
                              post_type: str = "book") -> list[dict]:
    """Generate social media posts to cross-promote a blog post."""
    campaign = f"blog-{blog_slug}"
    posts = []

    # LinkedIn
    linkedin_text = format_for_platform("linkedin",
        f"New on the MIFECO blog: {blog_title}"
        f"\n\nI break down the key insights and what they mean for your business."
        f"\n\nRead the full post: {blog_url}"
        f"\n\n#MIFECO #AI #Business",
        blog_url
    )
    posts.append({
        "platform": "linkedin",
        "campaign": campaign,
        "text": linkedin_text,
        "link_url": blog_url,
        "media_urls": [],
    })

    # Facebook
    facebook_text = format_for_platform("facebook",
        f"New blog post: {blog_title}"
        f"\n\nWorth a read if you're thinking about AI for your business."
        f"\n\n{blog_url}",
        blog_url
    )
    posts.append({
        "platform": "facebook",
        "campaign": campaign,
        "text": facebook_text,
        "link_url": blog_url,
        "media_urls": [],
    })

    # Instagram
    instagram_text = format_for_platform("instagram",
        f"📝 New blog: {blog_title}"
        f"\n\nLink in bio for the full post."
        f"\n\n#MIFECO #AI #Business #Blog",
        blog_url
    )
    posts.append({
        "platform": "instagram",
        "campaign": campaign,
        "text": instagram_text,
        "link_url": None,
        "media_urls": [],
    })

    return posts


def generate_saas_promo_posts(product_name: str, product_key: str, product_url: str,
                                price: str = "$99/mo") -> list[dict]:
    """Generate social media posts for a SaaS product."""
    campaign = f"saas-promo"
    posts = []

    linkedin_text = format_for_platform("linkedin",
        f"🚀 {product_name} is now live!"
        f"\n\nAI-powered project management for engineering teams."
        f"\n\nStarting at {price}. Try it free for 14 days."
        f"\n\n{product_url}"
        f"\n\n#SaaS #AI #ProjectManagement #Engineering",
        product_url
    )
    posts.append({
        "platform": "linkedin",
        "campaign": campaign,
        "text": linkedin_text,
        "link_url": product_url,
        "media_urls": [],
    })

    facebook_text = format_for_platform("facebook",
        f"Struggling with project management? {product_name} uses AI to help engineering teams stay on track."
        f"\n\nStarting at {price}. Free 14-day trial."
        f"\n\n{product_url}",
        product_url
    )
    posts.append({
        "platform": "facebook",
        "campaign": campaign,
        "text": facebook_text,
        "link_url": product_url,
        "media_urls": [],
    })

    instagram_text = format_for_platform("instagram",
        f"🚀 {product_name} is LIVE!"
        f"\n\nAI-powered project management"
        f"\n\nStarting at {price}"
        f"\n\nLink in bio"
        f"\n\n#SaaS #AI #ProjectManagement",
        product_url
    )
    posts.append({
        "platform": "instagram",
        "campaign": campaign,
        "text": instagram_text,
        "link_url": None,
        "media_urls": [],
    })

    return posts


def generate_consulting_promo_posts(tier_name: str = "AI Readiness Assessment",
                                      price: str = "$199") -> list[dict]:
    """Generate social media posts for consulting services."""
    campaign = "consulting-promo"
    consult_url = "https://mifeco.com/consult/"
    posts = []

    linkedin_text = format_for_platform("linkedin",
        f"Want to know if your business is ready for AI?"
        f"\n\nMy {tier_name} ({price}) gives you a comprehensive 30+ page report with:"
        f"\n• Current state analysis"
        f"\n• AI opportunity assessment"
        f"\n• Prioritized action plan"
        f"\n• ROI projections"
        f"\n\nDelivered within 4 hours of survey completion."
        f"\n\n{consult_url}"
        f"\n\n#AIConsulting #DigitalTransformation #BusinessStrategy",
        consult_url
    )
    posts.append({
        "platform": "linkedin",
        "campaign": campaign,
        "text": linkedin_text,
        "link_url": consult_url,
        "media_urls": [],
    })

    facebook_text = format_for_platform("facebook",
        f"Thinking about AI for your business but don't know where to start?"
        f"\n\nThe {tier_name} ({price}) gives you a clear roadmap — no jargon, no hype."
        f"\n\n{consult_url}",
        consult_url
    )
    posts.append({
        "platform": "facebook",
        "campaign": campaign,
        "text": facebook_text,
        "link_url": consult_url,
        "media_urls": [],
    })

    instagram_text = format_for_platform("instagram",
        f"🤖 Is your business AI-ready?"
        f"\n\nFind out with a professional assessment."
        f"\n\n30+ page report • 4-hour delivery"
        f"\n\nLink in bio"
        f"\n\n#AIConsulting #Business #AI",
        consult_url
    )
    posts.append({
        "platform": "instagram",
        "campaign": campaign,
        "text": instagram_text,
        "link_url": None,
        "media_urls": [],
    })

    return posts


# ── API client functions ────────────────────────────────────────────────────────

def create_social_post_draft(posts: list[dict], owner_user_id: str = "bob",
                               created_by: str = "pipeline-engine") -> list[dict]:
    """Submit social post drafts to the social publisher API."""
    results = []
    for post in posts:
        payload = {
            "owner_user_id": owner_user_id,
            "created_by": created_by,
            "base_message": post["text"],
            "platforms": [post["platform"]],
            "account_ids": [],  # Will use default accounts
            "campaign": post.get("campaign", ""),
            "link_url": post.get("link_url"),
            "approval_mode": "approve_then_publish",
        }
        try:
            resp = httpx.post(
                f"{SOCIAL_PUBLISHER_URL}/social/posts",
                json=payload,
                timeout=30,
            )
            if resp.status_code == 200:
                result = resp.json()
                result["_local_campaign"] = post.get("campaign", "")
                result["_local_platform"] = post["platform"]
                results.append(result)
                print(f"  ✅ Draft created: {post['platform']} — {result.get('id', 'N/A')}")
            else:
                print(f"  ❌ Failed: {post['platform']} — {resp.status_code} {resp.text}")
                results.append({"error": resp.text, "platform": post["platform"]})
        except Exception as e:
            print(f"  ❌ Error: {post['platform']} — {e}")
            results.append({"error": str(e), "platform": post["platform"]})
    return results


def list_drafts(status: str = "pending_approval") -> list[dict]:
    """List social posts from the publisher API."""
    try:
        resp = httpx.get(
            f"{SOCIAL_PUBLISHER_URL}/social/posts",
            params={"status": status},
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json()
        print(f"Error: {resp.status_code} {resp.text}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def approve_post(post_id: str, approved_by: str = "bob") -> dict:
    """Approve a social post for publishing."""
    try:
        resp = httpx.post(
            f"{SOCIAL_PUBLISHER_URL}/social/posts/{post_id}/approve",
            json={"approved_by": approved_by},
            timeout=30,
        )
        return resp.json() if resp.status_code == 200 else {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}


def publish_post(post_id: str, actor: str = "bob") -> dict:
    """Publish an approved social post via API."""
    try:
        resp = httpx.post(
            f"{SOCIAL_PUBLISHER_URL}/social/posts/{post_id}/publish",
            json={"actor": actor, "force": False},
            timeout=60,
        )
        return resp.json() if resp.status_code == 200 else {"error": resp.text}
    except Exception as e:
        return {"error": str(e)}


def publish_all_approved(actor: str = "bob") -> list[dict]:
    """Find and publish all approved posts."""
    results = []
    try:
        resp = httpx.get(
            f"{SOCIAL_PUBLISHER_URL}/social/posts",
            params={"status": "approved"},
            timeout=30,
        )
        if resp.status_code != 200:
            return [{"error": resp.text}]

        posts = resp.json()
        if isinstance(posts, list):
            for post in posts:
                post_id = post.get("id")
                if post_id:
                    result = publish_post(post_id, actor)
                    results.append(result)
                    status = result.get("status", "unknown")
                    print(f"  {'✅' if status == 'published' else '❌'} {post_id} — {status}")
        return results
    except Exception as e:
        return [{"error": str(e)}]


# ── Local draft tracking ───────────────────────────────────────────────────────

def save_local_drafts(drafts: list[dict]):
    """Save draft records to local JSON for pipeline tracking."""
    existing = []
    if SOCIAL_DRAFTS_FILE.exists():
        with open(SOCIAL_DRAFTS_FILE) as f:
            existing = json.load(f)

    existing.extend(drafts)
    with open(SOCIAL_DRAFTS_FILE, "w") as f:
        json.dump(existing, f, indent=2, default=str)
    print(f"  💾 Saved {len(drafts)} drafts to {SOCIAL_DRAFTS_FILE}")


# ── Main CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Social Publisher API Client for Pipeline Engine")
    parser.add_argument("--action", required=True,
                        choices=["create_draft", "list_drafts", "approve", "publish",
                                 "publish_approved", "status", "book_launch", "blog_crosspost",
                                 "saas_promo", "consulting_promo"])
    parser.add_argument("--pipeline", help="Pipeline ID that triggered the event")
    parser.add_argument("--event", help="Event type (book_published, blog_published, etc.)")
    parser.add_argument("--book-key", help="Book key identifier")
    parser.add_argument("--book-title", help="Book title")
    parser.add_argument("--asin", help="Amazon ASIN")
    parser.add_argument("--series", help="Series name")
    parser.add_argument("--genre", default="Science Fiction", help="Book genre")
    parser.add_argument("--blog-title", help="Blog post title")
    parser.add_argument("--blog-slug", help="Blog post slug")
    parser.add_argument("--blog-url", help="Blog post URL")
    parser.add_argument("--product-name", help="SaaS product name")
    parser.add_argument("--product-url", help="SaaS product URL")
    parser.add_argument("--price", default="$99/mo", help="Product price")
    parser.add_argument("--post-id", help="Social post ID for approve/publish/status")
    parser.add_argument("--status", default="pending_approval", help="Filter by status")
    parser.add_argument("--owner", default="bob", help="Owner user ID")
    args = parser.parse_args()

    print(f"🔗 Social Publisher API: {SOCIAL_PUBLISHER_URL}")
    print(f"📋 Action: {args.action}")
    print()

    if args.action == "create_draft":
        print("Creating social post draft from pipeline event...")
        # This is a generic wrapper — use specific actions for content generation
        print("Use --action book_launch, blog_crosspost, saas_promo, or consulting_promo")

    elif args.action == "book_launch":
        if not args.book_title or not args.book_key:
            print("❌ --book-title and --book-key required")
            sys.exit(1)
        print(f"📚 Generating book launch posts: {args.book_title}")
        posts = generate_book_launch_posts(
            book_title=args.book_title,
            book_key=args.book_key,
            asin=args.asin,
            series_name=args.series,
            genre=args.genre,
        )
        results = create_social_post_draft(posts, owner_user_id=args.owner)
        save_local_drafts(results)

    elif args.action == "blog_crosspost":
        if not args.blog_title or not args.blog_slug or not args.blog_url:
            print("❌ --blog-title, --blog-slug, and --blog-url required")
            sys.exit(1)
        print(f"📝 Generating blog cross-posts: {args.blog_title}")
        posts = generate_blog_crosspost(
            blog_title=args.blog_title,
            blog_slug=args.blog_slug,
            blog_url=args.blog_url,
        )
        results = create_social_post_draft(posts, owner_user_id=args.owner)
        save_local_drafts(results)

    elif args.action == "saas_promo":
        if not args.product_name or not args.product_url:
            print("❌ --product-name and --product-url required")
            sys.exit(1)
        print(f"🚀 Generating SaaS promo posts: {args.product_name}")
        posts = generate_saas_promo_posts(
            product_name=args.product_name,
            product_key=args.book_key or "",
            product_url=args.product_url,
            price=args.price,
        )
        results = create_social_post_draft(posts, owner_user_id=args.owner)
        save_local_drafts(results)

    elif args.action == "consulting_promo":
        print(f"💼 Generating consulting promo posts")
        posts = generate_consulting_promo_posts()
        results = create_social_post_draft(posts, owner_user_id=args.owner)
        save_local_drafts(results)

    elif args.action == "list_drafts":
        drafts = list_drafts(status=args.status)
        print(f"Found {len(drafts)} drafts with status '{args.status}':")
        for d in drafts:
            print(f"  [{d.get('status')}] {d.get('id')} — {d.get('base_message', '')[:60]}...")

    elif args.action == "approve":
        if not args.post_id:
            print("❌ --post-id required")
            sys.exit(1)
        result = approve_post(args.post_id)
        print(f"Approval result: {json.dumps(result, indent=2, default=str)}")

    elif args.action == "publish":
        if not args.post_id:
            print("❌ --post-id required")
            sys.exit(1)
        result = publish_post(args.post_id)
        print(f"Publish result: {json.dumps(result, indent=2, default=str)}")

    elif args.action == "publish_approved":
        print("Publishing all approved posts...")
        results = publish_all_approved()
        published = sum(1 for r in results if r.get("status") == "published")
        failed = sum(1 for r in results if r.get("status") == "failed")
        print(f"\nResults: {published} published, {failed} failed, {len(results)} total")

    elif args.action == "status":
        if not args.post_id:
            print("❌ --post-id required")
            sys.exit(1)
        try:
            resp = httpx.get(f"{SOCIAL_PUBLISHER_URL}/social/posts/{args.post_id}", timeout=30)
            if resp.status_code == 200:
                print(json.dumps(resp.json(), indent=2, default=str))
            else:
                print(f"Error: {resp.status_code}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
