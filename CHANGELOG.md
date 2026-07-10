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

## Run 6 — 2026-07-09

- Acquisition probes (promisor-clone technique from Run 5): Smithsonian/OpenAccess — data removed from GitHub, S3 host egress-blocked, dead; MoMA/collection — all data files are LFS pointers, dead; cmoa/collection — repo gone (404); tategallery/collection — 69,202 artwork JSON files as PLAIN blobs, CC0 1.0, acquisition WORKS.
- Data-source pivot Met → Tate recorded in DECISIONS.md (Met acquisition impossible; Tate is CC0, plain-blob, and itself a neglected frozen-2014 artifact).
- Built `experiments/tate_convert.py` (stdlib-only): converts Tate artwork JSON to the met_tail JSONL schema (field mapping documented in the script; subjects-tree leaves → tags; classification → department; isHighlight=False recorded as a mapping limitation).
- Added `experiments/tate_sample.jsonl`: 290 REAL CC0 records (4 accession-prefix directories, commit a51d8af). `met_tail.py` verified unchanged against real data: tail, share, tags, tags --rare, show, and date filters all work. The fixture is no longer the only data.

## Run 7 — 2026-07-09

- Scaled real data ~12x: `experiments/tate_stratified.jsonl` — 3,458 CC0 records (2.4 MB), a deterministic stratified sample (every 20th of 738 artwork subdirs at pinned commit a51d8af, proportional across all 6 accession prefixes). Chose the JSON route over artwork_data.csv because the CSV lacks the subjects tree that feeds tags/--rare.
- Added `experiments/tate_fetch.sh`: regenerates the sample byte-for-byte (verified by diff) via blob:none clone + sparse-checkout; `STRIDE=1` fetches the full 69,202-record collection.
- Verified met_tail.py at scale: share (70% Turner-Bequest "on paper, unique"), tags (2,595 distinct), tags --rare (1,345 singletons, 52% — the long-tail story), tail/show/date/department filters, reproducible --seed. Findings in RESEARCH_LOG.md.
