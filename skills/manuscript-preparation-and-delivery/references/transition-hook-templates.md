# Transition Hook Templates for Multi-Volume Series

Every book in a multi-volume series needs two transition hooks:
1. **First chapter opening** — recalls the previous book's ending and establishes continuity
2. **Last chapter closing** — sets up the next book's premise without spoiling it

## First Chapter Opening Templates

### After a political/crisis ending (Book N follows a resolution)
```
<p class="first-para">The [settlement/colony/council] had [achieved/resolved/survived] the [crisis/conflict/election], but the scars ran deeper than anyone wanted to admit. [Character] had thought the hard part was over. She was wrong.</p>
```

### After an alien contact/first contact ending
```
<p class="first-para">Before the signals from deep space, before the [event], before any of the great events that would reshape humanity's future, there was a single [document/decision/moment]. This is the story of how it all began.</p>
```

### Time jump opener (years have passed)
```
<p class="first-para">[Number] years had passed since [the event]. The [base/colony/settlement] that had begun as a [description] had grown into something more — a community, a home, a foothold. But the challenges ahead would dwarf everything that had come before.</p>
```

## Last Chapter Closing Templates

### Forward-looking (next book is a different storyline)
```
<p class="scene-break">* * *</p>
<p>The [council/team/colony] had made their decisions, cast their votes, charted their course. But as [Character] looked out at the [landscape/stars/horizon], she felt the weight of something new pressing against her consciousness — [a tremor / a signal / a premonition] that she couldn't quite identify.</p>
<p>Far below/above/beyond, [something was stirring / instruments stirred / patterns emerged] that defied explanation. Something was out there. Something was [listening / waiting / approaching].</p>
<p>[Series name] would continue in [Next Book Title].</p>
```

### Same-storyline continuance
```
<p class="scene-break">* * *</p>
<p>The [crisis/event] had been [resolved/averted/survived], but not without cost. The [colony/team] had learned hard lessons about [theme], and those lessons would echo forward, shaping everything that came next.</p>
<p>The next chapter awaited in [Next Book Title].</p>
```

## Insertion Code

```python
# First chapter: insert after the </h1> 
ch_start = html.find('<h1 class="chapter-title"')
if ch_start >= 0:
    h1_end = html.find('</h1>', ch_start)
    if h1_end >= 0:
        html = html[:h1_end+5] + '\n' + transition_text + html[h1_end+5:]

# Last chapter: insert before back-matter
back_start = html.find('class="back-matter"')
if back_start < 0:
    back_start = html.find('<h1>About')
if back_start >= 0:
    last_p = html[:back_start].rfind('</p>')
    if last_p >= 0:
        html = html[:last_p+4] + '\n' + transition_text + html[last_p+4:]
```

## Quality Requirements

- Transitions must be 200-500 words — enough to orient the reader, not so much they drag
- Each transition MUST name a specific character, not "the group" or "everyone"
- The closing transition of Book N must NOT spoil the plot of Book N+1
- Transitions are part of the chapter body, NOT separate sections
- Use the same POV and tense as the book's main narrative