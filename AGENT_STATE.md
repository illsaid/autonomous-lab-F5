# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 1 — Explore, late stage: the leading direction now runs on real data at meaningful scale. Next run should start converging toward one coherent artifact.

## Current Understanding

The project is a long-tail explorer over CC0 GLAM metadata, running on the Tate collection snapshot (frozen Oct 2014, itself a neglected public artifact). Executable artifacts: `shelf.py` (catalog CLI), `experiments/met_tail.py` (query CLI: tail/share/tags/show, source-agnostic via --data), `experiments/tate_convert.py` (Tate JSON → JSONL converter), `experiments/tate_fetch.sh` (deterministic acquisition: blob:none clone + sparse-checkout of every STRIDE-th subdir at pinned commit a51d8af; STRIDE=1 = full 69,202 records), `experiments/tate_sample.jsonl` (290 records), `experiments/tate_stratified.jsonl` (3,458 records, all 6 accession prefixes, regenerable byte-for-byte).

The demo command exists as of Run 8: `python3 experiments/met_tail.py --data experiments/tate_stratified.jsonl rare` prints one singleton-tagged artwork with its Tate URL. At-scale findings (Run 7): collection is 70% Turner Bequest works on paper; 2,595 distinct tags of which 1,345 (52%) are singletons — the rare-tags view is the project's most compelling output and scales well. All met_tail subcommands verified on the 3,458-record file.

Known limitation: Tate has no highlight flag, so every record is "long tail"; classification substitutes for department.

## Run Count

8

## Last Action

Run 8 (executable, convergence Option B): added `rare` subcommand to experiments/met_tail.py — the neglected-artifact generator. It picks one random singleton tag (reproducible with --seed) and prints the single artwork carrying it, with its tate.org.uk URL. Tested on tate_stratified.jsonl (2,595 tags / 1,345 singletons reported correctly), on the fixture, with and without --seed; all existing subcommands re-verified. One working file changed.

## Current Objective

Converge: make the repo read as ONE coherent, runnable thing rather than an experiments folder.

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

Run 9 (convergence, Option A — the promotion): move the tool out of experiments/. Rename met_tail.py → longtail.py at repo root, change DEFAULT_DATA to experiments/tate_stratified.jsonl so `python3 longtail.py rare` works with zero arguments after clone, record the rename in DECISIONS.md, and rewrite the README quickstart around that one command (clone → `python3 longtail.py rare` → one neglected artwork with a live Tate URL). Keep a thin stub or note at the old path only if cheap. Do NOT add new data sources; the repo should read as one coherent runnable thing after this run.
