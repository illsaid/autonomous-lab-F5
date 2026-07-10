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

## Run 8 — 2026-07-09

- Added `rare` subcommand to `experiments/met_tail.py`: the neglected-artifact generator. Picks one random singleton tag (deterministic with `--seed`) and prints the lone artwork carrying it, including its tate.org.uk URL — the project mission demonstrated in one command.
- Tested: reproducible with `--seed 42` (tag "trout" → Rebeyrolle, *Trout*, 1956), random without seed, correct counts at scale (2,595 tags / 1,345 singletons on the 3,458-record stratified sample), graceful on tag-free data, works on the fixture; `tail`, `share`, `tags --rare` re-verified unchanged.
- No new data sources (per Run-7 convergence plan). One working file changed.

## Run 9 — 2026-07-09

- Promoted the CLI: `experiments/met_tail.py` → `longtail.py` at repo root (git mv, source-neutral name). DEFAULT_DATA now points at `experiments/tate_stratified.jsonl`, so `python3 longtail.py rare` works with zero arguments immediately after clone.
- Rewrote the README opening around a Quickstart: clone → `python3 longtail.py rare` → one neglected artwork with a live Tate URL; listed the other views and the fetch/scale script.
- Rename + rationale recorded in DECISIONS.md. All subcommands re-tested post-move: rare (seeded and random), tail, share, tags, show, and --data override with the Met fixture.

## Run 10 — 2026-07-10

- Added `tests/test_longtail.py` (stdlib-only, unittest): 8 regression tests pinning known-good behavior — 3,458 records load from the default data, 2,595 distinct tags / 1,345 singletons, `rare --seed 42` reproduces trout/Rebeyrolle/12338, `show 12338` returns valid JSON with accession T00116, seeded `tail` runs, missing objectID exits nonzero, `--data` override works with the Met fixture, and piped output survives a closed pipe. Run with `python3 tests/test_longtail.py`. All pass.
- Fixed a real defect found while writing the tests: `python3 longtail.py tags | head` died with BrokenPipeError; longtail.py now restores default SIGPIPE handling (POSIX only, guarded with hasattr).

## Run 11 (2026-07-10)

- Highlight proxy fixed: `tate_convert.py` now sets `isHighlight = bool(thumbnailUrl)`; `experiments/tate_stratified.jsonl` regenerated (2,902 head / 556 never-photographed tail). `share` is no longer a degenerate 100% column.
- Proxy validated against raw artwork JSON (199/199 agree) at pinned commit a51d8af; see DECISIONS.md Run 11.
- New regression test pins the 2,902/556 split (9 tests total, all passing).

## Run 12 (2026-07-10)

- Final packaging: added `REPORT.md`, a judge-facing report keyed to the 11 JUDGING.md criteria — what the repo became, the demo, at-scale findings, the acquisition dead-end story, license hygiene, honest limitations, and a continuation sketch. All quantitative claims re-verified against the live repo before writing (9 tests OK, seeded `rare` reproduces, `share` non-degenerate).
- README links the report from the Quickstart section.

## Run 13 (2026-07-10)

- New `era` subcommand: long-tail share by acquisition decade. Tate records carry no acquisition-year field (a prior AGENT_STATE note wrongly said they did); the year is parsed from creditLine (last plausible 4-digit year), covering 3,458/3,458 default records.
- Finding: unphotographed share is ~0–3% for 1980s–90s acquisitions but 37% for the 2000s and 84% for the 2010s — in the frozen Oct 2014 snapshot, photography lags acquisition; the newest works are the least visible.
- Regression test added pinning the 1850s row (1885 total / 261 long-tail / 14%) and the creditLine parser; suite is now 10 tests, all passing.

## Run 14 (2026-07-10)

- Documentation touch (allowed after executable Run 13): README now lists the `era` view in the Quickstart views block; REPORT.md updated to current behavior — six subcommands, 10 regression tests, the era finding (photography lags acquisition: 2010s works 84% never-photographed vs <=3% for 1980s-90s) added to Usefulness, and `era` removed from the continuation sketch since it shipped in Run 13.
- No code changes; test suite re-verified (10 tests OK).

## Run 15 (2026-07-10)

- `--json` flag added to `share`, `era`, and `rare`: machine-readable output (arrays/objects with department/decade totals, long-tail counts, shares; `rare --json` includes the full record). Enables piping into jq and downstream tools.
- Three regression tests pin the JSON shapes (share sums to the 2,902/556 split, era 1850s row, seed-42 rare pick); suite is now 13 tests, all passing.
- Suggested STRIDE scale-up deferred (exceeds one-run budget; needs atomic re-pin of all count tests) — recorded in AGENT_STATE.md.
