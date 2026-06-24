---
name: creative-visual-arts
description: "Creative content generation — ASCII art, architecture diagrams, Excalidraw, infographics, p5.js, Manim, ComfyUI, web design, humanizer, and pretext. Class-level umbrella for all visual/creative tools."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, visual, art, diagrams, ascii, infographic, generative, design, animation, video]
    related_skills: [architecture-diagram, ascii-art, ascii-video, excalidraw, humanizer, baoyu-infographic, p5js, manim-video, comfyui, pretext, design-md, popular-web-designs, sketch, claude-design]
---

# Creative & Visual Arts

Class-level umbrella for all creative content generation — diagrams, ASCII art, infographics, animations, generative art, and web design.

## Quick Decision Guide

| Need | Section |
|------|---------|
| Text banners, cowsay, boxes, image-to-ASCII | [ASCII Art](#ascii-art) |
| Architecture/cloud/infra SVG diagrams | [Architecture Diagrams](#architecture-diagrams) |
| Hand-drawn style diagrams (arch, flow, seq) | [Excalidraw](#excalidraw) |
| Infographics (21 layouts × 21 styles) | [Infographics](#infographics) |
| Interactive/generative browser art | [p5.js](#p5js) / [Pretext](#pretext) |
| 3Blue1Brown-style math/algo videos | [Manim](#manim) |
| AI image/video/audio generation | [ComfyUI](#comfyui) |
| Real web design systems as HTML/CSS | [Web Design Systems](#web-design-systems) |
| Design token specs (DESIGN.md) | [DESIGN.md](#design-md) |
| Strip AI-isms from text | [Humanizer](#humanizer) |

## ASCII Art
**Trigger:** Text banners, ASCII art, cowsay, image-to-ASCII conversion.

→ `references/ascii-art.md` — pyfiglet, cowsay, boxes, TOIlet, asciified API, image-to-ASCII, QR codes, weather art, search pre-made art.

## Architecture Diagrams
**Trigger:** Architecture diagrams, cloud/infra diagrams, system diagrams.

→ `references/architecture-diagram.md` — Dark-themed SVG architecture diagrams as standalone HTML. Components: frontend, backend, database, AWS/cloud, security, message bus. Template at `references/architecture-diagram.md`.

## Excalidraw
**Trigger:** Hand-drawn diagrams, flowcharts, sequence diagrams, concept maps.

→ `references/excalidraw.md` — Write Excalidraw JSON, save as `.excalidraw`, drag onto excalidraw.com. Elements: rectangle, ellipse, diamond, arrows, labels, container bindings. Color palette in `references/colors.md`. Upload script in `scripts/upload.py`.

## Infographics
**Trigger:** Infographics, visual summaries, 信息图, 高密度信息大图.

→ `references/baoyu-infographic.md` — 21 layouts × 21 styles. Bento-grid default. Full workflow: analyze → structure → recommend → confirm → generate prompt → image_generate. Layout refs in `references/layouts/`, style refs in `references/styles/`.

## p5.js
**Trigger:** Creative coding, generative art, interactive visualizations, canvas animations.

→ `references/p5js.md` — Browser-based generative art, shaders, interactive sketches. Single-file HTML output.

## Pretext
**Trigger:** DOM-free text layout, ASCII art, typography, kinetic typography, text-as-geometry.

→ `references/pretext.md` — @chenglou/pretext for creative browser demos. Single-file HTML.

## Manim
**Trigger:** Math animations, algorithm walkthroughs, 3Blue1Brown-style explainers.

→ `references/manim-video.md` — Manim CE for animated explanations, equation derivations, data stories. Pipeline: plan → code → render → stitch → audio. References: animations, mobjects, visual design, equations, rendering. Setup script: `scripts/setup.sh`.

## ComfyUI
**Trigger:** AI image generation, stable diffusion, video generation, audio generation.

→ `references/comfyui.md` — ComfyUI with comfy-cli. Local or Cloud. Nodes: flux, sd3, wan-video, hunyuan-video. Setup: `scripts/hardware_check.py` + `scripts/comfyui_setup.sh`.

## Web Design Systems
**Trigger:** Build a page that looks like [Stripe/Linear/Vercel/etc], landing page, UI design.

→ `references/popular-web-designs.md` — 54 real design systems as HTML/CSS templates. Font substitution reference. Templates in `templates/` (stripe.md, linear.md, vercel.md, etc.).

## DESIGN.md
**Trigger:** Design tokens, design system spec, formal brand identity file.

→ `references/design-md.md` — Google's DESIGN.md spec. YAML front matter + markdown body. Lint with `npx @google/design.md`. Export to Tailwind or W3C DTCG. Template: `templates/starter.md`.

## Humanizer
**Trigger:** Remove AI writing patterns, humanize text, strip AI-isms.

→ `references/humanizer.md` — Based on Wikipedia's "Signs of AI writing". Pattern detection and replacement rules.
