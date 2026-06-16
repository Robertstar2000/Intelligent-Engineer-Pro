# Massive Expansion Pattern: 20K -> 50K Words

## When to Use

When a book is severely underlength (20-30K words) and needs to reach the 50K target for a full-length novel.

## Strategy

1. Identify weak chapters (under 1,000 words or summary-like)
2. Rewrite weakest chapters from scratch (2,000-3,000 words each)
3. Expand remaining weak chapters with new scenes (1,000-2,000 words each)
4. Multiple passes: 3-5 passes, each adding 4-6K words
5. Verify after each pass: wc -w and chapter distribution

## Key Pitfalls

1. Delegate_task timeout: Always ~600s. Use terminal scripts for large expansions.
2. Python string size limits: Use terminal heredoc for large content, not write_file string literals.
3. Duplicate content: Strip trailing --- separators before appending expansions.
4. Chapter numbering: Maintain sequential numbering when replacing chapters.

## Real Example: NBS Book V

Starting: 23,223 words / 22 chapters (1,055 avg)
Target: 50,000 words (2,272 avg)

8 expansion passes over multiple sessions. Each pass adds 2-7K words.
Plan for 5-8 passes to go from 23K to 50K.

## Genre-Specific Expansion Content

Martian Colonization Epic:
- Faction debate scenes with dialogue
- Dust storm / environmental crisis scenes
- Personal stakes (family, relationships, sacrifice)
- Sensory detail (smells, sounds, textures of Mars)
- Political maneuvering and negotiation scenes
- Character internal monologue showing emotional weight

Use humanizer skill to strip AI-isms. Use genre benchmarks from book-editorial-review.
Ensure each chapter ends with a reason to keep reading. Vary sentence rhythm.
