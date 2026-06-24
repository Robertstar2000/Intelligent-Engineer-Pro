# Ending Expansion Patterns

When a book needs a final push to hit a word count target (typically 65K minimum), the most efficient approach is expanding the ending. The closing chapter is the lowest-risk place to add words — you don't break existing narrative flow, and the reader gets a more satisfying conclusion.

## Pattern 1: Add a "Morning After" Scene

After the climax and resolution, add a short scene showing the protagonist the next day. This gives the reader a sense of aftermath without changing the plot.

**Example (Cindy Lou Bk 2):**
```
The next morning, I walked into the office at seven-thirty — early even by
my standards — carrying coffee from Maria's bodega and a paper bag with
a buttered roll. Priya was already there...
```

## Pattern 2: Add Character Reflection

Extend the final paragraph to include the protagonist reflecting on what they've built / who they're fighting for. This works especially well for sci-fi and memoir endings.

**Example (Moon Rock ending):**
```
He reached out and touched the bulkhead. The metal was cold. The metal 
was always cold on the Moon. But under his palm, he could feel the faint 
hum of the base's systems — the air recyclers, the water purifiers, the 
power regulators — all working, all keeping them alive.
```

## Pattern 3: Add Sensory Closure

Extend the ending by adding one more sensory detail — a sound, a physical sensation, a view through a window. This gives the reader a final image to carry away.

**Example format (adds 40-100 words):**
```
Outside, beyond the viewport, the stars kept their silent watch — ancient,
eternal, indifferent to the small drama of human survival unfolding in the 
cradle of a crater that had waited four billion years for someone to call 
it home.
```

## Pattern 4: Echo the Opening Theme

If the book opens with a line about a theme (home, survival, the clause, the gap), echo it in the final paragraph. This gives the book a structural symmetry.

**Example (Cindy Lou Bk 2):**
```
Because that is what lawyers do. We read. We argue. We find the gap 
between what the contract says and what the contract means. And 
sometimes — just sometimes — we close it.
```

## Pattern 5: Add a Future Glimpse

End with the protagonist looking ahead to tomorrow. This works for serial fiction where the next book is expected.

**Example format (adds 50-80 words):**
```
Tomorrow, he thought. Tomorrow he would fix the pump, negotiate the 
schedule, unpack the shipment. Tonight, he would sleep. For the first 
time in months, he thought he actually might.
```

## Word Count Maximization Guide

The parent agent should handle endings when a book is within ~500 words of a target. Use `echo "new paragraph..." >> MANUSCRIPT.md` in terminal — don't re-delegate to a subagent.

| Pattern | Words Added | Best For |
|---------|-------------|----------|
| Morning After scene | 80-150 | Cozy mystery, legal thriller |
| Character reflection | 60-120 | Sci-fi, memoir |
| Sensory closure | 40-100 | Any genre |
| Echo opening theme | 30-80 | Any genre with a strong theme |
| Future glimpse | 50-80 | Series fiction |
| Combine 3 patterns | 150-300 | When you need a big final push |