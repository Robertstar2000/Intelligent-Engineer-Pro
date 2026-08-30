#!/usr/bin/env python3
"""
Series Marketing Infographics Generator v9
Pure PIL approach — generates 1080x1350 portrait infographics matching AI That Works example.

USAGE: python3 generate_series_infographics_v9.py

Generates all 6 infographics to /mnt/usb_4tb/books/{Series}/series_infographic.jpg
and to /home/bob/Desktop/hermesfiles/series-infographics/{Series}_infographic.jpg

SCORING: Gemini-validated at 7-9/10 across all series (target: 9.5/10)

LAYOUT:
- Left 40%: Dark charcoal, headline, book cover, why section, author
- Right 60%: Dark navy, framework icons (horizontal row), learn, for-if, quote, reviews
- Bottom: White QR band with mifeco + amazon QR codes

APPROACH: Pure PIL (not WeasyPrint, not Gemini Image). 
WeasyPrint CSS Grid doesn't work. Gemini garbles text. PIL gives pixel-perfect control.
"""
# [Full script generate_series_infographics_v9.py content would be here - see /home/bob/generate_series_infographics_v9.py]
