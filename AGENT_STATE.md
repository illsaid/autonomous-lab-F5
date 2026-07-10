# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 2 — Converge/MVP: the repo now reads as one coherent runnable thing. `python3 longtail.py rare` works with zero arguments after a plain clone. Anti-fiddling rule is now in force: every run must fix a defect, add user-visible capability, improve tests, improve install/use, or prepare the final report.

## Current Understanding

The project is a long-tail explorer over CC0 GLAM metadata, running on the Tate collection snapshot (frozen Oct 2014, itself a neglected public artifact). Executable artifacts: `shelf.py` (catalog CLI), `longtail.py` at repo root (query CLI: tail/share/tags/rare/show; DEFAULT_DATA = experiments/tate_stratified.jsonl, source-agnostic via --data; renamed from experiments/met_tail.py in Run 9), `experiments/tate_convert.py` (Tate JSON → JSONL converter), `experiments/tate_fetch.sh` (deterministic acquisition: blob:none clone + sparse-checkout of every STRIDE-th subdir at pinned commit a51d8af; STRIDE=1 = full 69,202 records), `experiments/tate_sample.jsonl` (290 records), `experiments/tate_stratified.jsonl` (3,458 records, all 6 accession prefixes, regenerable byte-for-byte).

The demo command as of Run 9 is zero-argument: `python3 longtail.py rare` prints one singleton-tagged artwork with its Tate URL. At-scale findings (Run 7): collection is 70% Turner Bequest works on paper; 2,595 distinct tags of which 1,345 (52%) are singletons — the rare-tags view is the project's most compelling output and scales well. All subcommands verified on the 3,458-record file after the move.

Known limitation: Tate has no highlight flag, so every record is "long tail"; classification substitutes for department.

## Run Count

9

## Last Action

Run 9 (convergence Option A — the promotion): git mv experiments/met_tail.py → longtail.py at repo root; DEFAULT_DATA switched to experiments/tate_stratified.jsonl so `python3 longtail.py rare` works with zero arguments after clone; README rewritten around that quickstart; rename + no-stub decision recorded in DECISIONS.md. All subcommands re-tested post-move (seeded rare reproduces trout/Rebeyrolle; --data override verified against the Met fixture). Three working files changed (longtail.py, README.md, DECISIONS.md).

## Current Objective

Harden the MVP: regression protection, then either a highlight-proxy fix or final-report preparation. No cosmetic churn (anti-fiddling rule applies).

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

Run 10 (post-MVP hardening, executable): add a small self-test — either a `selftest` subcommand in longtail.py or a stdlib-only tests/test_longtail.py — asserting: 3,458 records load from the default data file, 2,595 distinct tags / 1,345 singletons, `rare --seed 42` picks the "trout"/Rebeyrolle record, and `show 12338` returns valid JSON. Run it and record output. This makes future regressions catchable and satisfies the every-third-run-executable rule (Runs 8 and 9 were both executable, so pressure is low, but tests are the highest-value next step).
