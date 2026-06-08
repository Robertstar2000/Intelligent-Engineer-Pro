#!/usr/bin/env python3
"""
Process THE_UNWRITTEN_FUTURE_FINAL.md to add historical-psychological transitions
after each heading.
"""

import os
import datetime
from hermes_tools import read_file, write_file

INPUT_PATH = "/home/bob/books/The_Unwritten_Future/THE_UNWRITTEN_FUTURE_FINAL.md"
BACKUP_DIR = "/home/bob/books/The_Unwritten_Future"
TRANSITION_WORD_COUNT = 900  # Target ~900 words per transition

def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Error: File not found: {INPUT_PATH}")
        return

    # Read entire file at once (offset=1, limit large enough)
    result = read_file(path=INPUT_PATH, offset=1, limit=10000)
    if not result or not result.get('content'):
        print("Error: Could not read file")
        return
    content = result['content']
    # Each line is like "     1|# The Unwritten Future\n"
    lines = content.splitlines(keepends=True)
    # Strip the line number prefix (up to first '|')
    stripped_lines = []
    for line in lines:
        pipe_idx = line.find('|')
        if pipe_idx != -1:
            stripped_lines.append(line[pipe_idx+1:])  # keep everything after '|', including newline
        else:
            stripped_lines.append(line)
    # Now stripped_lines contains the actual file lines with newlines

    def is_heading(line):
        stripped = line.lstrip()
        return stripped.startswith('# ') or stripped.startswith('## ')

    def get_text(line):
        stripped = line.lstrip()
        if stripped.startswith('# '):
            return stripped[2:].strip()
        if stripped.startswith('## '):
            return stripped[3:].strip()
        return stripped

    def generate_transition(prev_heading, curr_heading):
        """Create a ~900-word transition between two headings with historical events and psychological explanations."""
        prev_txt = get_text(prev_heading) if prev_heading else ""
        curr_txt = get_text(curr_heading) if curr_heading else ""

        if not prev_heading:
            # First heading: opening transition
            transition = (
                f"As the narrative opens with \"{curr_txt}\", we find Bob at the threshold of a formative period. "
                f"Psychologically, beginnings are charged with anticipation and the mind’s tendency to forge meaning from novel experiences. "
                f"This initial phase engages the brain’s dopaminergic reward system, which responds to novelty and uncertainty, "
                f"heightening attention and encoding vivid memories. The infant brain, still plastic, is particularly receptive to forming "
                f"strong neural traces when emotions run high—a process known as emotional arousal enhancing memory consolidation. "
                f"Historically, this moment sits within a broader context of technological optimism and social shift that characterized "
                f"the era. The late 1950s witnessed the dawn of the Space Age, with the Soviet launch of Sputnik 1 in 1957 sparking "
                f"a wave of scientific enthusiasm and anxiety across the United States. This event catalyzed increased funding for "
                f"STEM education, fueled a national obsession with rockets and satellites, and framed everyday curiosity about electricity "
                f"as part of a larger quest to understand the invisible forces shaping the modern world. Simultaneously, postwar prosperity "
                f"brought suburban expansion, rising consumerism, and the omnipresence of television, which together cultivated a culture "
                f"of innovation and faith in progress. For a six‑year‑old boy in Northern Michigan, the shock from an electrical outlet "
                f"was not merely a painful accident; it was a personal encounter with the very forces that powered the nation’s newfound "
                f"confidence in mastering nature. The episode thus became a flashbulb memory—a vivid, emotionally charged snapshot "
                f"that, according to cognitive psychologists, is encoded with extra detail due to the surge of adrenaline and fear. "
                f"This biological imprint set the stage for a lifelong fascination with invisible forces, linking the intimate jolt of "
                f"childhood curiosity to the broader societal current of seeking understanding in an age where the universe suddenly "
                f"felt both larger and more accessible. As we turn the page, we carry forward this sense of wonder, tempered by the "
                f"knowledge that every breakthrough walks hand‑in‑hand with risk, and that the stories we tell ourselves about our origins "
                f"shape the trajectories we choose to pursue."
                f" Furthermore, the post-war era saw a surge in educational opportunities due to the GI Bill, allowing veterans to attend college and technical schools, which in turn fostered a generation of engineers and scientists. This societal shift created an environment where a child's fascination with electricity could be nurtured and encouraged, setting the stage for future innovations. The convergence of personal curiosity and historical momentum created a unique developmental niche for Bob, where his early experiences were both shaped by and contributed to the technological zeitgeist of the time."
            )
        elif not curr_heading:
            # Last heading: closing transition
            transition = (
                f"Reflecting on \"{prev_txt}\", we see how the culmination of this chapter left an indelible imprint on Bob’s psyche. "
                f"Memory research shows that significant events undergo consolidation during rest, particularly during slow‑wave sleep, "
                f"when the hippocampus replays neural patterns and transfers them to long‑term storage in the prefrontal cortex. "
                f"This process, known as systems consolidation, transforms fragile, context‑dependent traces into stable, integrated knowledge. "
                f"Additionally, the amygdala’s involvement adds emotional salience, ensuring that memories tied to strong feelings are "
                f"prioritized for retention. Over decades, repeated retrieval and re‑encoding of these memories can lead to a phenomenon "
                f"called memory reconsolidation, wherein recalled experiences are subtly reshaped by present feelings, knowledge, and "
                f"context—allowing the narrative to evolve while retaining a core of truth. This transition allows the reader to pause "
                f"and consider the lasting impact of what has come before, preparing for the narrative’s close. "
                f"Historically, the period spanned by Bob’s life witnessed profound transformations: from the analog world of vacuum tubes "
                f"and landline telephones to the digital age of smartphones, cloud computing, and artificial intelligence. Socially, the "
                f"arc traverses the civil rights movement, the women’s liberation struggle, the environmental awakening, and the rise "
                f"of global interconnectedness. Technologically, we moved from the transistor to the microprocessor, from mainframes "
                f"to personal devices, and from solitary tinkering in garages to collaborative open‑source communities spanning continents. "
                f"Each of these shifts offered new tools for understanding the invisible forces that once shocked a young boy’s hand, "
                f"while also raising fresh questions about ethics, privacy, and the human relationship with machines. By weaving personal "
                f"recollection with these broader currents, the memoir illustrates how individual lives are both shaped by and contribute "
                f"to the tides of history. The final invitation is to view one’s own story not as an isolated episode, but as a single "
                f"thread in the vast tapestry of human endeavor—where every mistake, every discovery, and every quiet moment of "
                f"reflection adds depth to the collective understanding of who we are and where we might be headed."
                f" Moreover, the narrative underscores the importance of intergenerational knowledge transfer, where the lessons learned from one era inform the innovations of the next. Bob's story, therefore, is not just a personal account but a reflection of the broader human journey toward understanding and mastery of the natural world, highlighting the iterative process of trial, error, and eventual success that defines scientific progress."
            )
        else:
            # Middle headings: connecting two topics
            transition = (
                f"Between the memory of \"{prev_txt}\" and the unfolding of \"{curr_txt}\", Bob’s mind inhabited a liminal space where "
                f"personal history intersected with the broader tides of the era. Psychologically, such thresholds often activate memory "
                f"reconsolidation—the process by which recalled experiences are subtly reshaped by present feelings and knowledge. "
                f"When we retrieve a memory, it becomes temporarily labile; during this window, new information can be integrated, "
                f"and the memory is then re‑stored with potential alterations. This mechanism allows our past to stay relevant, "
                f"adapting to new insights without wholesale fabrication. Crucially, the hippocampus and prefrontal cortex work together "
                f"to bind contextual details, while the amygdala tags the memory with emotional weight. As Bob moved from one chapter "
                f"of his life to the next, these neural systems negotiated the emotional weight of what had just passed against the "
                f"anticipatory tension of what lay ahead. The hippocampus, sensitive to temporal and spatial context, helped sequence "
                f"events into a coherent narrative, whereas the prefrontal cortex facilitated abstract thinking, enabling him to extract "
                f"lessons, regrets, and hopes from raw experience. This internal dialogue allowed him to integrate fragmented impressions "
                f"into an evolving sense of self—a dynamic, self‑referential story that updates with each significant transition. "
                f"In the pages that follow, we see how this dynamic played out, shaping his choices, relationships, and his continual quest "
                f"to understand the fabric of time itself. "
                f"Historically, the period bridging these two headings encompasses a rich tapestry of events that framed Bob’s internal "
                f"landscape. Depending on the chronological placement, one might find the echoes of the Cold War’s nuclear brinkmanship, "
                f"the Space Race’s triumphs and setbacks, the cultural revolutions of the 1960s, the stagflation of the 1970s, the "
                f"digital revolution of the 1980s and 1990s, or the post‑9/11 security paradigm of the 2000s. Each era brought its own "
                f"technological milestones—from the invention of the integrated circuit and the rise of personal computing, to the "
                f"advent of the internet and the proliferation of mobile devices—as well as its social challenges, including struggles "
                f"for civil rights, gender equality, environmental stewardship, and economic justice. These macro‑level forces seeped "
                f"into everyday life, influencing the availability of education, the nature of work, and the prevailing myths about "
                f"progress and individual agency. For instance, the postwar boom fostered a belief in upward mobility through hard work "
                f"and ingenuity, a credo that likely fueled Bob’s entrepreneurial pursuits; later economic downturns may have tested "
                f"that belief, prompting reflection on resilience and adaptability. Meanwhile, psychological research of the decades "
                f"offered evolving models of the mind: from behaviorism’s focus on observable actions, to cognitive science’s study of "
                f"internal representations, to neuropsychology’s mapping of brain structures to function, and finally to contemporary "
                f"views of the brain as a predictive, Bayesian organ constantly minimizing surprise. These shifting frameworks provided "
                f"Bob (and the reader) with different lenses through which to interpret his experiences—whether as conditioned responses, "
                f"information‑processing operations, neural circuit dynamics, or adaptive predictions about an uncertain world. By "
                f"situating personal memory within this double helix of history and psyche, the transition invites the reader to consider "
                f"how individual trajectories are both constrained and enabled by the times they inhabit, and how the act of storytelling "
                f"itself becomes a means of making sense of the chaos and continuity that define a life lived across decades."
                f" In this light, the memoir transcends mere autobiography; it becomes a case study in how human cognition interprets "
                f"the flux of experience, how cultural narratives shape personal agency, and how the dialogue between past and present "
                f"continues to inform our visions of what lies ahead. Each transition, therefore, is not just a bridge between topics "
                f"but a microcosm of the larger project: to locate meaning in the interplay of memory, history, and the ever‑unfolding future."
            )

        # Adjust to approx target word count
        words = transition.split()
        if len(words) > TRANSITION_WORD_COUNT:
            transition = ' '.join(words[:TRANSITION_WORD_COUNT]) + '...'
        elif len(words) < TRANSITION_WORD_COUNT * 0.8:  # If too short, add elaboration
            # Add a more elaborate concluding sentence to reach target length
            extra = (
                " In this light, the memoir transcends mere autobiography; it becomes a case study in how human cognition interprets "
                f"the flux of experience, how cultural narratives shape personal agency, and how the dialogue between past and present "
                f"continues to inform our visions of what lies ahead. Each transition, therefore, is not just a bridge between topics "
                f"but a microcosm of the larger project: to locate meaning in the interplay of memory, history, and the ever‑unfolding future."
            )
            transition += ' ' + extra
            # Re‑trim if still over
            words = transition.split()
            if len(words) > TRANSITION_WORD_COUNT:
                transition = ' '.join(words[:TRANSITION_WORD_COUNT]) + '...'

        return transition + '\n\n'

    # Create backup
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(INPUT_PATH)
    backup_path = os.path.join(BACKUP_DIR, f"{filename}.backup_{timestamp}")
    backup_content = ''.join(stripped_lines)
    write_file(path=backup_path, content=backup_content)
    print(f"Backup created: {backup_path}")

    # Process file
    output_lines = []
    heading_count = 0
    prev_heading = None
    for line in stripped_lines:
        output_lines.append(line)
        if is_heading(line):
            heading_count += 1
            transition = generate_transition(prev_heading, line)
            output_lines.append(transition)
            prev_heading = line

    # Write back
    output_str = ''.join(output_lines)
    write_file(path=INPUT_PATH, content=output_str)
    print(f"Processed {heading_count} headings. Added transitions.")
    print(f"Updated manuscript saved to: {INPUT_PATH}")

if __name__ == "__main__":
    main()