# Telegram Allowlist Debugging — Session Notes (2026-06-07 / 2026-06-14)

## Root Cause
`TELEGRAM_ALLOWED_USERS=n` in `~/.hermes/.env` was blocking ALL incoming Telegram messages.
The `config.yaml` `telegram.allowed_chats` was also misconfigured as a quoted string `'[8137891480]'`.

## Error Signature
```
WARNING gateway.run: Unauthorized user: 8137891480 (Robert Mills) on telegram
```
Appears on EVERY incoming message when the allowlist doesn't include the sender's chat ID.

## Debugging Steps That Worked

1. **Check both config locations:**
   ```bash
   grep "allowed_chats" ~/.hermes/config.yaml
   grep "TELEGRAM_ALLOWED_USERS" ~/.hermes/.env
   ```

2. **Fix `.env` (legacy gate):**
   ```bash
   sed -i "s/TELEGRAM_ALLOWED_USERS=.*/TELEGRAM_ALLOWED_USERS=<chat_id>/" ~/.hermes/.env
   ```

3. **Fix `config.yaml` (active gate) — DO NOT use `hermes config set`:**
   ```bash
   # WRONG — produces quoted string:
   # hermes config set telegram.allowed_chats "8137891480"
   # Result: allowed_chats: '[8137891480]'  ← broken

   # RIGHT — edit YAML directly:
   sed -i "s/allowed_chats:.*/allowed_chats: [<chat_id>]/" ~/.hermes/config.yaml
   ```

4. **Restart and verify:**
   ```bash
   hermes gateway restart
   sleep 8
   journalctl --user -u hermes-gateway --since "1 minute ago" --no-pager
   # Should show NO "Unauthorized user" errors
   ```

5. **Test delivery:**
   ```bash
   TOKEN=*** '^TELEGRAM_BOT_TOKEN=*** ~/.hermes/.env | cut -d= -f2-)
   curl -s "https://api.telegram.org/bot${TOKEN}/sendMessage" \
     -d "chat_id=<chat_id>" \
     -d "text=Test $(date)"
   ```

## Additional Context
- Gateway PID was in a restart loop (start→stop→start) until both allowlists were fixed
- After fix: gateway stabilized, `send_message` returned successfully with message_id
- The `GATEWAY_ALLOW_ALL_USERS=true` in `.env` was also present but didn't override the `TELEGRAM_ALLOWED_USERS=n` gate

## 2026-06-14 Session — Additional Observations

### Gateway Restart Behavior
- When the gateway does a "planned restart" (triggered by Desktop app or systemd), it launches a helper process:
  ```
  /bin/sh -lc while kill -0 <pid> 2>/dev/null; do sleep 0.2; done; systemctl --user reset-failed hermes-gateway; systemctl --user restart hermes-gateway
  ```
- During restart, Telegram connections go to CLOSE-WAIT. The gateway reconnects within ~15 seconds.
- The old PID logs a final "Gateway stopped" message before the new PID takes over.

### Telegram Flood Control
- After a polling conflict (two sessions hitting the same bot), Telegram imposes a ~264s rate limit
- The gateway logs `Telegram flood control, waiting 264.0s` and retries automatically
- Recovery is automatic but slow — user sees ~4 minutes of unresponsiveness

### Network Resilience
- Transient `api.telegram.org` connection failures were observed (June 12 05:27)
- Fallback IP `149.154.166.110` was also unreachable during that window
- Connection recovered on its own — no manual intervention needed
- Current connectivity test: `curl -4 -s https://api.telegram.org` → HTTP 302 in ~0.4s (normal)

### Desktop App GPU Crash (unrelated to gateway)
- Hermes Desktop (Electron) crashes with `GPU process launch failed: error_code=1002`
- `--disable-gpu` alone was insufficient
- Does NOT affect the gateway (separate process) but does cause gateway restart when Desktop triggers systemd planned-restart
