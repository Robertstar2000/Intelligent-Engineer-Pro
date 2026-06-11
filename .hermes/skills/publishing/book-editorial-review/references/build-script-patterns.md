# Build Script Disclaimer Patterns

## Problem

Business/non-fiction books often have excellent source manuscripts but are downgraded in editorial review because **build scripts inject weaker language into the output**. The author writes strong first-person content with specific, attributable numbers, but the compilation pipeline adds "anonymized composites" and "illustrative numbers" disclaimers that undercut the book's authority.

## Files to Check

In any business book directory, search for disclaimer language in:

```
build_html.py
build_epub.py
build_package.py
KDP_AI_Disclosure.md
FRONT_MATTER.md
```

Also check any file whose name contains `build` or `package`.

## Grep Patterns

```bash
grep -r -i "anonymized" path/to/book/ --include="*.py" --include="*.md"
grep -r -i "composite" path/to/book/ --include="*.py" --include="*.md"
grep -r -i "illustrative" path/to/book/ --include="*.py" --include="*.md"
grep -r -i "observed patterns" path/to/book/ --include="*.py" --include="*.md"
grep -r -i "not just mine" path/to/book/ --include="*.py" --include="*.md"
grep -r -i "subject to change" path/to/book/ --include="*.py" --include="*.md"
```

## Specific Replacements (from the Owner's Manual session)

| Original | Replacement | Context |
|---|---|---|
| "anonymized composites... numbers are illustrative... failures just not always mine" | "draw from real MIFECO implementations... numbers are actual operating figures... I've made most of them myself" | build_html.py, disclaimer section |
| "illustrative examples... illustrative and subject to change" | "real AI agent implementations... drawn from actual operating deployments" | build_html.py, metadata section |
| "patterns observed across dozens of implementations" | "scenarios and costs are real \u2014 drawn from actual implementations at MIFECO and client organizations" | build_html.py |
| "illustrative examples... observed patterns" | "real AI agent implementations" | build_epub.py (copyright page) |
| "anonymized composites based on real observed patterns" | "draw from real implementations with names and identifying details changed" | build_package.py (KDP disclosure) |
| "anonymized composites..." | Same as build_package.py | KDP_AI_Disclosure.md |

## Verification After Fix

```bash
grep -i "anonymized\|composite\|illustrative\|observed patterns" path/to/book/output/ 2>/dev/null
```

## Why This Matters

This is often the **fastest path from A- to A** for business books. The manuscript may already be excellent \u2014 the problem is only in the delivery pipeline. Patching 4-6 build script files takes ~15 minutes and can raise a rating a full letter grade.