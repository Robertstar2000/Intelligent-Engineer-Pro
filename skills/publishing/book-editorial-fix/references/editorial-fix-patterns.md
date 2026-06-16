# Editorial Fix Patterns (From Iteration 3)

## Plot Coherence Fixes

### Fix: Broken Cause→Effect Chain
**Pattern:** Chapter N event doesn't cause Chapter N+1; "and then this happened"
**Fix:**
1. Identify the 3 main plot threads
2. For each break, write a bridging scene or revise chapter ending
3. Ensure each segment's "Link to Next" in Plot Map is specific and causal

### Fix: Sagging Middle (Act II Plateau)
**Pattern:** Middle 40% has flat stakes; chapters reorderable without loss
**Fix:**
1. Compress middle by 30-40% (cut filler, merge scenes)
2. Add rising complication every 2-3 chapters
3. Each chapter must raise personal AND public stakes

### Fix: Deus Ex Machina Resolution
**Pattern:** External force/coincidence solves climax; protagonist passive
**Fix:**
1. Identify what protagonist COULD do to resolve
2. Rewrite climax with protagonist's agency/choice/skill as driver
3. External forces can create the problem; protagonist must create the solution

### Fix: Dropped Plot Threads
**Pattern:** Mystery/conflict introduced in first third, ignored by final third
**Fix:**
1. List 3 biggest setups from first third
2. For each: either resolve in climax, or add "character accepts mystery" beat
3. Update Plot Map resolution status for each thread

### Fix: Episodic "And Then" Structure
**Pattern:** Chapters don't cause each other; same opening template repeated
**Fix:**
1. Audit consecutive chapters: does Chapter N's ending force Chapter N+1?
2. Rewrite chapter transitions with explicit causal links
3. Vary openings — unique hook, conflict, revelation per chapter

## Structural Rewrite Patterns

### Pattern: Complete Structural Rewrite (Type R)
**When:** Uniqueness ratio <15%, 10+ placeholder matches, cross-book leaks >2
**Process:**
1. Backup: `cp MANUSCRIPT.md MANUSCRIPT.md.BEFORE_REWRITE`
2. Identify salvageable chapters (typically last 20-30%)
3. Design new chapter structure around actual theme
4. Write entire manuscript via `write_file()` (NOT patch)
5. Integrate salvageable chapters with renumbering
6. Add Plot Map, Character Map, front/back matter inline

### Pattern: Duplicate Content Consolidation
**When:** Same scene/beat repeated 2-3× with minor variations
**Fix:**
1. Identify canonical version (usually first or most complete)
2. Remove all other versions
3. If variations add value, integrate as single enriched scene
4. Update Plot Map — one entry per structural beat

### Pattern: Formulaic Chapter Template
**When:** Same opening structure repeated 5+ times
**Fix:**
1. Audit first 100 words of each chapter
2. Categorize template components (alert type, character action, AI dialogue)
3. Rewrite each chapter with unique combination:
   - Ch 1: Crisis alert + personal stakes + AI warning
   - Ch 2: Discovery + character conflict + AI analysis
   - Ch 3: Decision point + moral dilemma + AI projection
   - etc.

## Character Consistency Fixes

### Fix: Name/Identity Drift
**Pattern:** Same character different names across books/chapters
**Process:**
1. Build Character Map from CHARACTER_MAP.md
2. `grep -n` every name variant
3. `patch(replace_all=True)` for systematic fixes
4. Verify: old count = 0, new count = expected total

### Fix: Pronoun Chaos
**Pattern:** Singular character referred as "they/their" inconsistently
**Fix:**
1. Determine canonical pronouns per Character Map
2. Search all variants: `grep -ni "they\|their\|them" MANUSCRIPT.md`
3. Context-aware replace (not blind — check each occurrence)

## Plot Map Verification During Fixes

After ANY fix pass, audit against Plot Map:

```bash
# 1. Verify chapter count matches Plot Map segments
grep -c "^## Chapter\|^# Chapter" MANUSCRIPT.md

# 2. Check each Plot Map segment has content
# 3. Verify cause→effect links exist in text
# 4. Check resolution status matches actual ending

# Quick cause→effect check:
for i in {1..39}; do
  echo "=== Ch $i end ==="
  sed -n "/^## Chapter $i /,/^## Chapter $((i+1)) /p" MANUSCRIPT.md | tail -5
done
```

## Non-Fiction Specific Fixes

### Fix: Duplicate Chapter Versions
**Pattern:** Every chapter appears twice (long-form + short-form)
**Fix:**
1. Identify which version is canonical (usually long-form with case studies)
2. Remove all short-form duplicates
3. Verify: 1 "The One Thing" per chapter, 12 chapters total

### Fix: Appendix Overwhelms Main Text
**Pattern:** Appendix = separate book (16-agent system)
**Fix:**
1. Extract appendix to companion file: `COMPANION.md`
2. Add integrated reference table in main text (8 key agents → chapters)
3. Update back matter with link to companion

### Fix: Descriptive Chapter Headers
**Pattern:** "Why Most Lead Scoring Is Guesswork" (descriptive, not provocative)
**Fix:** Rewrite as claim reader wants to verify:
- "The 400-Lead Fiasco That Almost Bankrupted Our Sales Team"
- "The $80,000 Mistake: Three Gates That Stop the Bleeding"

## Verification Commands

```bash
# Word count
wc -w MANUSCRIPT.md

# Chapter count
grep -c "^## Chapter\|^# Chapter" MANUSCRIPT.md

# Check for template phrases
grep -i "regolith underfoot\|work required patience\|equipment hummed" MANUSCRIPT.md

# Check for duplicate phrases
grep -oP '.{0,80}regolith underfoot.{0,80}' MANUSCRIPT.md | sort | uniq -c | sort -rn

# Verify Plot Map segments have content
# (manual: check each segment in Plot Map has corresponding chapters)

# Character name audit
grep -c "CanonicalName" MANUSCRIPT.md  # should match expected
grep "OldName" MANUSCRIPT.md           # should be 0
```