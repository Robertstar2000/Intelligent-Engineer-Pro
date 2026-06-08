MIFECO Virtual Consulting Pipeline: Complete system architecture - PHP on DreamHost + Python API, Stripe payments, survey state machine, IDK branching, deployment procedures, file paths. MemPalace Event ID: d20a43cc-c6a4-4f47-b7c4-7699dbfa6a2f
§
MIFECO Virtual Consulting Credentials: SSH/SFTP, MySQL, Stripe (placeholders), Python API, backdoor login, file paths, site URLs. MemPalace Event ID: f1dd1327-83e7-49a4-a3c4-45171c1c94c8
§
MemPalace System: Storage at ~/.hermes/mempalace/, FAISS index (384-dim, IndexFlatIP), embedding model all-MiniLM-L6-v2, search via embed.search_embeddings(query, k=5), modules: capture.py, tag.py, embed.py
§
2026-07-03: Skill updates made — (1) hermes-agent-operations: added MEMORY.md drift pitfall — never use write_file/patch on MEMORY.md or USER.md, only the memory tool. (2) mempalace-vector-integration: rewrote to match live stack (faiss-cpu + sentence-transformers + embed.py), replaced stale ONNX/ChromaDB docs.
§
2026-07-03 Skills disabled 90/202 to reduce system prompt tokens from ~5,704 to ~3,634 (-36%). Disabled ML ops, gaming, social media, email, red teaming, reference profiles, heavy dev workflows. Configured via yaml module (not hermes config set which mangles JSON-in-YAML). Skills snapshot cache cleared; gateway restart needed from shell.
§
2026-07-03 Key learnings: (1) NEVER use write_file/patch on MEMORY.md or USER.md — only the memory tool. (2) NEVER use `hermes config set` for list values — it mangles JSON-in-YAML. Use yaml.safe_load/dump directly. (3) Patch tool can leave orphaned code — always verify after edits. (4) Stored 220 skills in MemPalace (267 FAISS vectors), disabled 91 for -36% token savings. (5) auto_nap() adaptive cron ticker implemented. (6) skill-finder skill + weekly cron created. (7) Bob prefers concise, direct responses — no fluff.
§
GitHub access: user Robertstar2000, SSH key id_ed25519 works. 29 repos visible via API. gh CLI v2.83.0 installed at ~/.local/bin/gh (not authenticated — needs PAT for gh auth). API access works via curl. Key repos: TallmanZero (Python/agent), Tallman-LMS, mifeco_web, Hypatia, BOBnet, MIFECO_Web_php.