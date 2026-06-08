SaaS Stack (2026-06-07): 3 products on Cloud Run. MIFECO VibraEngineer ($19/mo, Intelligent-Engineer repo, port 3001), MIFECO PM Accelerator ($29/mo, Project-management-accelerator repo, port 3002), MIFECO Hypatia Pro ($29/mo, HypatiaPro repo, port 3003). Free/pro tiers + Stripe scaffold. "MIFECO" prefix ensures uniqueness. Start: ~/start-mifeco-saas.sh. FL-Hermes private repo for GitHub backup. Nightly backup cron cf9aad854695. SaaS GitHub backup cron 66b8c9411afe. WordPress integration at mifeco.com with /hypatia, /accelerator, /vibraengineer pages.
§
MIFECO Virtual Consulting Credentials: SSH/SFTP, MySQL, Stripe (placeholders), Python API, backdoor login, file paths, site URLs. MemPalace Event ID: f1dd1327-83e7-49a4-a3c4-45171c1c94c8
§
MemPalace System: Storage at ~/.hermes/mempalace/, FAISS index (384-dim, IndexFlatIP), embedding model all-MiniLM-L6-v2, search via embed.search_embeddings(query, k=5), modules: capture.py, tag.py, embed.py
§
2026-07-03 Skills disabled 90/202 to reduce system prompt tokens from ~5,704 to ~3,634 (-36%). Disabled ML ops, gaming, social media, email, red teaming, reference profiles, heavy dev workflows. Configured via yaml module (not hermes config set which mangles JSON-in-YAML). Skills snapshot cache cleared; gateway restart needed from shell.
§
Memory management: When MEMORY.md gets full (near 2,200 char limit), offload to MemPalace. Don't keep shrinking entries. Use: import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace')); import embed; embed.init_embedding(...); embed.add_entry(text, tags=[...]). Always compact memory entries before adding new ones.
§
2026-07-03: Created FL-Hermes private GitHub backup repo (Robertstar2000/FL-Hermes). Backed up config (redacted), skills, mempalace, memories, scripts, cron jobs. .env excluded. SSH push works. gh CLI v2.83.0 installed at ~/.local/bin/gh. Added hermes-backup-pattern.md reference to github-repo-management skill.