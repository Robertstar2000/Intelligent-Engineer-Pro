# Firefox Remote Debugging Incompatibility

## Issue
Firefox's `--remote-debugging-port` flag does NOT expose a Chrome DevTools Protocol (CDP) endpoint. Instead, it serves `httpd.js` — a simple static file server built into Firefox.

## Symptoms
- `curl http://127.0.0.1:<port>/json/version` returns 404
- `curl http://127.0.0.1:<port>/` returns an HTML page titled "httpd.js"
- `browser-harness` fails with "is the dedicated automation Chrome running?"
- Built-in browser tools (`browser_navigate`, `browser_snapshot`, `browser_click`) return empty/404

## Root Cause
Firefox uses the Mozilla DevTools Protocol (DWP/Remote Debugging Protocol), which is entirely different from Chrome's CDP. The two protocols are not interoperable.

## Solutions
1. **Use the headless Chromium session** (already configured on the server at `BU_CDP_URL=http://127.0.0.1:9222`)
2. **Ask the user to log into the target site in the headless Chromium browser** (share credentials once)
3. **Use `mozprofile`/`mozrunner`** Python libraries — but these are not installed by default and the built-in tools won't use them
4. **Use Playwright with Firefox** (`npx playwright install firefox`) — but this requires reconfiguration of the browser toolchain

## Do NOT
- Repeatedly try different ports on Firefox — none will expose CDP
- Tell the user "enable CDP in Firefox" — it doesn't exist
- Claim the browser tools "don't work" — they work fine with Chrome/Chromium
