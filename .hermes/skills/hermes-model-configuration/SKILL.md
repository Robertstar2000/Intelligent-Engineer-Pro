---
name: hermes-model-configuration
description: Configure and manage LLM model selection in Hermes Agent — fix model config issues, set primary/fallback models, and troubleshoot model resolution
category: devops
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("Hermes model configuration LLM provider fallback", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Hermes Model Configuration

When the LLM is stuck on the wrong model or not using the configured model, follow this guide.

## Config Structure (~/.hermes/config.yaml)

The `model:` section is a **dict**, not a flat key. Hermes uses nested config:

```yaml
model:
  api_mode: chat_completions
  base_url: https://openrouter.ai/api/v1
  provider: openrouter
  default: nvidia/nemotron-3-super-120b-a12b:free
fallback_providers:
- provider: openrouter
  model: nvidia/nemotron-3-super-120b-a12b
```

## Key Fields

| Field | Location | Purpose |
|-------|----------|---------|
| `model.default` | model section | Primary model string (e.g., `vendor/model-id:free`) |
| `model.provider` | model section | Provider name (e.g., `openrouter`, `nous`, `anthropic`) |
| `model.base_url` | model section | API endpoint URL |
| `model.api_mode` | model section | API mode: `chat_completions`, `anthropic_messages`, `codex_responses` |
| `fallback_providers` | TOP-LEVEL (NOT under model!) | List of `{provider, model}` dicts for API fallback |
| `fallback_model` | TOP-LEVEL (legacy) | Single `{provider, model}` dict — deprecated, use fallback_providers |

## Common Mistakes

1. **`hermes config set fallback_providers` stores JSON as string** — Setting fallback_providers via the CLI with a JSON list stores it as a quoted YAML string, not a list:
   ```yaml
   # WRONG — stored as quoted string, not parsed as list
   fallback_providers: '[{"provider": "openrouter", "model": "deepseek/deepseek-v4-flash"}]'
   ```
   Fix: Use Python script or sed to write the YAML list directly in config.yaml:
   ```bash
   python3 -c "
   import yaml
   c = yaml.safe_load(open('/home/bob/.hermes/config.yaml'))
   c['fallback_providers'] = [{'provider': 'openrouter', 'model': 'your/model-id'}]
   open('/home/bob/.hermes/config.yaml','w').write(yaml.dump(c, default_flow_style=False, sort_keys=False))
   ```
   Note: `yaml.dump` may change the file's formatting slightly (line count, order of some top-level keys). Always verify the result parses correctly.

2. **`model.model` with comma-separated string** — This was a legacy pattern that got parsed as a single broken string. Do NOT use:
   ```yaml
   # WRONG — comma-separated string parsed as one value
   model:
     model: nvidia/nemotron:free, nvidia/nemotron
   ```

3. **`model.fallback`** — This key is NOT recognized by Hermes. Use top-level `fallback_providers` instead.

4. **Flat `model:` string** — Also valid but limited:
   ```yaml
   model: nvidia/nemotron-3-super-120b-a12b:free
   ```
   Works but cannot set provider/base_url/api_mode separately.

## Model Resolution Paths

### Gateway (Telegram/Discord/etc.)

1. `GatewayRunner.__init__` reads config via `_load_gateway_config()`
2. `_resolve_gateway_model()` reads `model.default` or `model.model` → returns model string
3. `_load_fallback_model()` reads top-level `fallback_providers` or `fallback_model`
4. `AIAgent` created via `_resolve_turn_agent_config()` → `resolve_turn_route()` (may override via smart_model_routing)

### CLI (interactive terminal)

1. `load_cli_config()` in `cli.py` reads config.yaml
2. If `model` is string → `defaults["model"]["default"] = string`
3. If `model` is dict → `defaults["model"].update(file_config["model"])`
4. `HermesCLI.__init__` → `AIAgent` with `model=defaults["model"]["default"]`
5. `run_agent.py` normalizes model name via `normalize_model_for_provider()`

## Verification

### Config Parsing Check
```bash
python3 -c "
import yaml
with open('/home/bob/.hermes/config.yaml') as f:
    c = yaml.safe_load(f)
m = c.get('model', {})
print('default:', m.get('default'))
print('provider:', m.get('provider'))
print('base_url:', m.get('base_url'))
print('fallback_providers:', c.get('fallback_providers'))
print('model.model exists:', 'model' in m)  # Should be False or a single model
"

# Check what model the current session is using
python3 -c "
import json, glob
sessions = sorted(glob.glob('/home/bob/.hermes/sessions/session_*.json'), reverse=True)[:3]
for s in sessions:
    with open(s) as f:
        d = json.load(f)
    print(f'{s.split(\"/\")[-1]}: model={d.get(\"model\")}, platform={d.get(\"platform\")}')
"
```

### API-Level Model Verification (Primary + Fallback)

After changing model config, always verify both models respond correctly at the API level. This catches auth errors, rate limits, and model name issues that config parsing alone won't find.

```bash
# Source API key from env file
export $(grep -v "^#" ~/.hermes/.env | xargs)

echo "=== PRIMARY: <primary_model_id> ==="
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "<primary_model_id>", "messages": [{"role": "user", "content": "Reply with just the word: OK"}], "max_tokens": 20}' | python3 -c "import sys,json; d=json.load(sys.stdin); c=d.get('choices',[{}])[0].get('message',{}).get('content','ERROR'); print(c[:50])"

echo "=== FALLBACK: <fallback_model_id> ==="
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "<fallback_model_id>", "messages": [{"role": "user", "content": "Reply with just the word: OK"}], "max_tokens": 20}' | python3 -c "import sys,json; d=json.load(sys.stdin); c=d.get('choices',[{}])[0].get('message',{}).get('content','ERROR'); print(c[:50])"
```

Replace `<primary_model_id>` and `<fallback_model_id>` with the actual model IDs from your config. Both should return a response (not an error JSON).

## Fixing a Broken Model Config

1. Read current config: `read_file ~/.hermes/config.yaml`
2. Look for `model:` section
3. If `model.model` is a comma-separated string → REMOVE it
4. Ensure `model.default` has the correct primary model
5. Add `fallback_providers` at TOP LEVEL (same indent as `model:`)
6. Restart gateway: `sudo systemctl restart hermes-gateway`

## Provider-Specific Notes

- **OpenRouter**: Uses `vendor/model-id` format (e.g., `anthropic/claude-sonnet-4.6`, `openrouter/owl-alpha`)
- **OpenRouter free tier**: Add `:free` suffix (e.g., `nvidia/nemotron-3-super-120b-a12b:free`)
- **OpenRouter model names**: Users may reference models by marketing name (e.g. "alpha owl", "deepseek flash", "claude sonnet"). The actual model ID is always `vendor/model-id`. When the user gives a human-readable name, search OpenRouter or the model catalog to resolve the exact ID before configuring.
- **Anthropic**: Requires `anthropic_messages` api_mode
- **Codex**: Requires `codex_responses` api_mode
- Model names are normalized per-provider via `hermes_cli.model_normalize`

## Troubleshooting Checklist

1. Config parses as valid YAML (no syntax errors)
2. `model.default` exists and is a single model string
3. `fallback_providers` is a list of dicts at top level
4. No comma-separated strings in model config
5. Provider matches the API key available (check `auth.json` and `.env`)
6. Gateway restarted after config change (`sudo systemctl restart hermes-gateway`)
7. Check logs: `journalctl -u hermes-gateway --no-pager | tail -50`

## "Gateway Won't Switch to My Model" — Timeout Triggers Fallback

A common misdiagnosis: the config is correct (`model.default: openrouter/owl-alpha`), the API key works (curl succeeds), but the gateway keeps using a different model. This is usually a **timeout**, not a config bug.

**What happens:**
1. The gateway correctly reads `model.default` and sends requests to the right model.
2. Slow models (especially `owl-alpha`, large reasoning models, or cold-started instances) take 20-60s for their first token.
3. Hermes' API timeout is shorter than that. The connection drops → `APIConnectionError`.
4. After 3 retries, the agent activates its fallback chain.
5. The fallback model (e.g. `qwen/qwen3.6-plus`) is fast, so it "sticks" — every subsequent turn uses it.

**How to diagnose:**
```bash
# Check agent.log for the ACTUAL model attempts, not just the config
grep "model=" ~/.hermes/logs/agent.log | tail -20
# Look for: "APIConnectionError" + "Connection error" on the primary model
# Then: "Fallback activated: <primary> -> <fallback>"
```

**How to fix:**
- Increase `HERMES_API_TIMEOUT` in `~/.hermes/.env` (e.g. `HERMES_API_TIMEOUT=300` for 5 min).
- Or switch the model to one with acceptable latency for your use case.
- After fixing, restart the gateway and watch `agent.log` to confirm the primary model succeeds without connection errors.

**Important:** The fallback model that activates may NOT match `fallback_providers` in your config. Hermes has a built-in agent-level fallback path (`qwen/qwen3.6-plus`) that can activate independently of the user-configured fallback chain. Check the log line `Fallback activated: X -> Y` to see what actually happened.
