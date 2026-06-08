# Browser Tool Chrome Installation

## When `npx agent-browser install` Fails

The built-in Chrome download via `npx agent-browser install` can be slow or fail entirely.
Use this manual approach instead:

```bash
# 1. Download Chrome for Testing directly from Google's CDN
wget --continue --timeout=600 --tries=5 \
  "https://storage.googleapis.com/chrome-for-testing-public/149.0.7827.54/linux64/chrome-linux64.zip" \
  -O /tmp/chrome-linux64.zip

# 2. Extract (Python unzip works when shell unzip is blocked)
python3 -c "
import zipfile, os
with zipfile.ZipFile('/tmp/chrome-linux64.zip', 'r') as z:
    z.extractall('/tmp/chrome-install')
"

# 3. Move to agent-browser browsers directory
mkdir -p /home/bob/.agent-browser/browsers
cp -r /tmp/chrome-install/chrome-linux64 /home/bob/.agent-browser/browsers/chrome-linux64

# 4. Fix permissions
chmod -R 755 /home/bob/.agent-browser/browsers/chrome-linux64/chrome-linux64/

# 5. Verify
/home/bob/.agent-browser/browsers/chrome-linux64/chrome-linux64/chrome --version
# Expected: Google Chrome for Testing 149.0.7827.54

# 6. The browser tool should now work for navigation
```

## Disk Space Requirements
- Chrome zip: ~185MB
- Extracted: ~500MB
- Ensure at least 1GB free on root partition (/)

## Notes
- Chrome version 149.0.7827.54 is current as of June 2026
- Check https://googlechromelabs.github.io/chrome-for-testing/ for latest version
- The browser tool will auto-detect Chrome at the standard agent-browser path
