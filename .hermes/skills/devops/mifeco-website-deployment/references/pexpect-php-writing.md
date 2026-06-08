# pexpect PHP File Writing — $ Sign Stripping

## Problem
pexpect's `sendline()` strips `$` signs from PHP code. Variables like `$uri` become `uri`. This happens because pexpect interprets `$` as shell variable references.

## Affected Operations
- Writing PHP files through pexpect `sendline()`
- Heredoc strings containing PHP variables
- Triple-quoted Python strings passed through pexpect

## Solutions (in order of reliability)

### 1. Write Locally, SCP (Most Reliable)
```python
# Write file locally
with open('/tmp/router.php', 'w') as f:
    f.write(php_content)

# SCP to server
child = pexpect.spawn(f"scp -o StrictHostKeyChecking=no /tmp/router.php {SERVER}:{REMOTE_PATH}/")
child.expect("password:")
child.sendline(PASSWORD)
child.expect(pexpect.EOF, timeout=30)
```

### 2. Base64 Encoding
```python
import base64
encoded = base64.b64encode(php_content.encode()).decode()
child.sendline(f"echo '{encoded}' | base64 -d > router.php")
```

### 3. Python on Remote Server
```python
# SCP a Python script that writes the PHP file
child.sendline("python3 /tmp/write_router.py")
```

## What NOT to Do
- Never use heredoc (`<< 'EOF'`) through pexpect for PHP files
- Never use triple-quoted strings with PHP variables through pexpect
- Never assume `sendline()` will preserve `$` signs

## Verification
After writing a PHP file, always verify:
```bash
grep '\$' router.php | wc -l  # Should show variable count
php -l router.php              # Syntax check
```
