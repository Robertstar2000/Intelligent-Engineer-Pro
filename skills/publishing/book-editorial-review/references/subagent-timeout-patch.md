# Subagent Timeout Patch (1800s / 30 minutes)

## Problem
The default subagent timeout was **600 seconds (10 minutes)**, which caused subagents to time out on large editorial fix tasks such as:
- Expanding manuscripts by 20,000+ words
- Converting HTML to markdown (LF Book 4 Waters Horizon)
- Trimming 15,000+ words from over-length books
- Converting copy-pasted placeholder text into unique content

## Solution
Patched the timeout to **1800 seconds (30 minutes)** in three locations:

### 1. `tools/delegate_tool.py` (line ~547)
```python
DEFAULT_CHILD_TIMEOUT = 1800  # seconds before a child agent is considered stuck
```

### 2. `hermes_cli/config.py` (line ~1686)
```yaml
"child_timeout_seconds": 1800,  # wall-clock timeout for each child agent
```

### 3. `cli.py` (line ~489)
```python
"delegation": {
    "max_iterations": 45,
    "model": "",
    "provider": "",
    "base_url": "",
    "api_key": "",
    "child_timeout_seconds": 1800,  # Wall-clock timeout for each child agent
}
```

## Verification
After patching, verify the timeout is active:
```bash
grep -r "1800" ~/.hermes/hermes-agent/tools/delegate_tool.py ~/.hermes/hermes-agent/hermes_cli/config.py ~/.hermes/hermes-agent/cli.py | grep -i "timeout\|child"
```

## When to Still Use Micro-Goals
Even with 1800s, for extremely large tasks (>100K words, full manuscript rewrites), still use:
- **Micro-goal delegation:** "read Ch12-13 and expand" instead of "fix whole book"
- **Batch-and-reassess:** 3 books at a time, verify after each batch
- **Fix+Review split:** Subagent does fixes only, parent writes review

## Related Files
- `book-editorial-review` skill: "Timeout Pitfall & Workaround" section
- `book-editorial-fix` skill: "Subagent Timeout Configuration" section
- `references/session-workflow-patterns.md`: Broad-to-narrow goal mapping table