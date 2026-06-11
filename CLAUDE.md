# CLAUDE.md — pfuzz

This repo uses **dev-docs v4.0 (Project Memory OS)**. Before working:

1. Read `dev-docs/AI-INSTRUCTIONS.md` and `dev-docs/PROJECT-MEMORY.md`.
2. Read the relevant `dev-docs/modules/*.md`.
3. Prefer a context pack: `node dev-docs/bin/devdocs.mjs context <module> --task "..."`.

Key rules:
- Python package dir is `pfuzz/` (CLI command `pfuzz`). Keep ps-fuzz credits (MIT fork).
- Never change attack payloads or scoring silently — record a DECISION.
- Bilingual EN/PT-BR product; translate UX, never attack payloads.
- `dev-docs/` is gitignored (local-first memory).

Maintainer: Osvaldo Janeri Filho.
