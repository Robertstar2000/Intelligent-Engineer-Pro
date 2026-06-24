## Structured summary (required)
```yaml
consolidations:
  - from: github-auth
    into: github
    reason: GitHub authentication is a subsection of the GitHub workflow umbrella; content merged into github/SKILL.md and references/
  - from: github-code-review
    into: github
    reason: Code review is a subsection of the GitHub workflow umbrella; content preserved in references/ and templates/
  - from: github-issues
    into: github
    reason: Issue management is a subsection of the GitHub workflow umbrella; content preserved in references/ and templates/
  - from: github-pr-workflow
    into: github
    reason: PR lifecycle is a subsection of the GitHub workflow umbrella; content preserved in references/ and templates/
  - from: github-repo-management
    into: github
    reason: Repository management is a subsection of the GitHub workflow umbrella; content preserved in references/
  - from: python-debugpy
    into: systematic-debugging
    reason: Python debugging (pdb/debugpy) is a tool-specific extension of the systematic debugging methodology; content moved to references/
  - from: node-inspect-debugger
    into: systematic-debugging
    reason: Node.js inspect debugging is a tool-specific extension of systematic debugging; content moved to references/
  - from: simplify-code
    into: systematic-debugging
    reason: Parallel 3-agent code cleanup is a code quality process that belongs under the debugging/quality umbrella; content moved to references/
  - from: requesting-code-review
    into: systematic-debugging
    reason: Pre-commit code verification is a quality gate process that belongs under the debugging/quality umbrella; content moved to references/
  - from: spike
    into: systematic-debugging
    reason: Throwaway experiments for feasibility validation are part of the debugging/research workflow; content moved to references/
  - from: architecture-diagram
    into: creative-visual-arts
    reason: Architecture diagrams are a visual/creative output; content moved to references/ under the new creative umbrella
  - from: ascii-art
    into: creative-visual-arts
    reason: ASCII art generation is a creative content tool; content moved to references/
  - from: ascii-video
    into: creative-visual-arts
    reason: ASCII video production is a creative/visual tool; content moved to references/
  - from: excalidraw
    into: creative-visual-arts
    reason: Excalidraw diagram generation is a visual content tool; content moved to references/ with support files
  - from: humanizer
    into: creative-visual-arts
    reason: Text humanization is a creative writing tool; content moved to references/
  - from: baoyu-infographic
    into: creative-visual-arts
    reason: Infographic generation is a visual content tool; content moved to references/ with support files
  - from: p5js
    into: creative-visual-arts
    reason: p5.js generative art is a creative coding tool; content moved to references/
  - from: manim-video
    into: creative-visual-arts
    reason: Manim math animations are a creative/video tool; content moved to references/ with support files
  - from: comfyui
    into: creative-visual-arts
    reason: ComfyUI image/video/audio generation is a creative generative tool; content moved to references/
  - from: pretext
    into: creative-visual-arts
    reason: Pretext typography demos are a creative coding tool; content moved to references/
  - from: design-md
    into: creative-visual-arts
    reason: DESIGN.md token spec authoring is a design tool; content moved to references/ with templates
  - from: popular-web-designs
    into: creative-visual-arts
    reason: Web design system templates are a visual design resource; content moved to references/ with all templates
  - from: sketch
    into: creative-visual-arts
    reason: HTML mockup sketches are a creative prototyping tool; content moved to references/
  - from: claude-design
    into: creative-visual-arts
    reason: Claude design process skill is a creative workflow tool; content moved to references/
  - from: book-editorial-fix
    into: book-editorial-review
    reason: Editorial fix workflow is a subsection of the book editorial pipeline; content moved to references/
  - from: business-book-production
    into: book-editorial-review
    reason: Business book production is a publishing pipeline that shares the editorial workflow; content moved to references/
  - from: reader-magnet-production
    into: book-editorial-review
    reason: Reader magnet production is a publishing workflow that shares the editorial pipeline; content moved to references/
  - from: mifeco-pipeline-management
    into: mifeco-business-audit
    reason: Pipeline management is a data source for business audit; content moved to references/
  - from: hermes-agent-daily-briefing
    into: hermes-agent-skill-authoring
    reason: Daily briefing generation is a Hermes agent operation that belongs under the agent skill umbrella; content moved to references/
  - from: kanban-worker
    into: kanban-orchestrator
    reason: Kanban worker pitfalls are a subsection of the kanban orchestration workflow; content moved to references/
  - from: codex
    into: hermes-agent
    reason: Codex CLI delegation is an autonomous coding agent pattern that belongs under the agent umbrella; content moved to references/
  - from: opencode
    into: hermes-agent
    reason: OpenCode CLI delegation is an autonomous coding agent pattern; content moved to references/
  - from: airtable
    into: productivity-suite
    reason: Airtable integration is a productivity tool; content moved to references/
  - from: notion
    into: productivity-suite
    reason: Notion integration is a productivity tool; content moved to references/
  - from: nano-pdf
    into: productivity-suite
    reason: PDF editing is a productivity tool; content moved to references/
  - from: ocr-and-documents
    into: productivity-suite
    reason: Document extraction is a productivity tool; content moved to references/ with scripts
  - from: powerpoint
    into: productivity-suite
    reason: PowerPoint creation/editing is a productivity tool; content moved to references/
  - from: google-workspace
    into: productivity-suite
    reason: Google Workspace integration is a productivity tool; content moved to references/ with scripts
  - from: teams-meeting-pipeline
    into: productivity-suite
    reason: Teams meeting pipeline is a productivity tool; content moved to references/
  - from: obsidian
    into: productivity-suite
    reason: Obsidian vault management is a productivity/note-taking tool; content moved to references/
  - from: gif-search
    into: productivity-suite
    reason: GIF search is a media productivity tool; content moved to references/
prunings:
  - name: apple-notes
    reason: Disabled skill, unsupported on Linux, never used (activity=0)
  - name: apple-reminders
    reason: Disabled skill, unsupported on Linux, never used (activity=0)
  - name: imessage
    reason: Disabled skill, unsupported on Linux, never used (activity=0)
  - name: findmy
    reason: Disabled skill, unsupported on Linux, never used (activity=0)
  - name: claude-code
    reason: Disabled skill, never used (activity=0)
  - name: llama-cpp
    reason: Disabled skill, never used (activity=0)
  - name: huggingface-hub
    reason: Disabled skill, never used (activity=0)
  - name: weights-and-biases
    reason: Disabled skill, never used (activity=0)
  - name: test-driven-development
    reason: Disabled skill, never used (activity=0)
  - name: songsee
    reason: Disabled skill, never used (activity=0)
  - name: songwriting-and-ai-music
    reason: Disabled skill, never used (activity=0)
  - name: llm-wiki
    reason: Disabled skill, never used (activity=0)
  - name: openhue
    reason: Disabled skill, never used (activity=0)
  - name: polymarket
    reason: Disabled skill, never used (activity=0)
  - name: godmode
    reason: Disabled skill, never used (activity=0)
  - name: heartmula
    reason: Disabled skill, never used (activity=0)
  - name: obliteratus
    reason: Disabled skill, never used (activity=0)
  - name: xurl
    reason: Disabled skill, never used (activity=0)
  - name: blogwatcher
    reason: Disabled skill, never used (activity=0)
  - name: arxiv
    reason: Disabled skill, never used (activity=0)
  - name: touchdesigner-mcp
    reason: Disabled skill, never used (activity=0)
  - name: books-website
    reason: Disabled skill, low activity (use=10), website management better handled by other skills
  - name: research-paper-writing
    reason: Never used (activity=0, use=0), ML paper writing not a current domain need
```
