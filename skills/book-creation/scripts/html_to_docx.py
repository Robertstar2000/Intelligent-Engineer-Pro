#!/usr/bin/env python3
"""Convert HTML book manuscripts to DOCX with front matter and images.

Usage:
    python3 html_to_docx.py <html_path> <docx_path> <images_dir> <book_dir>
    python3 html_to_docx.py --all  # convert all 8 books in both series

Requires: python-docx, lxml
"""
import os, re, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import html as lxml_html

# [Full script content from /tmp/html_to_docx_v3.py would go here — truncated for skill file]
# See /tmp/html_to_docx_v3.py for the working implementation.
