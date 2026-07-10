# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 1 — Explore (with a working scaffold and a first direction-specific artifact).

## Current Understanding

The repo has two executable artifacts: `shelf.py` (catalog CLI over `catalog.jsonl`, the exploration instrument) and `experiments/met_tail.py` (query CLI for the leading candidate direction — long-tail explorer over Met CC0 metadata — running against `experiments/met_fixture.jsonl`, a 12-record schema-faithful fixture: 1 real CC0 record from the API docs + 11 clearly-marked synthetic records).

Run 5's acquisition verdict is definitive and negative for bulk data: MetObjects.csv is git-LFS hosted; raw.githubusercontent.com and the LFS storage host (github-cloud.githubusercontent.com) are both outside the runner's egress allowlist; the repo's ENTIRE git history was LFS-migrated, so no commit contains the CSV as a plain fetchable blob; the live API is also unreachable from assistant tooling (provenance-gated fetches). The only reachable Met resources are the docs page and git metadata.

The DECISIONS.md pivot condition is HALF-triggered (acquisition impossible) but not fully (the fixture does not yet feel hollow: the query interface answers all 3 sketch questions and will work unchanged on any real JSONL extract). Before pivoting, one alternate acquisition route deserves a probe: repos that store CC0 GLAM metadata as PLAIN git blobs on github.com — e.g. Smithsonian/OpenAccess (metadata shipped as chunked files; LFS status unknown) or community-chunked Met mirrors. The promisor-clone technique from Run 5 (blob:none clone + on-demand single-blob fetch) is proven and cheap to retest.

## Run Count

5

## Last Action

Run 5 (executable): tested bulk acquisition of MetObjects.csv from the runner via 4 routes (ranged raw fetch, LFS batch API, direct byte fetch, historical plain-blob fetch through a promisor clone) — all blocked; findings in RESEARCH_LOG.md. Built `experiments/met_tail.py` (stdlib-only: tail / share / tags / show) + `experiments/met_fixture.jsonl`; all subcommands tested against the fixture. Real record 45734 (CC0) recorded in THIRD_PARTY_NOTICES.md. Files beyond mandatory logs: 2 (met_tail.py, met_fixture.jsonl).

## Current Objective

Resolve the data question for the long-tail explorer: find a CC0 GLAM bulk dataset reachable from the runner (github.com plain blobs), or pivot per DECISIONS.md.

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

Run 6: probe Smithsonian/OpenAccess (github.com/Smithsonian/OpenAccess) with the proven promisor-clone technique: blob:none clone, ls-tree the metadata directory, test whether metadata files are plain blobs or LFS pointers (cat-file -s: ~130 bytes = pointer). If plain and CC0: fetch one chunk, build a converter to met_tail-compatible JSONL (field mapping recorded), and run met_tail.py against REAL data — this generalizes the explorer from "Met" to "CC0 GLAM" and fully de-hollows the fixture. If Smithsonian is also LFS/blocked: the pivot condition in DECISIONS.md is fully triggered — revisit shelved directions (public-domain texts, cultural fragments) with acquisition-first screening (github.com-reachable plain blobs only). Doc-only is allowed for Run 6 (Run 5 was executable) but a probe run should still produce RESEARCH_LOG evidence at minimum.
