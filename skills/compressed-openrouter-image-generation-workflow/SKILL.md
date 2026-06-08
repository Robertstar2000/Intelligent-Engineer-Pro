---
name: compressed-openrouter-image-generation-workflow
description: ""
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("image generation OpenRouter Flux API workflow", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

{"name":"openrouter-image-generation-workflow","goal":"Generate images via OpenRouter API with post-processing","steps":[{"action":"setup","params":{"api":"openrouter","model":"Flux.2-max"}},{"action":"prepare_prompt","input":"user_prompt","output":"processed_prompt"},{"action":"api_call","endpoint":"image/generations","params":{"prompt":"processed_prompt","width":1024,"height":1024},"retry":{"max_attempts":3,"backoff":"exponential"}},{"action":"process_response","extract":"image_url"},{"action":"download_image","url":"image_url","output":"raw_image.png"},{"action":"post_process","input":"raw_image.png","operations":[{"op":"resize","width":1024,"height":1024},{"op":"overlay_text","text":"generated_text","position":"bottom"}],"output":"final_image.png"},{"action":"validate","checks":["file_exists","dimensions","format"]},{"action":"output","format":"png","name":"final_image.png"},{"action":"deliver","platform":"telegram","format":"media","path":"MEDIA:/final_image.png"}]}