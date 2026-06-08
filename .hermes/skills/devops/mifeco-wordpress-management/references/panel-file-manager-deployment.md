# DreamHost Deployment via Panel File Manager

## When to Use This Approach

SSH/SFTP is frequently unavailable on DreamHost shared hosting (port 22 connection refused). This is a known limitation of shared hosting plans. Use the Panel File Manager as your **primary fallback** when SSH fails.

## Step-by-Step Deployment

### 1. Create Deployment Package

```bash
# For a subdirectory deployment (e.g., /books/)
cd /path/to/books-section
zip -r /tmp/books-section-deploy.zip . \
  --exclude "data/*" \
  --exclude ".git/*"

# For SPA root deployment
cd /path/to/mifeco-website/dist
zip -r /tmp/spa-dist.zip .
```

### 2. Log into DreamHost Panel

1. Navigate to `https://panel.dreamhost.com`
2. Enter credentials from `~/.hermes/secrets/mifeco-dreamhost.env`
3. **Panel is a React SPA** — if snapshot shows empty, use JS: `document.body.innerText.substring(0, 2000)`

### 3. Open File Manager

**Method A:** Panel → **Users** → **SFTP Users & Files** → dh_mwpxuu → **"File Manager"**
**Method B:** Panel → **Websites** → **Manage** → mifeco.com → **File Manager**

### 4. Upload and Extract

1. Navigate to target directory (`/home/dh_mwpxuu/mifeco.com/` or subfolder)
2. Click **Upload** → select zip file
3. Wait for upload to complete
4. Select zip → click **Extract**
5. Delete zip after extraction

### 5. Verify

```bash
curl -s -o /dev/null -w "%{http_code}" https://www.mifeco.com/books/
```

## URL Token (Direct Access)

The File Manager URL contains a base64-encoded token with SFTP credentials:

```bash
echo 'BASE64_TOKEN' | base64 -d
# Returns: {"t":"sftp","c":{"v":0,"p":"PASSWORD","s":0,"m":"Password"}}
```

This sometimes reveals SFTP credentials that work even when standard SSH doesn't.

## Tips

- **Never include `data/` directories** in deployment zips (contains subscriber data)
- **Don't use `--delete`** — web root contains both SPA and WordPress
- **Test after every deployment** with `curl` or browser
