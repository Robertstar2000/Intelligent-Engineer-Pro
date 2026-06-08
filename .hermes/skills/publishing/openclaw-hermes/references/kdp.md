# Amazon KDP Checklist

## Account

- Create or access Kindle Direct Publishing.
- Complete tax interview.
- Add payment information.
- Confirm author, publisher, or imprint name.
- Decide whether to enroll in KDP Select.

Do not enroll the eBook in KDP Select if the user wants the eBook available on Kobo, Barnes and Noble, Google Play, Apple, or other wide retailers during the exclusivity period.

## Files

- Prepare Kindle manuscript, usually EPUB, DOCX, or KPF.
- Prepare cover.
- Use Kindle Previewer.
- Check navigation, table of contents, chapter headings, images, links, and back matter.

## Metadata

- Title matches cover and manuscript.
- Subtitle matches cover and manuscript when used.
- Author name matches consistently.
- Series name goes in the series field.
- Categories and keywords match the book.
- Description is accurate and not misleading.
- No keyword stuffing, competitor names, fake awards, temporary price claims, or unrelated terms.

## Rights and Content

- User owns or controls all required rights.
- No copyright, trademark, privacy, publicity, or defamation issues.
- No misleading content.
- No poor customer experience.
- Adult content is correctly classified.

## AI Disclosure

Disclose AI-generated final reader-facing text, images, or translations. AI-assisted brainstorming, editing, outlining, proofreading, and refinement do not require disclosure if final content is human-created.

## ISBN

- Kindle eBook does not require an ISBN.
- Paperback and hardcover require ISBN handling.
- KDP free ISBN is for KDP print distribution.
- Publisher-owned ISBN is best for imprint control.

## Pricing

- Choose royalty path where eligible.
- Review delivery fee impact for large eBooks.
- Align prices across retailers unless running a controlled promotion.
- Normal list price cannot simply be set to free through standard KDP pricing.

## Live Verification

- Product page live.
- Cover correct.
- Description clean.
- Author page linked.
- Series linked if applicable.
- Formats linked when metadata matches.
- Save ASIN and Amazon.com URL.

## Publishing (No-AI Login)

**Amazon KDP blocks AI-driven logins.** The AI cannot enter credentials, complete CAPTCHAs, or do 2FA. Publishing requires a browser handoff:

1. **AI prepares**: manuscript, cover, metadata, AI disclosure, marketing copy
2. **AI opens browser**: Navigate to `https://kdp.amazon.com`
3. **Bob logs in**: Enter username + password + 2FA manually in the shared browser session
4. **AI navigates**: Once on the bookshelf dashboard, click "+ Create"
5. **AI fills metadata**: Title, subtitle, series, author, description, categories, keywords via `browser_type`
6. **Bob uploads files**: Manuscript EPUB and cover PNG (file dialogs can't be automated)
7. **AI guides pricing**: Read available options and tell Bob which to select
8. **AI marks disclosure**: Check the AI-generated content checkbox
9. **Bob submits**: Click "Publish Your Kindle eBook"
10. **AI confirms**: Capture ASIN from the confirmation screen and report to Bob
