# Cross-Book Duplication Patterns

Detecting and fixing content that is shared/copied across multiple books in the same series.

---

## 1. Opening Paragraph Identity

Two or more books in the same series share the exact same opening paragraph.

**Detection:**
```bash
# Extract first 3 lines of each book's MANUSCRIPT.md
for book in Book_*; do
  echo "=== $book ==="
  head -3 "$book/MANUSCRIPT.md"
done

# Direct comparison
diff <(head -5 Book_IV/MANUSCRIPT.md) <(head -5 Book_V/MANUSCRIPT.md)
# If diff returns nothing, openings are identical
```

**Real example from No Blue Sky:** Books IV and V both opened with: *"The monitor flickered, casting blue light across the huddle of exhausted faces. No one spoke. No one needed to. The numbers told the story..."* — verbatim identical.

**Fix:** Delete the shared opening from all but one book and write original opening hooks for each.

---

## 2. Shared Placeholder Text Blocks

Generic, template-generated paragraphs appearing identically in multiple books.

**Common AI-generated placeholder patterns:**
- *"The work required patience and precision — qualities that had been tested to their limits over the long months of the mission. Every movement mattered, every decision carried weight..."*
- *"The equipment hummed softly in the background, a constant reminder of the technology that kept them alive..."*
- *"The silence of the habitat was broken only by the steady hum of life support systems..."*
- *"We've come too far to fail now... whatever it takes, whatever we have to sacrifice..."*

**Detection:**
```bash
# Find the longest repeated block — look for paragraphs >20 words appearing identically in 2+ books
for phrase in "work required patience and precision" "equipment hummed softly" "silence of the habitat" "come too far to fail"; do
  echo "=== Checking: $phrase ==="
  for book in Book_*; do
    count=$(grep -c "$phrase" "$book/MANUSCRIPT.md" 2>/dev/null || echo 0)
    echo "  $book: $count matches"
  done
done
```

**Real example from No Blue Sky:** "The work required patience and precision" appeared 7+ times in Book IV and 8+ times in Book V. The drill-core scene ("The drill bit sang into the regolith...") appeared identically in both books. Books IV and V also shared the identical pandemic-fragment ("This doesn't make sense, Marcus") and the identical habitat-silence paragraph.

**Fix:** Delete all instances from all books. Write unique replacement content for each book that uses the book's specific characters, setting, and stakes.

---

## 3. Same Scene Structure Repeated as Chapter Template

Every chapter in a book following the exact same sequence of beats.

**Detection:**
```bash
# Look for the opening phrase pattern that signals a template
# For example, every chapter starting with "The alert came not as a crisis siren, but as a [X]"
grep -c "^The alert came" Book_II/MANUSCRIPT.md
# If >30, the book likely has template repetition

# Check for character ritual repetition
grep -c "adjusted.*spectacles.*familiar weight.*decades" Book_II/MANUSCRIPT.md
grep -c "ventilation shafts" Book_II/MANUSCRIPT.md
grep -c "her great-grandfather\|his great-grandfather\|her grandfather\|his grandfather" Book_II/MANUSCRIPT.md
```

**Real example from No Blue Sky:** Books I-II's present-day chapters followed this exact template every time:
1. An "alert" arrives on someone's console
2. A Mission AI quote of generational contrast ("Your grandparents feared X. You fear Y")
3. Someone "adjusted their spectacles, the familiar weight of decades spent in recycled air"
4. Mission AI reports statistics in "analytical yet engaged" tone
5. Character calls Kaito Varga
6. A generational ancestor's story is recalled
7. Character gives a public speech with identical rhetorical structure
8. A child's voice "drifted through the ventilation shafts"

This pattern repeated across ALL 21 present-day chapters in Book I and ALL 44 chapters in Book II.

**Fix:** Identify the fixed beats (e.g., 8 beats above). Vary at least 5 of the 8 per chapter. Some chapters should omit certain beats entirely. Not every chapter needs a Mission AI quote. Not every chapter needs a call to the leader. Not every chapter needs a child's voice in the vents.

