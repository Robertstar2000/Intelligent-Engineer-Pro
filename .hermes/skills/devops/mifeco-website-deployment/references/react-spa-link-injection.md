# React SPA External Link Injection (mifeco.com)

## When to Use

Use this reference when adding external links (e.g., to `/consult/` or `/books/`) to the main mifeco.com site, which is a React/Vite single-page application.

---

## Site Architecture

The main `mifeco.com` is a **React SPA** built with Vite:
- Entry point: `/index.html` (minimal shell with `<div id="root">`)
- JS bundle: `/assets/index-[hash].js` (468KB, minified, all content baked in)
- CSS bundle: `/assets/index-[hash].css`
- No server-side rendering — all content is client-rendered React
- No source maps available (`.js.map` returns 404)

The consulting app (`/consult/`) and books site (`/books/`) are **separate PHP/static sites** in subdirectories.

---

## Adding External Links: Two Approaches

### Approach 1: Modify the JS Bundle (Direct but Fragile)

The JS bundle is a single minified file. You can do targeted string replacements:

```bash
# Download the bundle
curl -s "https://www.mifeco.com/assets/index-Dd5ye8Ze.js" -o /tmp/bundle.js

# Find navigation strings
grep -oP '"Services".{0,500}' /tmp/bundle.js | head -3

# Replace: add /consult/ link alongside existing nav items
# Find the exact nav string, then sed it
sed -i 's|"Services"}),l.jsx("a",{href:"#bookstore"|"Services"}),l.jsx("a",{href:"/consult/",target:"_blank",rel:"noopener",className:"text-gray-600 hover:text-blue-600 transition-colors",children:"Virtual Consulting"}),l.jsx("a",{href:"#bookstore"|g' /tmp/bundle.js

# Upload back (SFTP to /home/dh_mwpxuu/mifeco.com/assets/)
```

**Caveats:**
- Bundle hash changes on rebuild — changes are lost if the site is redeployed
- Minified JS is fragile — a single character offset breaks everything
- Must maintain exact string matches including whitespace
- Test thoroughly after any change

### Approach 2: Inject External Script (Recommended, Survives Rebuilds)

Add a small script to `/index.html` that waits for React to render, then injects links:

```html
<!-- Add before closing </body> tag in /index.html -->
<script>
(function() {
  function injectLinks() {
    // Wait for React nav to render
    const nav = document.querySelector('nav');
    if (!nav) { setTimeout(injectLinks, 500); return; }
    
    // Add Virtual Consulting link
    const consultLink = document.createElement('a');
    consultLink.href = '/consult/';
    consultLink.textContent = 'Virtual Consulting';
    consultLink.className = 'text-gray-600 hover:text-blue-600 transition-colors';
    consultLink.style.marginLeft = '2rem';
    
    // Add Books link  
    const booksLink = document.createElement('a');
    booksLink.href = '/books/';
    booksLink.textContent = 'Books';
    booksLink.className = 'text-gray-600 hover:text-blue-600 transition-colors';
    booksLink.style.marginLeft = '2rem';
    
    // Insert into nav
    nav.appendChild(consultLink);
    nav.appendChild(booksLink);
  }
  
  // Start polling after page load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectLinks);
  } else {
    injectLinks();
  }
})();
</script>
```

**Advantages:**
- Survives JS bundle rebuilds
- No fragile string matching
- Easy to update

**Disadvantages:**
- Links appear after a brief delay (polling interval)
- May need adjustment if React component structure changes

---

## Identifying Bundle Files

The bundle filename includes a content hash that changes on rebuild. Always verify the current hash:

```bash
curl -s "https://www.mifeco.com/" | grep -oP 'src="/assets/index-[^"]+\.js"'
```

---

## Key Architectural Insight

The `#bookstore` nav link in the SPA is an **anchor to a section on the same page**, NOT an external link to `/books/`. These are different things:
- The SPA has its own bookstore section (id: `#bookstore`) with book cards
- `/books/` is a separate static PHP site in a subdirectory

When adding external links, you're adding them **alongside** the existing SPA navigation, not replacing it.
