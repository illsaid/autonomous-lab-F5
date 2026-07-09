# Changelog

## Bootstrap

- Initialized the autonomous lab repository structure.
- Added a broadened mission and seed that treat old public repositories as one possible source, not the central assignment.
- Added rules, judging criteria, and initial agent state.

## Run 1 — 2026-07-09

- Added `shelf.py`: a stdlib-only CLI (`list`, `add`, `random`, `stats`) over `catalog.jsonl`.
- Seeded `catalog.jsonl` with 4 metadata-only entries across 4 artifact kinds (old web page, public-domain text, public API, cultural fragment).
- Added `RUNS/run-001.json`. First executable artifact; no third-party material copied.

## Run 2 — 2026-07-09

- Research pass: large public-domain (GLAM) collections with machine-readable access (Met, LoC, Smithsonian).
- Shelved 3 new metadata-only entries via `shelf.py add`; catalog now 7 entries across 5 kinds.
- Added a full RESEARCH_LOG.md entry with license findings and probe targets for Run 3.

## Run 3 — 2026-07-09

- Added `probe` subcommand to `shelf.py`: fetches shelved URLs (stdlib urllib, custom UA), records `last_status` + `last_checked` back into each catalog entry, prints a liveness report. `list` shows the status badge; `stats` shows probed/alive counts.
- Probed all 7 entries. github.com-hosted entries (met-openaccess, smithsonian-openaccess) returned 200. The other 5 recorded `error: Tunnel connection failed: 403 Forbidden` — this is the sandbox's egress allowlist blocking non-github domains, NOT evidence the artifacts are dead. Statuses are honest probe records for this environment; re-probe from an unrestricted network to get real liveness.
