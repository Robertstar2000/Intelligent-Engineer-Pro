---
name: telegram-gateway-troubleshooting
description: Diagnose and fix Telegram delivery failures in the Hermes Gateway — token validation, chat ID resolution, network errors, polling conflicts, and allowlist issues.
tags: [telegram, gateway, messaging, troubleshooting]
---

## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("Telegram gateway troubleshooting delivery failure network error", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Telegram Gateway Troubleshooting

Use when: `send_message` to Telegram fails, the gateway logs show Telegram errors, cron jobs report delivery failures, or test messages don't arrive.

## Diagnostic Steps

### 1. Verify Gateway is Running
```bash
systemctl status hermes-gateway.service --no-pager
```

### 2. Check Gateway Logs for Errors
```bash
journalctl -u hermes-gateway.service --no-pager -n 30 | grep -i telegram
```

Common errors and their meanings:
- `httpx.ReadError` — network/HTTP disconnect; the gateway auto-reconnects (up to 10 attempts)
- `terminated by other getUpdates request` — multiple long-polling clients hitting the same bot; only one can poll at a time
- `chat not found` — the chat_id has never started a conversation with the bot, or the user blocked it
- `Bad Request` — invalid message format, markdown parse error, or entity issues
- `bot was kicked from the supergroup` — bot was removed from a chat
- `Forbidden: bot was blocked by the user` — user blocked the bot

### 3. Verify Bot Token is Valid and Not Masked
```bash
# Check the actual token value (NOT the masked *** placeholder)
grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env

# Test the token directly
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
curl -s "https://api.telegram.org/bot${TOKEN}/getMe"
```

Expected: `{"ok":true,"result":{"id":...,"is_bot":true,...}}`

Pitfall: The `.env` file may have literally `TELEGRAM_BOT_TOKEN=***` as placeholder. The real token is set in `.openclaw/openclaw.json` or was placed after initial setup. Always read the actual value with `cut` — never trust grep display alone.

### 4. Check if Chat ID is Reachable
```bash
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
curl -s "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=<CHAT_ID>" \
  -d "text=Test"
```

If you get `Bad Request: chat not found`:
- The user has NEVER sent a message to the bot. Bots CANNOT initiate conversations.
- Fix: Tell the user to open Telegram, search for the bot (e.g., `@FLBobBot`), and send any message like "hi".
- Then re-verify: `curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates?limit=3"`

### 5. Check Allowed Users Configuration

**Check BOTH locations — the config.yaml allowlist AND the .env variable:**

```bash
# 1. Hermes config.yaml (NEWER — this is the one that actually gates incoming messages)
grep -A 5 '^telegram:' ~/.hermes/config.yaml

# 2. Hermes .env (legacy — may be empty even when config.yaml is set)
grep 'TELEGRAM_ALLOWED_USERS\|GATEWAY_ALLOW' ~/.hermes/.env
```

**The `telegram.allowed_chats` field in `~/.hermes/config.yaml` is the active gate.** If it is `''` (empty string), ALL incoming Telegram messages are rejected — even from the bot's owner. The error in logs reads: `Unauthorized user: <chat_id> (<name>) on telegram`.

**Fix — TWO locations must BOTH be set:**

1. **`~/.hermes/config.yaml`** — `telegram.allowed_chats`:
   ```bash
   # DO NOT use hermes config set — it wraps the value in quotes, producing
   # allowed_chats: '[8137891480]' (a string) instead of a proper YAML list.
   # Edit the file directly:
   sed -i "s/allowed_chats:.*/allowed_chats: [<your_chat_id>]/" ~/.hermes/config.yaml
   ```

2. **`~/.hermes/.env`** — `TELEGRAM_ALLOWED_USERS` (legacy but still active):
   ```bash
   sed -i "s/TELEGRAM_ALLOWED_USERS=.*/TELEGRAM_ALLOWED_USERS=<your_chat_id>/" ~/.hermes/.env
   ```

Then restart:
```bash
hermes gateway restart
```

Where `<your_chat_id>` is your numeric Telegram chat ID (e.g. `8137891480`). Find it from the `Unauthorized user` log line, or from `getUpdates` API output.

**Pitfall:** `hermes config set telegram.allowed_chats "8137891480"` looks correct but YAML-encodes it as a quoted string `'[8137891480]'` instead of a list. The gateway then fails to match any chat ID. Always use `sed` to edit `config.yaml` directly for list-valued fields.

**Pitfall:** The `.env` variable `TELEGRAM_ALLOWED_USERS` is a separate gate from `config.yaml`. If it is set to `n`, `0`, empty, or any value that doesn't include your chat ID, incoming messages are rejected even when `config.yaml` is correct. Always check BOTH locations.

### 6. Check for Polling Conflicts
```bash
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates?limit=1"
```

If you get `Conflict: terminated by other getUpdates request`:
- Multiple processes are long-polling the same bot.
- The Hermes gateway handles this gracefully (auto-reconnects), but other OpenClaw instances or manual scripts may conflict.
- Only the gateway should be doing long polling. Kill any other process using the token.

### 7. Check Recent Telegram Updates (Who Has Contacted the Bot)
```bash
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates?limit=10"
```

