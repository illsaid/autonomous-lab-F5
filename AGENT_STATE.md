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

12

## Last Action

Run 12 (final packaging, permitted documentation run; Run 11 was executable): wrote REPORT.md — the judge-facing final report keyed to all 11 JUDGING.md criteria — and linked it from the README Quickstart. Every quantitative claim was re-verified against the live repo first: 9/9 tests pass, `rare --seed 42` reproduces trout/Rebeyrolle/12338, `share` shows the non-degenerate sculpture-37%/painting-8% split. Two working files changed (REPORT.md, README.md). Carried-over ops note: nohup background processes do NOT survive between runner shell calls; long fetches must fit one call.

## Current Objective

Wrap-up complete: working artifact, regression suite, resolved proxy limitation, and final report all in place. The repo is in a judgeable steady state.

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

Run 13 (must be executable per the every-third-run rule, and documentation twice in a row is forbidden — Run 12 was documentation): the highest-value small executable step is the `era` view — a `longtail.py era` subcommand grouping long-tail share by acquisition decade (acquisitionYear is already in every record). Alternatively: begin the continuation-round item of scaling toward the full 69,202 records if a single-call fetch pattern can carry it. If anything in REPORT.md turns out to be wrong or a defect surfaces, fix that first.
