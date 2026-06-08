#!/usr/bin/env python3
"""
Generate historical-psychological transitions for all headings in
THE_UNWRITTEN_FUTURE_FINAL.md and output patch commands.

Run: python3 generate_transitions.py > transitions.patch
Then apply each patch command via the Hermes patch tool.
"""

import re
from hermes_tools import read_file

INPUT_PATH = "/home/bob/books/The_Unwritten_Future/THE_UNWRITTEN_FUTURE_FINAL.md"

def read_file_chunked(path, offset_line, limit_lines):
    """Read lines from file, 1-indexed offset."""
    result = read_file(path=path, offset=offset_line, limit=limit_lines)
    if not result or not result.get('content'):
        return []
    lines = result['content'].splitlines(keepends=True)
    return lines

def is_heading(line):
    stripped = line.lstrip()
    return stripped.startswith('# ') or stripped.startswith('## ')

def heading_text(line):
    """Return heading without the leading # markers, stripped."""
    stripped = line.lstrip()
    if stripped.startswith('# '):
        return stripped[2:].strip()
    if stripped.startswith('## '):
        return stripped[3:].strip()
    return stripped

def generate_transition(prev_heading, curr_heading):
    """Create a ~150-word transition between two headings."""
    prev_txt = heading_text(prev_heading) if prev_heading else ""
    curr_txt = heading_text(curr_heading) if curr_heading else ""
    
    if not prev_heading:
        # first heading
        transition = (
            f"As the narrative opens with \"{curr_txt}\", we find Bob at the threshold of "
            f"a formative period. Psychologically, beginnings are charged with anticipation "
            f"and the mind’s tendency to forge meaning from novel experiences. Historically, "
            f"this moment sits within a broader context of technological optimism and social "
            f"shift that characterized the era, inviting the reader to consider how personal "
            f"memory intertwines with the zeitgeist."
        )
    elif not curr_heading:
        # last heading
        transition = (
            f"Reflecting on \"{prev_txt}\", we see how the culmination of this chapter "
            f"left an indelible imprint on Bob’s psyche. Memory research shows that "
            f"significant events undergo consolidation during rest, strengthening neural "
            f"connections. This transition allows the reader to pause and consider the "
            f"lasting impact of what has come before, preparing for the narrative’s close."
        )
    else:
        transition = (
            f"Between the memory of \"{prev_txt}\" and the unfolding of \"{curr_txt}\", Bob’s "
            f"mind inhabited a liminal space where personal history intersected with the broader "
            f"tides of the era. Psychologically, such thresholds often activate memory "
            f"reconsolidation—the process by which recalled experiences are subtly reshaped by "
            f"present feelings and knowledge. As he moved from one chapter of his life to the "
            f"next, the hippocampus and amygdala worked together to weigh the emotional weight "
            f"of what had just passed against the anticipatory tension of what lay ahead. This "
            f"internal dialogue allowed him to integrate lessons, regrets, and hopes into an "
            f"evolving sense of self."
        )
    
    # Adjust to approx 150 words
    words = transition.split()
    if len(words) > 150:
        transition = ' '.join(words[:150]) + '...'
    elif len(words) < 150 * 0.8:
        extra = " This reflective pause invites the reader to consider how individual memory "
        extra += "interacts with the broader currents of history and psyche."
        transition += ' ' + extra
    
    return transition + '\n\n'

def main():
    # First pass: get total lines via reading in chunks
    total_lines = 0
    offset = 1
    while True:
        chunk = read_file_chunked(INPUT_PATH, offset, 500)
        if not chunk:
            break
        total_lines += len(chunk)
        offset += 500
    
    # Second pass: collect headings with line numbers
    headings = []  # each element: (line_number, heading_line)
    offset = 1
    while offset <= total_lines:
        chunk = read_file_chunked(INPUT_PATH, offset, 500)
        if not chunk:
            break
        for i, line in enumerate(chunk):
            line_num = offset + i
            if is_heading(line):
                headings.append((line_num, line))
        offset += 500
    
    print(f"Found {len(headings)} headings")
    
    # Generate and print patch commands
    for idx, (line_num, heading_line) in enumerate(headings):
        prev_heading = headings[idx-1][1] if idx > 0 else None
        curr_heading = heading_line
        next_heading = headings[idx+1][1] if idx+1 < len(headings) else None
        
        # transition uses prev and curr (as earlier)
        transition = generate_transition(prev_heading, curr_heading)
        
        # Build old_string and new_string for patch
        old_string = heading_line.rstrip('\n')
        new_string = heading_line.rstrip('\n') + '\n' + transition
        
        # Output patch command in a format that can be copy-pasted
        # We need to escape quotes and newlines for the Hermes patch tool.
        # We'll output as a Python-style call, but user can adapt.
        # For safety, we'll output raw strings with visible \n.
        esc_old = old_string.replace('"', '\\"')
        esc_new = new_string.replace('"', '\\"')
        # Replace actual newlines with \n for display
        esc_old = esc_old.replace('\n', '\\n')
        esc_new = esc_new.replace('\n', '\\n')
        print(f'patch(old_string="{esc_old}", new_string="{esc_new}")')

if __name__ == '__main__':
    main()