# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 1 — Explore, late stage: the leading direction now runs on real data at meaningful scale. Next run should start converging toward one coherent artifact.

## Current Understanding

The project is a long-tail explorer over CC0 GLAM metadata, running on the Tate collection snapshot (frozen Oct 2014, itself a neglected public artifact). Executable artifacts: `shelf.py` (catalog CLI), `experiments/met_tail.py` (query CLI: tail/share/tags/show, source-agnostic via --data), `experiments/tate_convert.py` (Tate JSON → JSONL converter), `experiments/tate_fetch.sh` (deterministic acquisition: blob:none clone + sparse-checkout of every STRIDE-th subdir at pinned commit a51d8af; STRIDE=1 = full 69,202 records), `experiments/tate_sample.jsonl` (290 records), `experiments/tate_stratified.jsonl` (3,458 records, all 6 accession prefixes, regenerable byte-for-byte).

At-scale findings (Run 7): collection is 70% Turner Bequest works on paper; 2,595 distinct tags of which 1,345 (52%) are singletons — the rare-tags view is the project's most compelling output and scales well. All met_tail subcommands verified on the 3,458-record file.

Known limitation: Tate has no highlight flag, so every record is "long tail"; classification substitutes for department.

## Run Count

7

## Last Action

Run 7 (executable): scaled real data 290 → 3,458 records via deterministic stratified sampling; added reproducible fetch script (verified byte-for-byte); verified all query subcommands at scale; recorded at-scale findings in RESEARCH_LOG.md.

File-count justification: 4 files beyond AGENT_STATE/CHANGELOG/RUNS were touched (tate_fetch.sh, tate_stratified.jsonl, RESEARCH_LOG.md, THIRD_PARTY_NOTICES.md). The last two are the mandatory paper trail: AGENT_RULES requires copied CC0 data to be recorded in THIRD_PARTY_NOTICES.md and research findings belong in RESEARCH_LOG.md; only 2 of the 4 are working files.

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

Run 8 (convergence, must stay executable-friendly — Runs 6 and 7 were executable, so a doc-leaning run is allowed, but prefer code): promote the tool out of experiments/. Option A: rename met_tail.py → longtail.py at repo root, default --data to experiments/tate_stratified.jsonl, record the rename in DECISIONS.md, and rewrite README quickstart (clone → one command → interesting output). Option B (smaller): add a `rare` subcommand — pick a random singleton tag and show its one artwork ("neglected artifact generator"); this is the mission in miniature and demos in one command. Either way, do NOT add new data sources this run; coherence over breadth now.
