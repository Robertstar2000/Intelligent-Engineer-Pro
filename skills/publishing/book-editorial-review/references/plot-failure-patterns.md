# Common Plot Failure Patterns (From Iteration 3 Reviews)

## Pattern 1: Genre Breach / Identity Crisis
**Example:** No Blue Sky Book III — Space opera (aliens, FTL, extradimensional entities) in a colonization thriller series
**Detection:** Compare physics, antagonists, tech level, tone across series books
**Fix:** Rewrite to match series genre OR spin off as separate series
**Penalty:** -2 grades (genre breach = structural failure)

## Pattern 2: Sagging Middle / Act II Plateau
**Example:** No Blue Sky Book I (Part II episodic disputes); NBS Book III (Legacy Council debates Ch 5-28)
**Detection:** Middle 40% has no stakes escalation; chapters are interchangeable; could reorder without loss
**Fix:** Compress middle by 40%; add rising complications; each chapter must raise stakes
**Penalty:** -0.5 grade per sagging segment

## Pattern 3: Deus Ex Machina / Unearned Resolution
**Example:** NBS Book IV (alien signal solves nothing); LF Book 3 (signal undermines water victory)
**Detection:** Major problem solved by external force/coincidence, not character action
**Fix:** Rewrite climax so protagonist's choice/skill resolves it
**Penalty:** -1.5 grades

## Pattern 4: Dropped Plot Threads
**Example:** NBS Book V (flag ceremony 3×, celebration 2× = duplicated not resolved); AoLS Book 1 Epilogue signal vs Book 3 entities
**Detection:** Track 3 biggest mysteries from first third → verify resolved in final third
**Fix:** Either resolve or explicitly defer with "character accepts mystery"
**Penalty:** -1 grade per dropped thread

## Pattern 5: Episodic "And Then" Structure
**Example:** NBS Book IV (milestone checklist chapters); NBS Book II (formulaic template)
**Detection:** Chapters don't cause each other; same opening template repeated; no causal links
**Fix:** Rewrite with explicit cause→effect; each chapter's conflict must originate from previous
**Penalty:** -1 grade (capped at B)

## Pattern 6: Duplicate Content as Plot
**Example:** NBS Book IV (33% duplicate EVA paragraphs); NBS Book V (3 flag ceremonies, 2 celebrations)
**Detection:** Same scene/beat repeated with minor variations; word count inflated by repetition
**Fix:** Keep ONE canonical version; rewrite others as original consequences
**Penalty:** -1 grade per major duplication

## Pattern 7: Undermining Own Climax
**Example:** LF Book 3 — alien signal epilogue negates hard-won water sovereignty victory
**Detection:** Epilogue or final chapter introduces element that makes climax feel pointless
**Fix:** Epilogue must extend/hook, not negate; signal = mystery, not solution
**Penalty:** -1 grade

## Pattern 8: Formulaic Chapter Template
**Example:** NBS Book II — "alert came as... adjusted spectacles... Mission AI data dump" ×10
**Detection:** Same opening structure, same Mission AI dialogue pattern, same character beat repeated
**Fix:** Vary openings; each chapter needs unique hook, conflict, revelation
**Penalty:** -0.5 per template occurrence beyond 2

## Detection Commands

```bash
# Check for formulaic openings
grep -n "alert came as" MANUSCRIPT.md
grep -n "adjusted his spectacles" MANUSCRIPT.md

# Check for duplicate phrases
grep -oP '.{0,50}regolith underfoot.{0,50}' MANUSCRIPT.md | sort | uniq -c | sort -rn

# Check cause→effect: consecutive chapter conflicts
grep -n "^## Chapter" MANUSCRIPT.md | while read line; do echo "$line"; done

# Track plot threads
grep -n "alien signal\|oxygen crisis\|charter\|independence" MANUSCRIPT.md | head -20
```

## Verification Checklist (Per Review)

- [ ] Trace 3 main plot threads: setup → middle → climax → resolution
- [ ] Verify each segment's "Link to Next" is specific and causal
- [ ] Check stakes escalate: Act I < Act II < Act III < Climax
- [ ] No segment has "and then" structure — all are "therefore/but"
- [ ] Subplots appear in ≥2 segments and intersect main plot
- [ ] Ending is surprising AND inevitable (retrospectively obvious)
- [ ] No deus ex machina — protagonist's agency resolves climax
- [ ] No dropped threads from first third