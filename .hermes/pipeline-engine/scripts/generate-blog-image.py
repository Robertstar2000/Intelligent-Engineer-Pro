#!/usr/bin/env python3
"""
Gemini Image Generator for MIFECO Blog Posts

Uses Google AI Studio API (gemini-2.5-flash-image) to generate images.
Supports two modes:
  1. "cover-inspired" — Generate image inspired by a book cover's theme
  2. "infographic" — Generate an infographic representing blog content

Usage:
  python3 generate-blog-image.py --mode=cover-inspired --prompt="..." --output=/tmp/image.png
  python3 generate-blog-image.py --mode=infographic --prompt="..." --output=/tmp/image.png

Environment:
  GOOGLE_AI_STUDIO_KEY — API key for Google AI Studio
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

GEMINI_IMAGE_MODEL = "gemini-2.5-flash-image"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def generate_image(prompt: str, api_key: str, output_path: str) -> dict:
    """Generate an image using Gemini 2.5 Flash Image model."""
    url = f"{API_BASE}/{GEMINI_IMAGE_MODEL}:generateContent?key={api_key}"
    
    payload = json.dumps({
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"error": str(e)}
    
    # Extract image from response
    candidates = data.get("candidates", [])
    if not candidates:
        return {"error": "No candidates in response", "raw": data[:500] if isinstance(data, str) else str(data)[:500]}
    
    parts = candidates[0].get("content", {}).get("parts", [])
    image_data = None
    text_response = ""
    
    for part in parts:
        if "inlineData" in part:
            image_data = part["inlineData"].get("data")
        if "text" in part:
            text_response += part["text"]
    
    if not image_data:
        return {"error": "No image in response", "text": text_response[:500]}
    
    # Save image
    try:
        img_bytes = base64.b64decode(image_data)
        with open(output_path, "wb") as f:
            f.write(img_bytes)
        return {
            "success": True,
            "output_path": output_path,
            "size_bytes": len(img_bytes),
            "text_response": text_response[:200] if text_response else None,
        }
    except Exception as e:
        return {"error": f"Failed to save image: {e}"}


def build_cover_prompt(book_title: str, series: str, genre: str, description: str) -> str:
    """Build an image prompt inspired by a book cover's theme."""
    return (
        f"Create a stunning, professional book-cover-inspired illustration for a blog post about "
        f"the book '{book_title}' from the '{series}' series. "
        f"Genre: {genre}. "
        f"Book theme: {description}. "
        f"Style: Cinematic, high-quality digital art. The image should evoke the mood and themes of the book "
        f"while being suitable as a blog post featured image. 16:9 landscape aspect ratio, photorealistic style. "
        f"Do not include any text, titles, or watermarks in the image."
    )


def build_infographic_prompt(post_title: str, content_summary: str, category: str) -> str:
    """Build an image prompt for a SaaS/Consulting infographic."""
    return (
        f"Create a professional, modern infographic-style featured image for a blog post titled "
        f"'{post_title}' in the '{category}' category. "
        f"The blog content is about: {content_summary}. "
        f"Style: Clean, modern infographic design with visual metaphors representing the key concepts. "
        f"Use a professional color palette (blues, purples, teals). Include abstract visual elements "
        f"like flowing data streams, icons, charts, or conceptual illustrations. "
        f"16:9 landscape aspect ratio. Do not include any text or words in the image."
    )


def main():
    parser = argparse.ArgumentParser(description="Generate blog post images with Gemini")
    parser.add_argument("--mode", choices=["cover-inspired", "infographic"], required=True)
    parser.add_argument("--output", required=True, help="Output file path (PNG)")
    parser.add_argument("--book-title", help="Book title (cover mode)")
    parser.add_argument("--series", help="Book series (cover mode)")
    parser.add_argument("--genre", help="Book genre (cover mode)")
    parser.add_argument("--description", help="Book description (cover mode)")
    parser.add_argument("--post-title", help="Blog post title (infographic mode)")
    parser.add_argument("--content-summary", help="Content summary (infographic mode)")
    parser.add_argument("--category", help="Post category (infographic mode)")
    parser.add_argument("--prompt", help="Custom prompt (overrides auto-generation)")
    args = parser.parse_args()
    
    api_key = os.environ.get("GOOGLE_AI_STUDIO_KEY", "")
    if not api_key:
        # Try loading from .env
        env_path = os.path.expanduser("~/.hermes/.env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.strip().startswith("GOOGLE_AI_STUDIO_KEY="):
                        api_key = line.strip().split("=", 1)[1].strip().strip("'\"")
                        break
    if not api_key:
        print(json.dumps({"error": "GOOGLE_AI_STUDIO_KEY not found in env or ~/.hermes/.env"}))
        sys.exit(1)
    
    # Build prompt
    if args.prompt:
        prompt = args.prompt
    elif args.mode == "cover-inspired":
        if not all([args.book_title, args.series]):
            print(json.dumps({"error": "cover-inspired mode requires --book-title and --series"}))
            sys.exit(1)
        prompt = build_cover_prompt(
            args.book_title, args.series,
            args.genre or "Science Fiction",
            args.description or "Exploration and discovery"
        )
    elif args.mode == "infographic":
        if not all([args.post_title, args.content_summary]):
            print(json.dumps({"error": "infographic mode requires --post-title and --content-summary"}))
            sys.exit(1)
        prompt = build_infographic_prompt(
            args.post_title, args.content_summary,
            args.category or "Business"
        )
    else:
        print(json.dumps({"error": f"Unknown mode: {args.mode}"}))
        sys.exit(1)
    
    result = generate_image(prompt, api_key, args.output)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
