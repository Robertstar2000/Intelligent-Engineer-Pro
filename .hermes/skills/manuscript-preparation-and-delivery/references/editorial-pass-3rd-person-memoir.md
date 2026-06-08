# Editorial Pass Checklist for 3rd-Person Memoir Manuscripts

Run this checklist after any content merge or before final delivery of a 3rd-person memoir manuscript.

## 1. Verb Tense: "Bob would [verb]" → "Bob had [verb]"

A common pattern in AI-drafted 3rd-person narratives is using "would" where simple past or past perfect is correct. Search for these and fix:

| Wrong | Right |
|-------|-------|
| Bob would ordered | Bob had ordered / Bob ordered |
| Bob would learned | Bob had learned |
| Bob would said | Bob had said |
| Bob would had | Bob had |
| Bob would gotten | Bob had gotten |

Search regex: `Bob would (ordered|learned|said|had|gotten|taken|made|done|seen|known|built|begun)`

## 2. POV First-Person Residue

When converting from 1st to 3rd person, residual first-person pronouns often survive:

| Search Pattern | Fix |
|---------------|-----|
| `from mine` | from his |
| `of mine` | of his |
| `curved away from mine` | curved away from his |
| `inches from mine` | inches from his |
| `Everything after is mine` | Everything after is his |
| `Bob am writing` | I am writing (if in letters/quotations) |

## 3. Verb Agreement (3rd Person Singular)

In 3rd person, Bob = "he" = third person singular:

| Wrong | Right |
|-------|-------|
| Bob carry | Bob carries |
| Bob know | Bob knows |
| Bob have | Bob has |
| Bob remember | Bob remembers |
| Bob discover | Bob discovers |
| Bob wish | Bob wishes |
| Bob wonder | Bob wonders |

Search regex: `Bob (carry|know|have|remember|discover|wish|wonder)( |\.|\,|\!)` but NOT `Bob (will|could|would|should|may|might|can|must|did|does)` followed by the verb (those are auxiliary verbs).

## 4. Speling Typos

Common typos found in drafts:
- `remembereded` → `remembered`
- `rudendent` → `redundant`
- `predigest` → `prejudice`
- `his mine` → `his`
- `Bob would had` → `Bob had`

Search: `remembereded`, any doubled suffix after -ed.

## 5. Duplicate Content Detection

### Duplicate Transitions
AI writing systems sometimes produce duplicate transition paragraphs between sections. Look for:
- `Transition: From X to Y` appearing twice
- Different version of same transition (one with a missing word)

### Redundant Story Sections
When new user-contributed content is merged into an existing manuscript, check if it duplicates existing chapters:
- Compare new section summaries with existing chapter summaries
- Look for the same story events / anecdotes / character introductions
- The user-provided section may expand on something already covered

## 6. Duplicate Section Removal

When removing a duplicate section (e.g., a "Plenty of Fish / Then He Met Her" section that duplicates Chapter 9), use Python to find and remove:

```python
# Find section boundaries
fish_start = content.find("### The Singles club")
then_met = content.find("### Then He Met Her")
ch10_start = content.find("Chapter Ten:")
# Remove from fish_start to just before ch10_start
new_content = content[:fish_start] + content[ch10_start:]
```

Always verify by checking the number of remaining chapter headings equals 16 (for a standard memoir structure).

## 7. Front Matter to Add

Before final delivery, ensure these pages exist:
- **Copyright & Disclaimer page** (with AI disclosure if applicable)
- **Acknowledgments** (family, partners, children, grandchildren)
- Verify they appear after the title/subtitle/author lines and before Part One

## 8. Final Verification

```bash
# Count grammar fixes applied
grep -c "would \(ordered\|learned\|said\|had\|gotten\)" manuscript.md  # should be 0

# Count first-person residue
grep -c "from mine\|of mine\|curved away from mine" manuscript.md  # should be 0

# Count remembereded typos
grep -c "remembereded" manuscript.md  # should be 0

# Count chapter headings
grep -c "^Chapter " manuscript.md  # should match expected count
```

## 9. Chapter Transitions

Check that each chapter ends with a paragraph that:
- Reflects on the chapter's events
- Hints at what comes next
- Does NOT use templated AI transition patterns like:
  - "Leaving behind X and turning toward Y, I inhabited a mental landscape..."
  - "creative tension between memory and possibility"
  - "my mind rested in a space of integration"
  - "memories blend with anticipation"
  - "psychological threshold"

Remove any such patterns and replace with a simple closing paragraph or section break.