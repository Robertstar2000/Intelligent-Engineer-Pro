# Reader Magnet PDF Replacement Workflow

When replacing a gated reader magnet (free download PDF) on the mifeco.com/books/ section, THREE locations must be updated simultaneously:

## 1. Upload the New PDF

Upload to `/home/dh_mwpxuu/mifeco.com/books/magnets/`:

```python
import pexpect
child = pexpect.spawn('scp /path/to/new.pdf dh_mwpxuu@mifeco.com:/home/dh_mwpxuu/mifeco.com/books/magnets/new-name.pdf', timeout=60, encoding='utf-8')
child.expect('password:', timeout=15)
child.sendline('Rm2214ri####')
child.expect(pexpect.EOF, timeout=60)
```

**Naming:** Use lowercase kebab-case (e.g., `mifeco-ai-playbook.pdf`). Keep the old file for cached references — nothing active points to it after step 3.

## 2. Update the HTML Magnet Card

In the `#magnets` section of `/home/dh_mwpxuu/mifeco.com/books/index.html`. Each card:

```html
<div class="magnet-card">
  <div class="magnet-icon">📊</div>
  <div class="magnet-series">Business Books</div>
  <h3>MIFECO AI Playbook</h3>
  <p>Your complete guide to leveraging AI...</p>
  <a href="#newsletter" class="btn btn-secondary magnet-unlock-btn">Subscribe to Download →</a>
</div>
```

Update title + description via SSH sed.

## 3. Update the Subscribe API (TWO locations)

`/home/dh_mwpxuu/mifeco.com/books/api/subscribe.php` has download links in **two code paths:**
1. Duplicate email (returning subscriber) — first occurrence
2. New subscriber — second occurrence near EOF

Both must have title + url updated. Best: download, edit locally with patch tool, upload back.

## 4. Verify

- HTML card title on index.html
- API response returns new title + URL for both paths
- Clean up test subscribers from subscribers.json after verification