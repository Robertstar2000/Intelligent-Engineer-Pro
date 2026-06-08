---
name: discord-gateway-testing
description: Verify both outbound (send) and inbound (read/receive) paths for Discord via the Hermes Gateway — including REST API message fetching and config awareness of @mention requirements.
tags: [discord, gateway, messaging, connectivity, testing]
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Discord Gateway Connectivity Testing

Use when: setting up Discord for the first time, verifying the gateway works after configuration changes, debugging why Discord replies aren't being received, or confirming bidirectional connectivity.

## Prerequisites

- Discord bot token stored in `~/.hermes/.env` as `DISCORD_BOT_TOKEN`
- Gateway is running (`hermes gateway status`)
- Bot is in the target Discord server
- You know the target channel ID (get it from `channel_directory.json` or by listing available targets with `send_message action=list`)

## 1. Verify Gateway Connection

```bash
# Gateway state (check Discord is "connected")
cat ~/.hermes/gateway_state.json | grep -A5 discord

# Gateway logs — look for "Connected as"
grep -i "discord" ~/.hermes/logs/agent.log | grep -i "connected as"
```

Expected: `"state": "connected"` and `Connected as FL Hermes#6993` (or your bot's name).

## 2. Outbound Test (Send a Message)

```bash
# List available targets to get channel info
# Then send a test message via:
#   send_message(target="discord:#general", message="...")
```

Use `send_message` with the appropriate target. The API returns a `message_id` on success — save it for inbound verification.

**Success signal:** API returns `{"success": true, "platform": "discord", "chat_id": "...", "message_id": "..."}`

## 3. Inbound Test (Read Messages from Discord)

The gateway only captures Discord messages where the bot is **@mentioned** (due to `require_mention: true` by default). To read messages without @mention, use the Discord REST API directly:

```python
import requests

# Get bot token
with open(os.path.expanduser("~/.hermes/.env")) as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

headers = {"Authorization": f"Bot {token}"}

# Fetch recent messages from a channel
# Channel ID from channel_directory.json or send_message list output
url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages?limit=10"
resp = requests.get(url, headers=headers)

if resp.status_code == 200:
    messages = resp.json()
    for msg in messages:
        author = msg["author"]["username"]
        content = msg.get("content", "")
        print(f"[{msg['timestamp'][:19]}] {author}: {content}")
else:
    print(f"Error: {resp.status_code} {resp.text}")
```

**Success signal:** Returns JSON with message array including author, content, timestamp.

## 4. Checking for @Mentions

Messages where the bot IS @mentioned will be captured by the gateway and logged:

```bash
grep "discord.*inbound\|inbound.*discord" ~/.hermes/logs/agent.log
```

If a reply was sent but not captured, check if it contained an @mention of the bot:

```python
for msg in messages:
    mentioned = any(m.get("username") == "FL Hermes" for m in msg.get("mentions", []))
    # Or check by bot ID:
    mentioned = any(m.get("id") == bot_id for m in msg.get("mentions", []))
```

## 5. Config Reference

Key Discord config in `~/.hermes/config.yaml`:

```yaml
discord:
  require_mention: true   # ✨ KEY: only capture @mentioned messages inbound
  free_response_channels: ''  # channels where bot responds without @mention
  allowed_channels: ''        # restrict to specific channels
  auto_thread: true           # auto-create threads for /skill commands
  reactions: true             # react to acknowledge skill commands
```

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Outbound works but replies aren't received | `require_mention: true` — reply didn't @mention bot | Either @mention the bot, or temporarily disable `require_mention` in config |
| API returns 401 | Bot token is wrong or expired | Regenerate token in Discord Developer Portal, update `.env` |
| API returns 403 | Bot lacks permissions or is not in the server | Check bot has `Read Messages` + `View Channel` permissions |
| `channel_directory.json` is stale | Gateway hasn't refreshed channel list | Restart gateway: `hermes gateway restart` |
| Gateway logs show "Disconnected" | Bot token invalid, rate limited, or network issue | Check `DISCORD_BOT_TOKEN` in `.env`, verify gateway uptime |
| No Discord entry in `channel_directory.json` | Gateway hasn't re-scanned since Discord was configured | Check gateway state is "connected"; if so, manually add or restart |

## Quick Verification Script

Save as `~/.hermes/scripts/test-discord.py`:

```python
"""Test Discord outbound and inbound connectivity."""
import os, sys, json, requests

HOME = os.path.expanduser("~/.hermes")

# Read bot token from .env
with open(os.path.join(HOME, ".env")) as f:
    env = f.read()
token = None
for line in env.split("\n"):
    line = line.strip()
    if line.startswith("DISCORD_BOT_TOKEN="):
        token = line.split("=", 1)[1].strip().strip('"').strip("'")
        break

if not token:
    print("FAIL: DISCORD_BOT_TOKEN not found in .env")
    sys.exit(1)

# Test API connectivity
headers = {"Authorization": f"Bot {token}"}
resp = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
if resp.status_code == 200:
    bot = resp.json()
    print(f"OK: Connected as {bot['username']}#{bot['discriminator']} (ID: {bot['id']})")
else:
    print(f"FAIL: API auth failed: {resp.status_code}")
    sys.exit(1)

# Read channel directory
cd_path = os.path.join(HOME, "channel_directory.json")
if os.path.exists(cd_path):
    with open(cd_path) as f:
        cd = json.load(f)
    discord_channels = [c for c in cd.get("platforms", {}).get("discord", [])]
    print(f"\nAvailable Discord channels ({len(discord_channels)}):")
    for c in discord_channels:
        print(f"  #{c['name']} (ID: {c['id']}) — guild: {c.get('guild', '?')}")

    if discord_channels:
        ch = discord_channels[0]
        msg_url = f"https://discord.com/api/v10/channels/{ch['id']}/messages?limit=5"
        msg_resp = requests.get(msg_url, headers=headers)
        if msg_resp.status_code == 200:
            msgs = msg_resp.json()
            print(f"\nLast {len(msgs)} messages in #{ch['name']}:")
            for m in msgs:
                mentioned = any(g.get("id") == bot["id"] for g in m.get("mentions", []))
                tag = " (@bot)" if mentioned else ""
                print(f"  [{m['timestamp'][:19]}] {m['author']['username']}{tag}: {m.get('content','')[:120]}")
        else:
            print(f"FAIL: Could not read channel #{ch['name']}: {msg_resp.status_code}")
else:
    print("No channel_directory.json found — run send_message action=list first")