---

## 4. Character Name Inconsistency Across Books

The same protagonist has a different name in different series entries.

**Detection:**
```bash
# Check the protagonist name used in each book
for book in Book_*; do
  first100=$(head -100 "$book/MANUSCRIPT.md")
  echo "=== $book ==="
  # Common name patterns: "Elena" variants
  echo "$first100" | grep -oP '(Elena\s+\w+|Dr\.\s+\w+\s+\w+)' | sort -u | head -5
  # Author name
  grep -i "^by " "$book/MANUSCRIPT.md" | head -1
  grep -i "bob" "$book/MANUSCRIPT.md" | head -3
done
```

**Real example from No Blue Sky:**
- Book I: "Elena Varga" (author: "Bob N.")
- Book IV: "Elena Vargas" (author: "Bob Mills")
- Book V: "Dr. Elena Chen" (author: "Bob Mills")
- Three different names for what is clearly the same protagonist across the series.

**Fix:** Freeze one canonical name for the protagonist. Search-and-replace across all books to enforce consistency. Update the author byline to one name across all series entries.

---

## 5. Genre Incompatibility Between Series Books

A book in the middle of a series is a different genre from the books before and after it.

**Detection:**
```
Compare the genres of each book in the series. Key signals:
- Technology base: does Book 3 introduce sub-quantum skipping when Books 1-2 used conventional physics?
- AI entity: does Book 3 replace Mission AI with UNIT-7 with no explanation?
- Scope: does Book 3 escalate from colony politics to galaxy-spanning crisis?
- Characters: does Book 3 drop all established POV characters and introduce entirely new ones?
```

**Real example from No Blue Sky:** Books I-II are political Mars-colony dramas (sovereignty, infrastructure, diplomacy, betrayal). Book III is an alien first-contact thriller (sub-quantum signals, interdimensional races, galactic gateways, chitin-and-tentacle imagery). The two genres are incompatible in the same series.

**Fix:** Either (a) spin Book III off into its own series and write a proper Book III that continues the political arc, or (b) retrofit Books I-II with foreshadowing of the alien contact and rewrite Book III to connect characters and technology from Books I-II.

---

## 6. Supplementary Chapter Content Cross-Contamination

Chapters or scene fragments that were clearly written for one book but accidentally included in another.

**Detection:**
```bash
# Look for character names from one book appearing in another where they don't belong
grep -c "Marcus" Book_IV/MANUSCRIPT.md   # Character from a different book's fragment
grep -c "Marcus" Book_V/MANUSCRIPT.md    # Same fragment
grep -c "pandemic\|airborne\|incubation" Book_IV/MANUSCRIPT.md  # Out-of-genre content
grep -c "pandemic\|airborne\|incubation" Book_V/MANUSCRIPT.md  # Same fragment
```

**Real example from No Blue Sky:** Both Books IV and V contain the identical fragment: *"This doesn't make sense," Marcus said. He'd been staring at the same screen for seven hours, and the numbers still refused to align. "The spread pattern suggests an airborne vector, but the incubation period is wrong."* This is a pandemic-investigation scene fragment from an unrelated story that was included in both manuscripts.

**Fix:** Delete the fragment from both books. Replace with content relevant to the book's actual narrative.

---

## Impact on Rating

| Pattern Found | Rating Impact |
|---------------|---------------|
| 2+ books share the same opening paragraph | -1 full letter grade per affected book |
| Shared placeholder text blocks (3+ identical paragraphs) | -1 full letter grade per book |
| Formulaic chapter template (30+ chapters following same 8-beat structure) | -1 full letter grade |
| Three different character names across series | -1.5 letter grades per affected book |
| Genre incompatibility between series entries | -1 letter grade for the outlier book |
| Cross-contaminated scene fragments | -0.5 letter grade per fragment |