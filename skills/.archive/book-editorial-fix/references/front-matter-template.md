# Standard Front Matter Template (Copyright + TOC + Acknowledgments)

Insert before Chapter 1 of every full-length book. Place after any title/author banner but before the first chapter header.

```markdown
# [Book Title]

[Series name, if applicable]

**Copyright © 2026 Bob J Mills**

All rights reserved. No part of this book may be reproduced in any form or by any electronic or mechanical means, including information storage and retrieval systems, without written permission from the author, except for the use of brief quotations in a book review.

This is a work of fiction. Names, characters, places, and incidents either are the product of the author's imagination or are used fictitiously. Any resemblance to actual persons, living or dead, events, or locales is entirely coincidental.

ISBN: [To be assigned]

First Edition: 2026

---

## Table of Contents

- Chapter 1: [Title]
- Chapter 2: [Title]
...

---

## Acknowledgments

The author thanks the beta readers, editors, and early readers who helped shape this book. Special thanks to [community]. Without the support of family, friends, and readers, these stories would not exist.

---

```

### Insertion Technique

Use `cat >>` to append, temp-file prepend for front matter:

```bash
# Prepend front matter
cat front_matter.md MANUSCRIPT.md > MANUSCRIPT.md.new
mv MANUSCRIPT.md.new MANUSCRIPT.md

# Or use Python for precise insertion after a specific marker
python3 << 'PYEOF'
with open('MANUSCRIPT.md', 'r') as f:
    c = f.read()
insert = """[front matter text]"""
c = c.replace("[marker before Chapter 1]", f"{insert}[marker before Chapter 1]", 1)
with open('MANUSCRIPT.md', 'w') as f:
    f.write(c)
PYEOF
```

### Pitfalls

- **Worded chapter numbers**: Some manuscripts use `## Chapter One:` instead of `## Chapter 1:`. The TOC must match the actual header format.
- **Non-sequential numbers**: CLLC Bk 1 uses chapters 1,2,3,4,5,7,10,11,12,13,16,18,21,25,26,27,28,29 — the TOC must list only what exists.
- **Inline headers**: Some books (Tomorrow Remembered) have `## Chapter Two:` merged into the end of the previous paragraph with no newline before them. Detect with `grep -n "Chapter " MANUSCRIPT.md | grep -v "^[0-9]*:##"`
- **Non-fiction chapters**: Business books use Part divisions, not chapter numbers. Use Part headers for the TOC instead.
- **Multiple MANUSCRIPT files**: CLLC books have a stub `MANUSCRIPT.md` and the real `retainer-to-trouble_MANUSCRIPT.md` etc. Always verify word count and header count on the file you're modifying.