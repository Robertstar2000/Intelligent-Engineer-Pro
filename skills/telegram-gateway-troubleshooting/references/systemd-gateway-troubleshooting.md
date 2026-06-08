# Hermes Gateway — Systemd Service Troubleshooting

## Gateway Starts Then Dies After ~30 Seconds (SIGKILL)

**Symptom**: `systemctl status hermes-gateway` shows `Active: failed (Result: signal)` or `code=killed, status=9/KILL`

**Cause**: `TimeoutStopSec` too short. The gateway's drain timeout needs >= 90s but the systemd unit has 60s.

**Diagnose**:
```bash
grep TimeoutStopSec /etc/systemd/system/hermes-gateway.service
grep TimeoutStopSec ~/.config/systemd/user/hermes-gateway.service
```

**Fix**:
```bash
# System-level service (requires sudo)
sudo sed -i 's/TimeoutStopSec=60/TimeoutStopSec=120/' /etc/systemd/system/hermes-gateway.service
sudo systemctl daemon-reload

# User-level service
sed -i 's/TimeoutStopSec=60/TimeoutStopSec=120/' ~/.config/systemd/user/hermes-gateway.service
systemctl --user daemon-reload
```

## Two systemd Services Fighting

Both `/etc/systemd/system/hermes-gateway.service` (system) and `~/.config/systemd/user/hermes-gateway.service` (user) may exist. Disable the system-level one:

```bash
sudo systemctl stop hermes-gateway
sudo systemctl disable hermes-gateway
systemctl --user enable hermes-gateway
systemctl --user start hermes-gateway
systemctl --user status hermes-gateway
```

## "Gateway drain timed out after 60.0s with 1 active agent(s)"

An active agent session is blocking gateway start. Kill stale processes:

```bash
ps aux | grep -i "hermes\|telegram" | grep -v grep
# Kill stale PIDs manually
```

## Verify Telegram Connection

```bash
# From the Hermes CLI, send a test message:
# send_message(target="telegram:Robert Mills (dm)", message="Gateway test")
```

Or directly:
```bash
TOKEN=$(grep '^TELEGRAM_BOT_TOKEN=' ~/.hermes/.env | cut -d= -f2-)
curl -s "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d "chat_id=8137891480" \
  -d "text=Gateway test $(date)"
```
