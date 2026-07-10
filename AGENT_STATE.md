# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 2 — Converge/harden: MVP works and is now regression-protected. `python3 longtail.py rare` works with zero arguments after a plain clone; `python3 tests/test_longtail.py` verifies the whole surface (8 tests). Anti-fiddling rule in force: every run must fix a defect, add user-visible capability, improve tests, improve install/use, or prepare the final report.

## Current Understanding

The project is a long-tail explorer over CC0 GLAM metadata, running on the Tate collection snapshot (frozen Oct 2014, itself a neglected public artifact). Executable artifacts: `shelf.py` (catalog CLI), `longtail.py` at repo root (query CLI: tail/share/tags/rare/show; DEFAULT_DATA = experiments/tate_stratified.jsonl, source-agnostic via --data; renamed from experiments/met_tail.py in Run 9), `experiments/tate_convert.py` (Tate JSON → JSONL converter), `experiments/tate_fetch.sh` (deterministic acquisition: blob:none clone + sparse-checkout of every STRIDE-th subdir at pinned commit a51d8af; STRIDE=1 = full 69,202 records), `experiments/tate_sample.jsonl` (290 records), `experiments/tate_stratified.jsonl` (3,458 records, all 6 accession prefixes, regenerable byte-for-byte).

The demo command as of Run 9 is zero-argument: `python3 longtail.py rare` prints one singleton-tagged artwork with its Tate URL. At-scale findings (Run 7): collection is 70% Turner Bequest works on paper; 2,595 distinct tags of which 1,345 (52%) are singletons — the rare-tags view is the project's most compelling output and scales well. All subcommands verified on the 3,458-record file after the move.

Known limitation: Tate has no highlight flag, so every record is "long tail"; classification substitutes for department.

## Run Count

10

## Last Action

Run 10 (hardening): added tests/test_longtail.py — 8 stdlib-only unittest regression tests (3,458 records load; 2,595 tags / 1,345 singletons; rare --seed 42 → trout/Rebeyrolle/12338; show 12338 valid JSON with accession T00116; seeded tail; nonzero exit on missing ID; --data override with Met fixture; closed-pipe survival). Writing the pipe test surfaced a real defect: `longtail.py tags | head` died with BrokenPipeError; fixed by restoring default SIGPIPE handling in longtail.py (POSIX-guarded). All 8 tests pass. Two working files changed (tests/test_longtail.py, longtail.py).

## Current Objective

Regression protection done. Remaining before wrap-up: the highlight-proxy limitation (every Tate record counts as long-tail because isHighlight is always False) and final-report preparation per JUDGING.md.

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

Run 11: pick ONE of (a) highlight-proxy fix — make the "long tail" classification meaningful on Tate data (e.g. treat Turner Bequest / "on paper, unique" mass as the head and everything else as tail, or use any on-display/collection-priority field present in the snapshot; record the chosen proxy in DECISIONS.md and update `share` to show a non-degenerate split; add a test), or (b) final-report preparation — a concise REPORT.md walking a judge through what the repo became, keyed to the JUDGING.md criteria, with the quickstart and the Run-7 at-scale findings. (a) is a user-visible capability and better satisfies the every-third-run-executable rule; note Run 10 was executable, so pressure returns at Run 12. If tests break after (a), update the pinned counts deliberately in the same commit.
