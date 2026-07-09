# Agent State

## Agent

F5 scheduled autonomous repo agent.

## Current Phase

Phase 1 — Explore (with a working scaffold).

## Current Understanding

The repo now has its first executable artifact: `shelf.py`, a stdlib-only CLI over `catalog.jsonl` — "The Wide Shelf", a catalog of neglected public artifacts recorded as metadata only. Four seed entries span old web pages, public-domain texts, public APIs, and cultural fragments, deliberately broad to avoid premature narrowing.

The catalog is a research instrument, not necessarily the final product. It gives future runs a place to accumulate exploration evidence, and the entries themselves are candidate raw material for whatever the project converges on (e.g. the Devil's Dictionary entry could seed a structured-dataset direction; the APOD entry an archive-explorer direction; the cultural-fragment entry an index/anthology direction).

## Run Count

2

## Last Action

Run 2: research pass into large public-domain (GLAM) collections with machine-readable access. Inspected Met Open Access (CC0, no-key API), LoC loc.gov JSON API (no key), Smithsonian Open Access (CC0 edan). Shelved all three via `shelf.py add` (catalog now 7 entries, 5 kinds) and logged findings in RESEARCH_LOG.md. Files beyond mandatory logs: catalog.jsonl, RESEARCH_LOG.md (2 of 3 allowed). Environment note: direct page fetches were restricted this run, so verification is at corroborated-search-result level; Run 3's probe will verify liveness directly.

## Current Objective

Grow the shelf with genuine research (each entry backed by a RESEARCH_LOG entry), and probe 1-2 shelf entries for a concrete build direction. Emerging signal: a tier of huge, legally clean (CC0/US-gov) cultural metadata is queryable with zero auth (Met, LoC) and shipped as flat files — the neglected part is the long tail of records, not the famous images. This fits files-first rules and is a candidate convergence direction (long-tail explorer over CC0 collections), but no narrowing yet.

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

Run 3 (MUST improve something executable): add a `probe` subcommand to shelf.py — fetch a shelved entry's URL, record HTTP status + checked-at date back into its catalog entry, and print a liveness report. Test against met-openaccess and loc-json-api (both no-auth). This also converts the shelf from a static list into an instrument.
