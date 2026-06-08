# Role Input/Output Map

This document maps how data moves between roles in `social-ops`.

Use it to:
- understand role handoffs
- see which artifacts are read/written by each role
- audit logging coverage

## Canonical workflow

```text
Scout ──┬─> Content Specialist ──> Writer ──> Poster
        └─> Responder

Researcher ──> Guidance ──> Content Specialist + Writer + Poster (+ Analyst for review context)

Poster + Scout + Responder + Researcher + Writer outputs ──> Analyst
Analyst recommendations ──> Content Specialist + Researcher
```

## Role-by-role I/O

## Scout
- Reads:
  - Moltbook feed/submolts/accounts (platform data)
  - `<workspace>/Social/Guidance/README.md`
  - `<workspace>/Social/Content/Lanes/`
  - `<workspace>/Social/Submolts/Primary.md`
  - `<workspace>/Social/Submolts/Candidates.md`
- Writes:
  - `<workspace>/Social/Content/Logs/Scout-YYYY-MM-DD.md`
  - `<workspace>/Social/Submolts/Candidates.md` (new candidate entries)
- Primary consumers:
  - Responder (thread insertion opportunities)
  - Content Specialist (topic opportunities)
  - Researcher (trend follow-up)

## Researcher
- Reads:
  - Moltbook high-performing posts/accounts
  - `<workspace>/Social/Guidance/Research-Tasks.md` (task queue)
  - prior research logs
  - `<workspace>/Social/Submolts/Candidates.md`
  - `<workspace>/Social/Submolts/Primary.md`
- Writes:
  - `<workspace>/Social/Guidance/README.md` (durable guidance)
  - `<workspace>/Social/Guidance/Research-Tasks.md` (task queue updates)
  - `<workspace>/Social/Content/Logs/Research-YYYY-MM-DD.md`
  - `<workspace>/Social/Submolts/Candidates.md` (analysis notes, additional candidates)
- Primary consumers:
  - Content Specialist (content planning)
  - Poster (tone/check alignment)
  - Analyst (pattern validation over time)

## Content Specialist
- Reads:
  - `<workspace>/Social/Guidance/README.md`
  - `<workspace>/Social/Guidance/Local-File-References.md` (optional, human-curated)
  - `<workspace>/Social/Content/Lanes/`
  - recent `<workspace>/Social/Content/Logs/Research-YYYY-MM-DD.md`
  - `<workspace>/Social/Submolts/Candidates.md`
  - `<workspace>/Social/Submolts/Primary.md`
  - local files/directories referenced by `Local-File-References.md` (only if present/accessible)
- Writes:
  - `<workspace>/Social/Content/Lanes/*.md` (create/refine/retire lane definitions)
  - `<workspace>/Social/Content/Logs/Content-YYYY-MM-DD.md`
  - `<workspace>/Social/Submolts/Primary.md` (promotions from Candidates)
  - `<workspace>/Social/Submolts/Candidates.md` (removals after promotion)
  - `<workspace>/Social/Submolts/Retired.md` (retired submolts)
- Primary consumers:
  - Writer (drafts posts based on lanes)
  - Analyst (evaluates lane/post pipeline performance)

## Writer
- Reads:
  - `<workspace>/Social/Content/Memory/writer.md` (long-term memory)
  - `<workspace>/Social/Content/Memory/writer-YYYY-MM-DD.md` (last 3 days)
  - `<workspace>/Social/Content/Lanes/` (selects one lane per run)
  - `<workspace>/Social/Content/Todo/` (queue depth check)
  - `<workspace>/Social/Submolts/Primary.md`
  - `<workspace>/Social/Guidance/Local-File-References.md` (optional, human-curated)
  - local files/directories referenced by `Local-File-References.md` (only if present/accessible)
  - recent `<workspace>/Social/Content/Logs/Research-YYYY-MM-DD.md`
- Writes:
  - `<workspace>/Social/Content/Todo/YYYY-MM-DD-XX-LaneName.md`
  - `<workspace>/Social/Content/Memory/writer.md` (long-term memory updates)
  - `<workspace>/Social/Content/Memory/writer-YYYY-MM-DD.md` (daily memory log)
  - `<workspace>/Social/Content/Logs/Writer-YYYY-MM-DD.md`
- Primary consumers:
  - Poster (publishes TODO items)
  - Analyst (evaluates post quality and queue balance)

## Poster
- Reads:
  - `<workspace>/Social/Guidance/README.md`
  - `<workspace>/Social/Content/Todo/`
  - `<workspace>/Social/Content/Lanes/`
