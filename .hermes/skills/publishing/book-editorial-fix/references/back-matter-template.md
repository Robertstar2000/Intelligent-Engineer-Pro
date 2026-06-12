# Standard Back Matter Template (Also by Bob J Mills)

Append to the end of every full-length MANUSCRIPT.md after the final chapter content.

```markdown
---

## Also by Bob J Mills

### The Age of Lightships Series
- [**Sunward Exodus**](https://www.amazon.com/dp/[LINK])
- [**The Mercury Accord**](https://www.amazon.com/dp/[LINK])
- [**Ghosts Beyond Neptune**](https://www.amazon.com/dp/[LINK])
- [**The Last Photon Fleet**](https://www.amazon.com/dp/[LINK])

### The Lunar Foundation Series
- [**Moon Rock**](https://www.amazon.com/dp/[LINK])
- [**Mooncoming**](https://www.amazon.com/dp/[LINK])
- [**Waters End**](https://www.amazon.com/dp/[LINK])
- [**Waters Horizon**](https://www.amazon.com/dp/[LINK])

### No Blue Sky Series
- [**Built from Dust**](https://www.amazon.com/dp/[LINK])
- [**The Oxygen Gamble**](https://www.amazon.com/dp/[LINK])
- [**Rivers Under Mars**](https://www.amazon.com/dp/[LINK])
- [**The Red Charter**](https://www.amazon.com/dp/[LINK])
- [**The First Martian Nation**](https://www.amazon.com/dp/[LINK])

### Cindy Lou Legal Capers Series
- [**Retainer to Trouble**](https://www.amazon.com/dp/[LINK])
- [**Clause for Alarm**](https://www.amazon.com/dp/[LINK])
- [**Affidavits and Alibis**](https://www.amazon.com/dp/[LINK])

### Business / Non-Fiction
- [**The Crisis-Ready Company**](https://www.amazon.com/dp/[LINK])
- [**AI That Works**](https://www.amazon.com/dp/[LINK])
- [**The Owner's Manual for AI Agents**](https://www.amazon.com/dp/[LINK])

### Memoir
- [**Tomorrow Remembered**](https://www.amazon.com/dp/[LINK])

---

**Get free prequel novellas** at [mifeco.com/books](https://www.mifeco.com/books)

**Visit the author's website:** [mifeco.com](https://www.mifeco.com)

---
```

### Insertion Technique

Use `cat >>` with heredoc (reliable, never fails on old_string matching):

```bash
cat >> /path/to/MANUSCRIPT.md << 'EOF'

---

## Also by Bob J Mills

...full template...

---
EOF
```

### Notes
- Use `[LINK]` as placeholder ASIN if Amazon links aren't assigned yet
- Include ALL 6 series even if the current book is in only one
- Business books and Tomorrow Remembered should also include fiction series (cross-promotion)
- The novella/free book link goes to mifeco.com/books
- Add a "Reader review request" footer after the back matter if one doesn't exist: "If you enjoyed this book, please leave a review — it helps independent authors enormously."