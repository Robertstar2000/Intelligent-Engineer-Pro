---
name: systematic-debugging
description: "4-phase root cause debugging: understand bugs before fixing. Also covers Python pdb/debugpy, Node.js inspect, code review, simplification, and spike experiments."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation, python-debug, node-debug, code-review, refactoring]
    related_skills: [test-driven-development, writing-plans, subagent-driven-development]
---

# Systematic Debugging & Code Quality

Class-level umbrella for debugging workflows, code review, and quality processes. The core 4-phase debugging methodology is in this file; detailed tool-specific guides and workflows are in `references/`.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## The Four Phases

### Phase 1: Root Cause Investigation
- Read error messages carefully — they often contain the exact solution
- Reproduce consistently — exact steps, every time
- Check recent changes — git diff, new dependencies
- Gather evidence in multi-component systems — log at each boundary
- Trace data flow — find where the bad value originates

**Completion checklist:** Error messages read, issue reproduced, recent changes identified, evidence gathered, root cause hypothesis formed.

### Phase 2: Pattern Analysis
- Find working examples in the same codebase
- Compare against reference implementations
- Identify differences between working and broken
- Understand dependencies and assumptions

### Phase 3: Hypothesis and Testing
- Form a single specific hypothesis
- Test minimally — one variable at a time
- Verify before continuing
- If 3+ fixes failed: question the architecture, don't fix again

### Phase 4: Implementation
- Create failing test case first
- Implement single fix addressing root cause
- Verify fix — regression test + full suite
- If fix doesn't work: Rule of Three (see Phase 3)

## Red Flags — STOP and Follow Process

"Quick fix for now", "Just try changing X", "Skip the test", "It's probably X", "One more fix attempt" (after 2+ failures) — ALL mean STOP and return to Phase 1.

## DOX Integration

When debugging in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the fix affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Subsections (in `references/`)

| File | Content |
|------|---------|
| `references/python-debugpy.md` | Python debugging: pdb REPL, debugpy remote/DAP, post-mortem, pytest debugging, Hermes-specific processes |
| `references/node-inspect-debugger.md` | Node.js debugging: `node inspect` REPL, CDP scripting, attaching to running processes, Hermes TUI debugging |
| `references/simplify-code.md` | Parallel 3-agent code cleanup: reuse, quality, efficiency reviewers |
| `references/requesting-code-review.md` | Pre-commit verification: security scan, quality gates, independent reviewer subagent, auto-fix loop |
| `references/spike.md` | Throwaway experiments: decompose → research → build → verdict |
| `references/python-package-shadowing.md` | Python `.py` script shadowing package directory — diagnosis and fix |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |
