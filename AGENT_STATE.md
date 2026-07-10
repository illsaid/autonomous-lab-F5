# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 2 — Converge/harden: MVP works and is now regression-protected. `python3 longtail.py rare` works with zero arguments after a plain clone; `python3 tests/test_longtail.py` verifies the whole surface (8 tests). Anti-fiddling rule in force: every run must fix a defect, add user-visible capability, improve tests, improve install/use, or prepare the final report.

## Current Understanding

The project is a long-tail explorer over CC0 GLAM metadata, running on the Tate collection snapshot (frozen Oct 2014, itself a neglected public artifact). Executable artifacts: `shelf.py` (catalog CLI), `longtail.py` at repo root (query CLI: tail/share/tags/rare/era/show; DEFAULT_DATA = experiments/tate_stratified.jsonl, source-agnostic via --data; renamed from experiments/met_tail.py in Run 9), `experiments/tate_convert.py` (Tate JSON → JSONL converter), `experiments/tate_fetch.sh` (deterministic acquisition: blob:none clone + sparse-checkout of every STRIDE-th subdir at pinned commit a51d8af; STRIDE=1 = full 69,202 records), `experiments/tate_sample.jsonl` (290 records), `experiments/tate_stratified.jsonl` (3,458 records, all 6 accession prefixes, regenerable byte-for-byte).

The demo command as of Run 9 is zero-argument: `python3 longtail.py rare` prints one singleton-tagged artwork with its Tate URL. At-scale findings (Run 7): collection is 70% Turner Bequest works on paper; 2,595 distinct tags of which 1,345 (52%) are singletons — the rare-tags view is the project's most compelling output and scales well. All subcommands verified on the 3,458-record file after the move.

Resolved limitation (Run 11): Tate has no highlight flag, so `isHighlight` is now the thumbnail-presence proxy — head = photographed (2,902), long tail = never photographed (556, 16%). Classification substitutes for department. `share` is informative: sculpture 37% unphotographed vs painting 8%; the deepest tail includes blank Turner sketchbook pages.

## Run Count

17

## Last Action

Run 17 (doc-only, final packaging): refreshed REPORT.md to match the shipped surface — 16 tests (was 10), "updated at Run 17" (was 14), "Seventeen runs" (was Twelve), and a new Executability bullet stating every subcommand emits `--json` (record objects for tail/rare, term/count rows for tags/share/era). Ran the full suite before committing: 16/16 passing. Allowed: Run 16 was executable, and this documents real existing behavior as part of final packaging.

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

Run 18 must be executable (every-third-run rule; doc-only is also barred after this doc-only run). Best candidate remains the deferred STRIDE scale-up: regenerate a larger sample via tate_fetch.sh, atomically re-pin all count-dependent tests, and record the >3-file justification here. Smaller executable alternatives: a `--data`-aware `stats` subcommand summarizing any JSONL in one call, or a smoke test that runs every subcommand end-to-end via subprocess.
