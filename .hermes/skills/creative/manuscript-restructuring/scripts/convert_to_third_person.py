#!/usr/bin/env python3
"""
Convert first-person narrative voice to third-person in a markdown file.

Usage:
    python3 convert_to_third_person.py input.md output.md

Features:
    - Tracks " quote state character-by-character; does NOT change pronouns inside quotes
    - Handles contractions: I'm, I've, I'll, I'd, I don't, I didn't
    - Handles multi-word patterns: I was, I had, I could, I knew, etc.
    - Handles single-word pronouns: I, my, me, myself, we, our, us
    - Preserves capitalization (e.g., My → His at start of sentence)
    - Edge cases: 'I' at line starts, 'I' followed by punctuation
"""

import re
import sys


# Multi-word and contraction patterns — checked FIRST to avoid partial matches
# (ordered longest-first so "I don't" matches before "I" does)
MULTI_WORD_PATTERNS = [
    ("I don't", "Bob didn't"),
    ("I didn't", "Bob didn't"),
    ("I remember", "Bob remembered"),
    ("I could", "Bob could"),
    ("I was", "Bob was"),
    ("I had", "Bob had"),
    ("I knew", "Bob knew"),
    ("I think", "Bob thought"),
    ("I felt", "Bob felt"),
    ("I'm", "Bob was"),
    ("I've", "Bob had"),
    ("I'll", "Bob would"),
    ("I'd", "Bob would"),
]
MULTI_WORD_PATTERNS.sort(key=lambda x: -len(x[0]))

# Single-word patterns — checked AFTER multi-word patterns
# Use IGNORECASE so capitalized forms (My, We, Our, etc.) at sentence starts are caught.
# For 'I' we keep case-sensitive to avoid matching lowercase 'i'.
SINGLE_WORD_PATTERNS = [
    (re.compile(r'\bmy\b', re.IGNORECASE), 'his'),
    (re.compile(r'\bme\b', re.IGNORECASE), 'him'),
    (re.compile(r'\bmyself\b', re.IGNORECASE), 'himself'),
    (re.compile(r'\bwe\b', re.IGNORECASE), 'they'),
    (re.compile(r'\bour\b', re.IGNORECASE), 'their'),
    (re.compile(r'\bus\b', re.IGNORECASE), 'them'),
    (re.compile(r'\bI\b'), 'Bob'),
]


def _capitalize(matched_text: str, replacement: str) -> str:
    """Preserve the capitalization of the matched text in the replacement."""
    if matched_text and matched_text[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def convert_to_third_person(text: str) -> str:
    """
    Main conversion: single character-by-character pass with quote-state tracking.
    
    Outside quotes, apply first→third person transformations.
    Inside quotes, pass text through unchanged.
    """
    result = []
    in_quotes = False
    i = 0
    text_len = len(text)

    while i < text_len:
        char = text[i]

        # --- Quote-state tracking ---
        if char == '"':
            in_quotes = not in_quotes
            result.append(char)
            i += 1
            continue

        if in_quotes:
            result.append(char)
            i += 1
            continue

        # --- Outside quotes: try to match patterns ---
        matched = False

        # 1. Multi-word / contraction patterns (exact string match)
        for pattern, replacement in MULTI_WORD_PATTERNS:
            plen = len(pattern)
            if i + plen <= text_len and text[i:i + plen] == pattern:
                result.append(replacement)
                i += plen
                matched = True
                break

        if matched:
            continue

        # 2. Single-word patterns (regex with \b word boundaries)
        for pattern_re, replacement in SINGLE_WORD_PATTERNS:
            m = pattern_re.match(text, i)
            if m:
                matched_text = m.group(0)
                result.append(_capitalize(matched_text, replacement))
                i += len(matched_text)
                matched = True
                break

        if matched:
            continue

        # 3. No pattern matched — pass character through unchanged
        result.append(char)
        i += 1

    return ''.join(result)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python3 convert_to_third_person.py input.md output.md")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: input file not found — '{input_path}'")
        sys.exit(1)
    except IOError as e:
        print(f"Error reading '{input_path}': {e}")
        sys.exit(1)

    converted = convert_to_third_person(text)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted)
    except IOError as e:
        print(f"Error writing to '{output_path}': {e}")
        sys.exit(1)

    print(f"✓ Converted '{input_path}' → '{output_path}'")


if __name__ == '__main__':
    main()
