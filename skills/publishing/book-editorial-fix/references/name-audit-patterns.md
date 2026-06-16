# Name Audit Patterns

## Common Name Inconsistency Patterns Found

### Multi-Variant Surname Problem
Characters often appear with 3-5 surname variants across a manuscript:

| Character | Variants Found | Canonical |
|-----------|---------------|-----------|
| Patricia | Chen, Zhào, Varma, Osei, Okonkwo | Okonkwo |
| Elena | Varga, Vargas, Chen | Varga |
| James | Reeves, Kovacs | Kovacs |
| Robert | Chen, Kanake | Chen (lunar), Kanake (separate?) |
| David | Chen, Okafor | Okafor (Ops Director) |

### Detection Script
```bash
# For each character, audit ALL surname variants
for surname in Chen Vargas Varma Zhào Osei Okonkwo Reeves Kovacs Kanake Okafor; do
  echo "$surname: $(grep -ic "$surname" MANUSCRIPT.md)"
done
```

### Cross-Book Consistency
| Book Series | Character | Book 1 | Book 2 | Book 3 | Book 4 | Canonical |
|-------------|-----------|--------|--------|--------|--------|-----------|
| NBS | Elena | Varga | Varga | — | Vargas | Chen | Varga |
| AoLS | Patricia | Chen | Okonkwo | — | Okonkwo | — | Okonkwo |
| LF | Tom | Chen | Chen | Chen | Chen | Chen |
| LF | James | Okonkwo | Okonkwo | Okonkwo | Okonkwo | Okonkwo |

### Fix Protocol

1. **Full Audit First**
   ```bash
   grep -rn "Patricia" MANUSCRIPT.md | sort -u
   grep -rn "Elena" MANUSCRIPT.md | sort -u
   ```

2. **Replace with Word Boundaries**
   ```bash
   sed -i 's/\bPatricia Chen\b/Patricia Okonkwo/g' MANUSCRIPT.md
   sed -i 's/\bPatricia Zhào\b/Patricia Okonkwo/g' MANUSCRIPT.md
   sed -i 's/\bPatricia Varma\b/Patricia Okonkwo/g' MANUSCRIPT.md
   sed -i 's/\bPatricia Osei\b/Patricia Okonkwo/g' MANUSCRIPT.md
   ```

3. **Verify Zero Old, Correct New**
   ```bash
   grep -c "Patricia Chen\|Patricia Zhào\|Patricia Varma\|Patricia Osei" MANUSCRIPT.md  # Must be 0
   grep -c "Patricia Okonkwo" MANUSCRIPT.md  # Should equal expected total
   ```

### Merge Artifacts to Watch For

| Artifact | Example | Cause |
|----------|---------|-------|
| First + Last from different chars | "Patricia Osei" (Patricia + Amara Osei) | Name fix applied to wrong occurrence |
| Surname from Book N in Book M | "David Chen" (should be Okafor) | Copy-paste from another book |
| Accented variants | "Zhào" vs "Zhao" | Encoding inconsistency |

### Prevention
- Always search for ALL known variants before replacing
- Use `\b` word boundaries in sed
- After fixing, re-run the FULL audit including partial matches
- Cross-check with series bible for canonical names