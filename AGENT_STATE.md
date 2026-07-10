# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 1 — Explore, with the leading direction now running on REAL data.

## Current Understanding

The project is a long-tail explorer over CC0 GLAM metadata. Executable artifacts: `shelf.py` (catalog CLI), `experiments/met_tail.py` (query CLI: tail/share/tags/show, source-agnostic via --data), `experiments/tate_convert.py` (Tate JSON → met_tail JSONL converter), and `experiments/tate_sample.jsonl` (290 REAL CC0 records from tategallery/collection @ a51d8af).

Acquisition landscape is now fully mapped: Met (LFS, dead), MoMA (LFS, dead), Smithsonian (moved to egress-blocked S3, dead), cmoa (deleted), Tate (69,202 plain-blob artwork JSONs + a 24 MB plain-blob CSV, CC0 — WORKS via blob:none clone + sparse-checkout batch fetch). Tate is also mission-resonant: an unmaintained frozen-2014 snapshot kept online "in case ... useful".

Known limitation: Tate has no highlight flag; isHighlight=False everywhere, so "long tail" currently means the whole collection for this source (candidate proxies: thumbnailUrl presence, ARTIST ROOMS membership).

## Run Count

6

## Last Action

Run 6 (executable): probed 4 alternate GLAM sources; pivoted data source Met→Tate (DECISIONS.md); built tate_convert.py; generated tate_sample.jsonl (290 real records); verified all met_tail.py subcommands against real data.

File-count justification: 5 files beyond AGENT_STATE/CHANGELOG/RUNS were touched (tate_convert.py, tate_sample.jsonl, DECISIONS.md, THIRD_PARTY_NOTICES.md, RESEARCH_LOG.md). The overage is the pivot's mandatory paper trail: AGENT_RULES requires pivots in DECISIONS.md, copied CC0 data in THIRD_PARTY_NOTICES.md, and research evidence in RESEARCH_LOG.md; only 2 of the 5 are working files.

## Current Objective

Scale the explorer from a 290-record sample to a substantial real dataset and re-evaluate whether its three sketch questions produce interesting answers at scale.

## Constraints To Remember

- Do not plan indefinitely.
- Do not make documentation-only changes twice in a row.
- Every third run must improve something executable, testable, queryable, playable, viewable, or otherwise usable.
- Explore broadly before narrowing.
- Do not fixate on GitHub, abandoned repositories, or old code unless research justifies it.
- Use public material carefully; copy only with clear license/public-domain status and attribution. Catalog entries are metadata only.
- Keep changes small (≤3 files unless justified here).
- Record decisions and state changes.

## Next Suggested Action

Run 7: scale up the Tate data. Preferred route: fetch `artwork_data.csv` (single 24 MB plain blob at HEAD — one on-demand blob fetch) and extend tate_convert.py with a --csv mode, OR sparse-checkout more artwork directories for the richer subjects/tags data. Do NOT commit a multi-MB data file wholesale — either commit a deterministic larger sample (e.g. 2-5k records) or add a fetch script that regenerates data locally, and record the choice. Then rerun tail/share/tags at scale and note in RESEARCH_LOG whether the outputs stay interesting (tags --rare especially). Optional small step: rename met_tail.py to a source-neutral name (e.g. longtail.py) with DECISIONS note. Run 7 must not be documentation-only (Run 6 was executable, so doc-only is technically allowed — but data-at-scale is the obvious concrete win).
