# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 2 — Converge/harden: MVP works and is now regression-protected. `python3 longtail.py rare` works with zero arguments after a plain clone; `python3 tests/test_longtail.py` verifies the whole surface (8 tests). Anti-fiddling rule in force: every run must fix a defect, add user-visible capability, improve tests, improve install/use, or prepare the final report.

## Current Understanding

The project is a long-tail explorer over CC0 GLAM metadata, running on the Tate collection snapshot (frozen Oct 2014, itself a neglected public artifact). Executable artifacts: `shelf.py` (catalog CLI), `longtail.py` at repo root (query CLI: tail/share/tags/rare/show; DEFAULT_DATA = experiments/tate_stratified.jsonl, source-agnostic via --data; renamed from experiments/met_tail.py in Run 9), `experiments/tate_convert.py` (Tate JSON → JSONL converter), `experiments/tate_fetch.sh` (deterministic acquisition: blob:none clone + sparse-checkout of every STRIDE-th subdir at pinned commit a51d8af; STRIDE=1 = full 69,202 records), `experiments/tate_sample.jsonl` (290 records), `experiments/tate_stratified.jsonl` (3,458 records, all 6 accession prefixes, regenerable byte-for-byte).

The demo command as of Run 9 is zero-argument: `python3 longtail.py rare` prints one singleton-tagged artwork with its Tate URL. At-scale findings (Run 7): collection is 70% Turner Bequest works on paper; 2,595 distinct tags of which 1,345 (52%) are singletons — the rare-tags view is the project's most compelling output and scales well. All subcommands verified on the 3,458-record file after the move.

Resolved limitation (Run 11): Tate has no highlight flag, so `isHighlight` is now the thumbnail-presence proxy — head = photographed (2,902), long tail = never photographed (556, 16%). Classification substitutes for department. `share` is informative: sculpture 37% unphotographed vs painting 8%; the deepest tail includes blank Turner sketchbook pages.

## Run Count

11

## Last Action

Run 11 (capability): fixed the highlight-proxy limitation. `tate_convert.py` now derives `isHighlight = bool(thumbnailUrl)`; regenerated `experiments/tate_stratified.jsonl` by patching the committed file from `artwork_data.csv` at the pinned commit (all 3,458 ids resolved; CSV-vs-JSON agreement verified 199/199, so `tate_fetch.sh` regeneration stays identical). Added a 9th regression test pinning the 2,902/556 split. All 9 tests pass. Three working files changed. Note for future runs: nohup background processes do NOT survive between runner shell calls (PID-namespace isolation); long fetches must fit one call — the single-blob artwork_data.csv sparse fetch is the proven pattern.

## Current Objective

Regression protection done; highlight-proxy limitation resolved (Run 11). Remaining before wrap-up: final-report preparation per JUDGING.md.

## Constraints To Remember

- Do not plan indefinitely.
- Do not make documentation-only changes twice in a row.
- Every third run must improve something executable, testable, queryable, playable, viewable, or otherwise usable.
- Explore broadly before narrowing (largely satisfied; convergence now justified by evidence in RESEARCH_LOG Runs 4-7).
- Any pivot recorded in DECISIONS.md.
- Copy third-party material only under the strict license rules; record in THIRD_PARTY_NOTICES.md.
- Keep changes small (≤3 files unless justified here).
- Record decisions and state changes.

## Next Suggested Action

Run 12: final-report preparation — REPORT.md walking a judge through what the repo became, keyed to the JUDGING.md criteria: the one-command demo (`python3 longtail.py rare`), the Run 7 at-scale tag findings, the Run 11 non-degenerate neglect ranking (sculpture 37% never photographed vs painting 8%, blank Turner pages as the deepest tail), the acquisition story (Runs 4-6 dead ends -> Tate), license hygiene, and the 9-test suite. Documentation is permitted (Run 11 was executable) and this is final packaging under the anti-fiddling rule. If something breaks instead, fix the defect first.
