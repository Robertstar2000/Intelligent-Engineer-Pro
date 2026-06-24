---
name: manual-docx-processing
description: Extract text from DOCX via XML parsing when python-docx unavailable
category: software-development
version: 1.0
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Manual DOCX Processing via XML Parsing

## When to Use
When you need to extract text content from a DOCX file but standard libraries like `python-docx` or `pandoc` are unavailable or not working.

## Problem
Standard DOCX processing tools may be missing in restricted environments, requiring alternative approaches to access document content.

## Solution
Manually treat the DOCX file as a ZIP archive and extract/process the XML content directly.

## Steps

1. **Verify DOCX Structure**
   ```bash
   # Check if it's a valid ZIP archive
   unzip -l document.docx
   # Should show word/document.xml among other files
   ```

2. **Extract the XML Content**
   ```bash
   # Create a temporary directory
   mkdir -p /tmp/docx_extract
   # Extract the DOCX (which is a ZIP file)
   unzip -q document.docx -d /tmp/docx_extract
   # The main content is in word/document.xml
   ```

3. **Parse the XML Content**
   Use Python's built-in `xml.etree.ElementTree` to extract text:
   ```python
   import xml.etree.ElementTree as ET
   
   # Parse the document XML
   tree = ET.parse('/tmp/docx_extract/word/document.xml')
   root = tree.getroot()
   
   # Define namespace (standard for WordprocessingML)
   ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
   
   # Extract all text from paragraph elements
   paragraphs = []
   for para in root.findall('.//w:p', ns):
       texts = [node.text for node in para.findall('.//w:t', ns) if node.text]
       if texts:
           paragraphs.append(''.join(texts))
   
   # Join paragraphs with double newlines for markdown-like formatting
   narrative_text = '\n\n'.join(paragraphs)
   ```

4. **Clean and Format the Extracted Text**
   - Fix escaped XML characters (like `&amp;` → `&`)
   - Normalize whitespace and newlines
   - Restore any markdown heading structures if they were present
   - Remove any residual XML artifacts

5. **Verify Extraction Quality**
   - Check word count against expectations
   - Ensure no major content loss
   - Validate paragraph boundaries are preserved

## DOX Integration

When working in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the change affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Pitfalls & Solutions

- **Missing Namespaces**: Always define the proper WordprocessingML namespace (`w:` prefix) when searching elements
- **Lost Formatting**: This method extracts only text content; formatting (bold, italic, etc.) will be lost
- **Complex Elements**: Tables, images, and headers/footers require additional parsing if needed
- **Large Files**: Process in chunks if memory is constrained; the XML approach is generally efficient
- **Corrupted DOCX**: Always verify the ZIP structure first with `unzip -t document.docx`

## Reconstruction Notes
If you need to preserve specific structural elements:
- Headings: Look for `w:pStyle` with values like 'Heading1', 'Heading2'
- Lists: Check for `w:numPr` elements
- The basic approach above extracts all paragraph text in document order

## Example Workflow from Practice
In a recent memoir project:
1. User provided DOCX via Telegram when standard tools failed
2. Extracted `word/document.xml` using unzip
3. Used ElementTree to parse and extract all w:t (text) elements
4. Cleaned escaped characters and normalized spacing
5. Resulted in clean narrative text ready for further processing
6. Enabled transition extraction and rewriting from original manuscript

## Validation
- Compare input/output character counts (should be similar minus XML markup)
- Spot-check paragraphs for correctness
- Verify no XML tags remain in output

## Dependencies
- Standard Python library (`xml.etree.ElementTree`, `zipfile` via unzip command)
- No external packages required

## Alternative Approaches
- If unzip is unavailable, use Python's `zipfile` module directly
- For simpler text extraction, `strings` + grep can work but loses structure
- Consider online conversion tools if network is available