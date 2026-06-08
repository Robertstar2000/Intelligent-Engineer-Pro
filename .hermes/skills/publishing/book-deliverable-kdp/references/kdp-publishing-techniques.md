# KDP Publishing Techniques

## KDP Sign-In Requires OTP

Amazon KDP sign-in always triggers two-step verification (OTP sent to phone).
The agent CANNOT complete sign-in alone -- must ask user for the OTP code.

Workflow:
1. Navigate to `https://kdp.amazon.com/en_US/bookshelf` (triggers sign-in redirect)
2. Enter email, click Continue
3. Enter password, click Sign in
4. **STOP** -- ask user for the OTP code (sent to phone ending in last 4 digits)
5. Enter OTP code, check "Don't require code on this browser", click Sign in
6. Verify login success by checking for bookshelf page

**Session interrupt warning**: If the session is interrupted before OTP is entered,
the login state is lost. The entire sign-in flow must be restarted from scratch.
There is no way to resume a partial KDP login. Plan for this: warn the user
beforehand that you'll need the OTP within the same conversation turn.

NOTE: `google/gemini-2.5-flash-image-preview` returns 404 on OpenRouter.
Use `google/gemini-2.5-flash-image` instead.

## Partial KDP Package Anti-Pattern

A common failure mode: a book directory has `KDP_PACKAGE/Marketing_and_Compliance/`
with all text files, plus a cover and infographic in the root, but is **missing the
actual publishing assets** inside KDP_PACKAGE:

Missing (but required):
- `KDP_PACKAGE/Kindle/` -- contains the cover JPEG for Kindle upload
- `KDP_PACKAGE/Print/` -- contains the print-ready PDF
- `KDP_PACKAGE/images/` -- chapter illustration images (if applicable)
- `KDP_PACKAGE/*.zip` -- the final zipped submission package

Present (but insufficient without the above):
- `cover.jpg/cover.png` in book root
- `Marketing_Infographic.png`
- `Author_Photo.jpg`
- `KDP_PACKAGE/Marketing_and_Compliance/*.txt` files

**How to detect**: When auditing a book for KDP readiness, check for the
*contents* of KDP_PACKAGE, not just its existence. A directory with only
`Marketing_and_Compliance/` inside is a partial/incomplete package. Report it
as "marketing-ready, publishing-incomplete" rather than "KDP-ready."

**How to fix**: Use the main SKILL.md build path: generate/render the print PDF,
build the Kindle cover from the KDP-spec-compliant image, add chapter images,
then zip the entire KDP_PACKAGE directory.

## Marketing Infographic Generation

1. Generate QR codes with `qrcode` library (qrcode==7.4.2)
2. Generate infographic base with Gemini via OpenRouter
3. Composite QR codes onto corners with PIL paste
4. Target size: 1024x1280 (4:5 ratio), PNG format

## Marketing Infographic Generation (Updated 2026-05-31)

### When to Use
User requests a "sales infographic," "marketing infographic," or "social media image" for a book.

### Two-Pass Technique

**Pass 1: Generate the base image with Flux.2 Max via OpenRouter.**
Do NOT include QR codes, fine text, or precise branding in the AI prompt.
Focus on the hero visual, mood, and large text headers only.
Use model `black-forest-labs/flux.2-max`, timeout 300s.
Extract base64 from `choices[0].message.images[0].image_url`.

**Pass 2: Composite QR codes, text bars, and branding with PIL.**
1. Load raw image as RGBA
2. Load and resize QR codes to 180x180 (qrcode library, ERROR_CORRECT_H, 300x300 source)
3. Add bottom bar: dark navy, alpha 230, height ~220px
4. Paste QR codes side by side with 8px white padding
5. Add top branding bar: dark navy, alpha 200, height ~50px
6. Add text labels with DejaVuSans-Bold or LiberationSans-Bold
7. Save final as PNG with optimize=True

### Prompt Guidelines
- Specify book title, subtitle, author name, and key sales hook/stat
- Request bold business aesthetic with specific brand colors
- Put the urgency CTA as large bold text in the prompt
- Request 1024x1024 (square) for Instagram/social media
- Do NOT ask AI to render QR codes or precise logos -- those are Pass 2
- Include "no watermarks" in prompt

### Output Files
- `Marketing_Infographic.png` -- final composited image in book root
- `Marketing_Infographic_raw.png` -- raw AI output (keep for recomposition)
- Also copy final to `KDP_PACKAGE/Marketing_Infographic.png`

### QR Code URLs
- MIFECO: `https://www.mifeco.com`
- Amazon: `https://www.amazon.com/stores/Bob-J-Mills/author/`

## Chapter Cleanup Before PDF Regeneration

When chapters have been edited (dedup, cleanup), always regenerate the PDF to sync page numbers. Use two-pass TOC rendering:
- Pass 1: Render with empty page numbers
- Extract page numbers with pdftotext
- Pass 2: Render with hardcoded page numbers
