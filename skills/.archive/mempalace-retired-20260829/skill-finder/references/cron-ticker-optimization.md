# Cron Ticker Optimization: auto_nap() Pattern

## Problem

The default cron ticker calls `tick()` every 60 seconds even when no jobs are due. Each tick:
- Acquires a file lock
- Loads all jobs from `jobs.json`
- Filters to due jobs (usually zero)
- Releases the lock

This wastes CPU cycles during idle periods, especially on shared hosting or low-power devices.

## Solution: Adaptive Ticker

Replace the fixed-interval ticker with an adaptive one that extends the sleep interval during idle time.

### Behaviour

| State | Tick Interval | Trigger |
|-------|:-------------:|---------|
| **Normal** | 60 seconds | User activity within last 10 minutes |
| **Idle** | 30 minutes | No user activity for 10+ minutes |
| **Reset** | Immediate | Any inbound user message from any gateway |

### Implementation

See `auto_nap()` function in `gateway/run.py`. Key design decisions:

1. **Shared activity tracker** — Module-level `_cron_activity` dict with `threading.Lock()`:
   ```python
   _cron_activity: dict = {
       "last_activity_ts": time.time(),
       "lock": threading.Lock(),
   }
   ```

2. **Activity recording** — Call `_record_cron_activity()` from `_handle_message()` (and any other inbound entry point) for all non-internal events:
   ```python
   if not is_internal:
       _record_cron_activity()
   ```

3. **Adaptive interval** — Normal 60s, idle 30min, resets on user input

4. **Wall-clock house-keeping** — Channel directory refresh, image cache cleanup, paste sweep, and curator poll use `time.time()` differences instead of tick counts, so cadences stay correct regardless of tick mode.

5. **Back-compat alias** — `_start_cron_ticker = auto_nap` keeps existing code working.

### Token Reduction via Skills Disabled List

Disabling unused skills reduces system prompt size significantly:

```yaml
# config.yaml
skills:
  disabled:
    - ml-skill-1
    - ml-skill-2
    # ...
```

Current: 90 disabled skills → ~3,634 tokens (down from ~5,704, saving ~36%)

**Editing the disabled list safely:**
```python
import yaml
with open(os.path.expanduser('~/.hermes/config.yaml')) as f:
    cfg = yaml.safe_load(f)
cfg['skills']['disabled'] = ['skill-a', 'skill-b']  # proper list
with open(os.path.expanduser('~/.hermes/config.yaml'), 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
```

**Do NOT use `hermes config set` with JSON strings** — it mangles the YAML and creates 1500+ fragments.

### Related Skills
- `skill-finder` — find/search skills, check status, re-enable
- Weekly cron job (ID: bcd209af7131) scans for new skills every Sunday 9am