This shows which users the bot can actually message. You can only send messages to users who have initiated a conversation first.

### 8. Investigate Persistent Network Errors (httpx.ReadError)

If the gateway repeatedly logs `httpx.ReadError` (not `httpx.ConnectError`), the connection is being **dropped mid-polling**. Unlike full connect failures, these auto-reconnect briefly but cause message loss.

#### 8a. Characterize the Error Pattern

```bash
# Count errors
grep -c "Telegram network error" ~/.hermes/logs/errors.log

# Measure timing between consecutive errors — key diagnostic
grep "Telegram network error" ~/.hermes/logs/errors.log | head -30 | awk '{
  split($2,time,":");
  t = time[1]*3600 + time[2]*60 + time[3];
  if (prev > 0) printf "Interval: %d seconds (%.1f min)\n", t-prev, (t-prev)/60;
  prev = t;
}'
```

**Known patterns:**

- **Every ~5 minutes (306s) in tight pairs** (two errors at the same second, then nothing for ~306s) → **WiFi Power Management**. The first reconnect attempt also fails because the WiFi card is still in low-power mode. The pair-with-pause pattern is the most specific diagnostic signature — distinct from random network hiccups.
- **Erratic intervals** → Network congestion, firewall/proxy timeout, or ISP-level connection reset.
- **Every 30-300s** → Could be reverse proxy keepalive timeout (check `haproxy`, `nginx`, or corporate firewall idle timeout config).

#### 8b. Check WiFi Power Management (Most Common Cause)

```bash
# Check current state
iwconfig wlp2s0 2>&1 | grep -i "Power"
# Expected: "Power Management:off" — if "on", this is the root cause

# Check kernel power control
cat /sys/class/net/wlp2s0/power/control
# Expected: "on" — if "auto", power saving can kill connections

# Check for NetworkManager config
cat /etc/NetworkManager/conf.d/wifi-powersave-off.conf 2>/dev/null
```

#### 8c. Fix WiFi Power Management (Temporary)

```bash
sudo iwconfig wlp2s0 power off
# Verify: should now show "Power Management:off"
```

#### 8d. Fix WiFi Power Management (Permanent — Survives Reboot)

Create `/etc/NetworkManager/conf.d/wifi-powersave-off.conf`:

```ini
[connection]
wifi.powersave = 2
```

Where `wifi.powersave` values:
- `2` = disable power saving
- `1` = enable (default)
- `0` = use global default

Apply with:

```bash
sudo systemctl restart NetworkManager
```

Verify the fix persisted:

```bash
iwconfig wlp2s0 2>&1 | grep "Power Management"
# Should show: "Power Management:off"
```

#### 8e. Rule Out Other Causes

If the error pattern is NOT 5-minute intervals:

- **Connectivity verification**: Ping and HTTP tests should work fine (this is a long-poll issue, not a connectivity issue)
- **IPv6 vs IPv4**: Test both — some ISPs have flaky IPv6 routing:
  ```bash
  curl -4 -s -o /dev/null -w "IPv4: %{http_code} %{time_total}s\n" https://api.telegram.org --max-time 10
  curl -6 -s -o /dev/null -w "IPv6: %{http_code} %{time_total}s\n" https://api.telegram.org --max-time 10
  ```
- **System sleep/suspend**: Check if the system is suspending: `uptime`
- **NetworkManager** may reset the WiFi power state on reconnect — make sure the conf file is in place

#### 8f. Error Signature Quick Reference

| Log Pattern | Likely Cause | Action |
|-------------|-------------|--------|
| `httpx.ReadError` in tight pairs every ~306s (5.1 min) | WiFi Power Management | `iwconfig power off` + NM config |
| `httpx.ReadError` at irregular intervals | Network congestion / firewall idle timeout | Check ISP, check proxy keepalive |
| `httpx.ConnectError` (repeated every 1-15s) | DNS / network outage / bot token issue | Check `nslookup`, `ping`, token validity |
| `terminated by other getUpdates request` | Multiple polling clients | Kill conflicting processes |
| Cron job `last_status: ok` but user didn't receive delivery | Intermittent `httpx.ReadError` during send window | Check errors.log timing vs cron delivery time; WiFi power mgmt is likely cause |

### 9. Fix Common Issues

| Issue | Fix |
|-------|-----|
| Token = `***` literal | Run `hermes setup` or manually set `TELEGRAM_BOT_TOKEN=actual_token_here` in `~/.hermes/.env` |
| User needs to start chat | Tell user: "Open Telegram, search for @BotName, send 'hi'" |
| Wrong chat_id in config | Update `TELEGRAM_ALLOWED_USERS` in `~/.hermes/.env` |
| Persistent httpx.ReadError every ~5 min | Disable WiFi power management (see §8) |
| Polling conflict | Ensure only one process (gateway) is doing long-polling |
| Markdown parse error in messages | Use `parse_mode=HTML` or escape markdown chars |

## Quick Test Command
```bash
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
curl -s "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=8137891480" \
  -d "text=Test from Hermes $(date)"
```

## See Also
- `references/allowlist-debug-2026-06-07.md` — detailed debugging transcript from a real incident where both `.env` and `config.yaml` allowlists were misconfigured, including the `hermes config set` YAML quoting pitfall.
