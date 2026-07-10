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

## Run 4 — 2026-07-09

- Research/direction run (documentation-only; Run 3 was executable). Read the Met Collection API reference at full depth; recorded ~10 concrete design facts in RESEARCH_LOG.md (no key, 80 req/s, 471,581 objects, machine-readable dates, AAT/Wikidata/ULAN links, search filters, 19 department IDs).
- DECISIONS.md: designated "long-tail explorer over CC0 GLAM metadata (Met first)" the leading candidate direction, with evidence, a 3-question concrete sketch, next build step, and an explicit pivot condition. Not a narrowing; other categories stay open.
- Key acquisition insight for Run 5: the Met bulk CSV lives on github.com — the only domain inside the runner's egress allowlist.

## Run 5 — 2026-07-09

- Acquisition test (negative, definitive): MetObjects.csv is unreachable from the runner by all 4 routes tried — ranged raw fetch (403 blocked-by-allowlist), LFS batch API (reachable on github.com, but download href points to github-cloud.githubusercontent.com, blocked), direct byte fetch (connection refused by allowlist), and historical plain-blob fetch (entire history is LFS-migrated pointers, verified back to the 2016 first commits via promisor clone). Live API confirmed unreachable from assistant tooling as well. Details in RESEARCH_LOG.md.
- Built `experiments/met_tail.py`: stdlib-only query CLI for the long-tail direction — `tail` (random never-highlighted public-domain objects with department/date filters), `share` (per-department long-tail share), `tags` (frequency + `--rare` one-off tags), `show`. All subcommands tested.
- Added `experiments/met_fixture.jsonl`: 12 records in Met Collection API schema — 1 real CC0 record (objectID 45734, from the API docs; noted in THIRD_PARTY_NOTICES.md) + 11 synthetic records marked `"fixture": true` and titled "Fixture: …".
