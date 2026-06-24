# Hermes Desktop — GPU Crash Workaround

## Problem
The Hermes Desktop Electron app crashes on launch with:
```
GPU process launch failed: error_code=1002
FATAL:content/browser/gpu/gpu_data_manager_impl_private.cc:415] GPU process isn't usable. Goodbye.
```

This happens on machines without proper GPU drivers or with certain kernel/graphics configurations (e.g., NVIDIA driver 535 on kernel 6.8).

## Fix
Launch with GPU disabled:
```bash
/home/bob/.hermes/hermes-agent/apps/desktop/release/linux-unpacked/Hermes \
    --no-sandbox --disable-gpu --disable-software-rasterizer
```

A launcher script is available at `/tmp/launch-hermes-desktop.sh`.

## Also Required: Chrome Sandbox
The first launch may also fail with:
```
Failed to configure Electron's Linux sandbox helper: chrome-sandbox
```
This requires root to set the setuid bit on chrome-sandbox. If sudo is unavailable, `--no-sandbox` works as a fallback (less secure but functional).

## Desktop + Gateway Interaction
The Desktop app connects to the gateway via WebSocket. If the gateway is running but the Desktop shows no connection:
1. Check gateway is running: `hermes gateway status`
2. Check the gateway log for WebSocket errors
3. The Desktop reads gateway URL from `~/.hermes/config.yaml` — ensure `gateway` section has correct host/port
