# SSH MySQL Query Quoting Patterns

MySQL queries passed through pexpect SSH (via `ssh_blog.py ssh` or inline `ssh_run()`) are notoriously brittle because the shell strips quoting levels before MySQL sees them. Use these proven patterns.

## Pattern 1: Python heredoc via terminal() (RECOMMENDED)

The cleanest approach — write the Python script inline using a heredoc delimiter so the shell and pexpect don't fight over quotes:

```python
# Inside a terminal("python3 << 'PYEOF' ... PYEOF") call
import sys
sys.path.insert(0, '/home/bob/.hermes/skills/content-marketing/mifeco-daily-blog/scripts')
from ssh_blog import ssh_run

result = ssh_run("""mysql -h mysql.mifeco.com -u ak48bme -p7jpetxEL mifeco_com_1 -N -e "SELECT post_title, post_name, post_date FROM wp_gryu9c_posts WHERE post_type='post' ORDER BY post_date DESC;" """)
print(result)
```

**How to run it:**
```bash
cd /home/bob && python3 << 'PYEOF'
... python code from above ...
PYEOF
```

**Why it works:** The `<< 'PYEOF'` heredoc (quoted delimiter) prevents shell expansion inside the script. Python's `"""..."""` preserves the inner double quotes for `-e` argument. pexpect sees the whole thing as one command string.

## Pattern 2: Direct ssh_blog.py (works for simple queries)

For simple queries without quotes or with no WHERE clause:

```bash
python3 scripts/ssh_blog.py ssh "mysql -h mysql.mifeco.com -u ak48bme -p7jpetxEL mifeco_com_1 -N -e 'SELECT post_title, post_name FROM wp_gryu9c_posts LIMIT 5;'"
```

**Fails when** the SQL contains `WHERE post_type='post'` because the single quotes inside the SQL conflict with the SSH command quoting.

## Pattern 3: Inline Python via terminal() with escaped SQL

```python
# Avoid this — too fragile
from ssh_blog import ssh_run
result = ssh_run("mysql -h mysql.mifeco.com -u ak48bme -p7jpetxEL mifeco_com_1 -N -e \"SELECT post_title, post_name FROM wp_gryu9c_posts WHERE post_type='post' ORDER BY post_date DESC;\"")
```

## Specific Queries Used in This Workflow

### Dedup check — list all published posts
```python
result = ssh_run("""mysql -h mysql.mifeco.com -u ak48bme -p7jpetxEL mifeco_com_1 -N -e "SELECT post_title, post_name FROM wp_gryu9c_posts WHERE post_type='post' ORDER BY post_date DESC;" """)
```

### Verify specific posts by ID
```python
result = ssh_run("""mysql -h mysql.mifeco.com -u ak48bme -p7jpetxEL mifeco_com_1 -N -e "SELECT ID, post_title, post_name, post_date FROM wp_gryu9c_posts WHERE post_type='post' AND ID IN (51, 53);" """)
```