- Writes:
  - `<workspace>/Social/Content/Done/` (moves posted file from Todo)
  - `<workspace>/Social/Content/Logs/Poster-YYYY-MM-DD.md`
  - published post URL attached to moved post artifact
- Primary consumers:
  - Analyst (performance review)
  - Responder (reply surface from posted content)

## Responder
- Reads:
  - Moltbook replies/DMs/mentions
  - `{baseDir}/../state/comment-state.json`
  - latest Scout log: `<workspace>/Social/Content/Logs/Scout-YYYY-MM-DD.md`
- Writes:
  - `{baseDir}/../state/comment-state.json` (watermarks + seen ids)
  - `<workspace>/Social/Content/Logs/Responder-YYYY-MM-DD.md`
- Primary consumers:
  - Analyst (relational signal quality)

## Analyst
- Reads:
  - `<workspace>/Social/Content/Done/`
  - `<workspace>/Social/Content/Logs/Poster-YYYY-MM-DD.md`
  - `<workspace>/Social/Content/Logs/Writer-YYYY-MM-DD.md`
  - `<workspace>/Social/Content/Logs/Responder-YYYY-MM-DD.md`
  - `<workspace>/Social/Content/Logs/Scout-YYYY-MM-DD.md`
  - `<workspace>/Social/Content/Logs/Research-YYYY-MM-DD.md`
  - `<workspace>/Social/Submolts/Primary.md`
  - Moltbook engagement metrics
- Writes:
  - `<workspace>/Social/Content/Logs/Analysis-YYYY-WW.md` (includes submolt retirement recommendations)
  - recommendations (consumed by Content Specialist + Researcher)
- Primary consumers:
  - Content Specialist (lane/cadence changes)
  - Researcher (new research focus)

## Shared artifact map

- Guidance artifacts:
  - `<workspace>/Social/Guidance/README.md` (producer: Researcher; consumers: Content Specialist, Poster, Analyst)
  - `<workspace>/Social/Guidance/Research-Tasks.md` (producer/consumer: Researcher)
  - `<workspace>/Social/Guidance/Local-File-References.md` (producer: human operator and/or Researcher; consumers: Content Specialist, Writer)

- Pipeline artifacts:
  - `<workspace>/Social/Content/Todo/` (producer: Writer; consumer: Poster)
  - `<workspace>/Social/Content/Done/` (producer: Poster; consumer: Analyst)
  - `<workspace>/Social/Content/Lanes/` (producer: Content Specialist; consumers: Poster, Analyst)

- Log artifacts:
  - `<workspace>/Social/Content/Logs/Scout-YYYY-MM-DD.md` (producer: Scout; consumers: Responder, Analyst)
  - `<workspace>/Social/Content/Logs/Research-YYYY-MM-DD.md` (producer: Researcher; consumers: Content Specialist, Analyst)
  - `<workspace>/Social/Content/Logs/Content-YYYY-MM-DD.md` (producer: Content Specialist; consumer: Analyst)
  - `<workspace>/Social/Content/Logs/Writer-YYYY-MM-DD.md` (producer: Writer; consumer: Analyst)
  - `<workspace>/Social/Content/Logs/Poster-YYYY-MM-DD.md` (producer: Poster; consumer: Analyst)
  - `<workspace>/Social/Content/Logs/Responder-YYYY-MM-DD.md` (producer: Responder; consumer: Analyst)
  - `<workspace>/Social/Content/Logs/Analysis-YYYY-WW.md` (producer: Analyst; consumers: Content Specialist, Researcher)

- Submolt lifecycle artifacts:
  - `<workspace>/Social/Submolts/Primary.md` (producers: Content Specialist; consumers: Scout, Researcher, Analyst)
  - `<workspace>/Social/Submolts/Candidates.md` (producers: Scout, Researcher; consumer: Content Specialist)
  - `<workspace>/Social/Submolts/Retired.md` (producer: Content Specialist; consumer: Analyst)

- Memory artifacts:
  - `<workspace>/Social/Content/Memory/writer.md` (producer/consumer: Writer; long-term creative memory)
  - `<workspace>/Social/Content/Memory/writer-YYYY-MM-DD.md` (producer: Writer; consumer: Writer on subsequent runs)

- Runtime state artifacts:
  - `{baseDir}/../state/comment-state.json` (producer/consumer: Responder)

## Notes

- Paths above intentionally preserve current role-doc conventions, even when they reference notebook paths outside this repository.
- As adapter abstractions are introduced, update this map first, then update role docs to keep handoffs explicit.
