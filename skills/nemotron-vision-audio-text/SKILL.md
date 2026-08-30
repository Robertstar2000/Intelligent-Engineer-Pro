---
name: nemotron-vision-audio-text
description: Use NVIDIA Nemotron 3 Nano Omni (30B-A3B MoE, 3B active parameters) for vision, audio transcript analysis, and deep text understanding via OpenRouter.
category: mlops
---
# Nemotron 3 Nano Omni — Vision, Audio & Text Understanding

## Memory context (Hindsight)

Long-term memory context is now provided automatically by Hindsight (bank
`mifeco-default`) on every turn — the retired MemPalace manual query step no
longer applies. Do NOT attempt to import `~/.hermes/mempalace` (it was removed
2026-08-19).This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

Use NVIDIA Nemotron 3 Nano Omni (30B-A3B MoE, 3B active parameters) for multimodal understanding tasks. This is the **default vision model** for Hermes Agent.

## Model Configuration

```yaml
provider: openrouter
model: nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free
# $0/M input, $0/M output (free tier via OpenRouter)
# Supports text, image, video, and audio inputs in a single inference loop
```

## When to Use This Model

1. **Vision Understanding** — Analyzing images, screenshots, diagrams, photos, UI layouts
2. **Audio Transcript Analysis** — Deep reasoning on transcribed voice content
3. **Complex Text Reasoning** — Tasks requiring deep analysis (256K context window)
4. **Multi-document reasoning** — Long-context tasks needing cross-reference

## Task-Specific Guidance

### Vision Tasks
This is the **primary vision model** for Hermes. Use for:
- Analyzing complex UI layouts
- Reading screenshots with embedded text
- Understanding charts, diagrams, or technical drawings
- Any vision task that also needs reasoning, not just OCR
- Infographic analysis

### Text Understanding Tasks
Use when:
- Long documents need cross-reference (256K context window)
- Complex reasoning over multiple inputs
- Tasks requiring both understanding and generation

### Audio Processing
Nemotron Omni accepts audio natively. For audio tasks, pass audio directly or use Whisper for transcription first, then pass the transcript for analysis.

## Available on OpenRouter

Free tier: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`
Paid tier: `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning`

## Current Config

Set as `auxiliary.vision` model in ~/.hermes/config.yaml.

> ✅ **Confirmed working** — Free tier supports image input on OpenRouter as of 2026-06. This replaced the previous `nvidia/nemotron-3-super-120b-a12b:free` which did NOT support vision.