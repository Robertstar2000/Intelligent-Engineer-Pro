# Memory compacted via MemPalace offload on 2026-06-23T07:25:57.925827+00:00 UTC
# Full content is available in MemPalace (~/.hermes/mempalace/).
#
§
§
User wants chapter images in Lunar Foundation and Age of Lightships books to be black/white/gray pencil sketches depicting chapter content — realistic moon (no Saturn-like rings), modern rovers/rockets/space suits. Each image must represent its chapter title.
§
KDP EPUB TOC requirements learned: (1) nav.xhtml with epub:type="toc" AND epub:type="landmarks" must have properties="nav" in OPF manifest, (2) NCX file must have playOrder attributes on all navPoint elements, (3) spine must have toc="ncx", (4) HTML TOC page should be near front of book before chapter 1, (5) images/ and chapter_images/ folders in book projects are usually identical copies.
§
Book projects structure: Source EPUBs are in output/ folder, KDP upload versions in KDP_Package/ and KDP_PACKAGE/Kindle/. The _fixed.epub files in output/ are the most complete versions with images. Lunar Foundation has 4 books (Moon Rock, Mooncoming, Waters End, Waters Horizon). Age of Lightships has 4 books (Sunward Exodus, Mercury Accord, Ghosts Beyond Neptune, Last Photon Fleet).
§
KDP rejects EPUB files for both Lunar Foundation and Age of Lightships series (as of 2026-06-23). Workaround: convert print HTML manuscripts to DOCX using python-docx + lxml for manual review. LibreOffice headless and pandoc both fail for EPUB→DOCX on this system. See book-creation skill references/html-to-docx-conversion.md for the technique.