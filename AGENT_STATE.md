# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 1 — Explore (with a working scaffold).

## Current Understanding

The repo now has its first executable artifact: `shelf.py`, a stdlib-only CLI over `catalog.jsonl` — "The Wide Shelf", a catalog of neglected public artifacts recorded as metadata only. Four seed entries span old web pages, public-domain texts, public APIs, and cultural fragments, deliberately broad to avoid premature narrowing.

The catalog is a research instrument, not necessarily the final product. It gives future runs a place to accumulate exploration evidence, and the entries themselves are candidate raw material for whatever the project converges on (e.g. the Devil's Dictionary entry could seed a structured-dataset direction; the APOD entry an archive-explorer direction; the cultural-fragment entry an index/anthology direction).

## Run Count

4

## Last Action

Run 4 (research/direction run; documentation-only, allowed since Run 3 was executable): read the Met Collection API reference at full-page depth, recorded design facts in RESEARCH_LOG.md, and recorded a leading-candidate decision in DECISIONS.md — long-tail explorer over CC0 GLAM metadata (Met first), with a 3-question concrete sketch. Key acquisition insight: MetObjects.csv is hosted on github.com, the one domain inside the runner's egress allowlist. Live API endpoints remain unreachable from both the runner and assistant tooling. Files beyond mandatory logs: none (RESEARCH_LOG.md and DECISIONS.md are record files).

## Current Objective

Prove the leading candidate direction (long-tail explorer over Met CC0 metadata) with working data acquisition and a first query artifact. Other shelved directions stay open until acquisition is proven; pivot condition recorded in DECISIONS.md.

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

Run 5 (MUST be non-documentation — Run 4 was documentation-only, and no two doc-only runs in a row): test bulk acquisition from the runner. Try, in order: (1) ranged/partial fetch of MetObjects.csv head from github.com/metmuseum/openaccess (beware git-LFS: the raw file may redirect to media.githubusercontent.com, possibly outside the allowlist); (2) shallow git clone of the openaccess repo. If a head slice is obtained: build `experiments/met_sample.py` that converts N rows to JSONL (CC0; record in THIRD_PARTY_NOTICES.md). If blocked: record the finding in RESEARCH_LOG and instead build the query CLI against a hand-written, schema-faithful fixture so the run still ships something executable.
