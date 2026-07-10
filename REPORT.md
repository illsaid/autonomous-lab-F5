# Final Report — Autonomous Lab F5

*Written by the F5 agent at Run 12, updated at Run 14, keyed to the criteria in [JUDGING.md](JUDGING.md). Every claim below is reproducible from a plain clone with Python 3 and no dependencies.*

## What the repo became

A **long-tail explorer over CC0 museum collection metadata**, running on the Tate collection snapshot — a dataset that is itself a neglected public artifact (69,202 CC0 artwork records, frozen on GitHub since October 2014, never updated since).

The one-command demo:

```
python3 longtail.py rare
```

prints one artwork that is the *only* work in the sample carrying its subject tag, with a live tate.org.uk URL. The seed asked for neglected public artifacts turned into a working artifact; `rare` is that mission compressed into one command — it hands you a genuinely obscure artwork every time.

## Usefulness

The tool answers real questions a curator, researcher, or bored human can't easily ask the Tate's own site: which works were *never photographed* (`tail`), which classifications are most neglected (`share`), which subjects exist exactly once in the collection (`tags --rare`, `rare`), and how neglect tracks acquisition date (`era`). Findings at scale (3,458-record stratified sample, Run 7 & 11):

- 1,345 of 2,595 subject tags (52%) are singletons — the tail is most of the vocabulary.
- 16% of sampled works have never been photographed; sculpture is 37% unphotographed vs painting at 8%.
- The deepest tail: blank pages of Turner's sketchbooks, individually accessioned, untagged, unphotographed.
- Photography lags acquisition (Run 13, `era`): works acquired in the 1980s–90s are ≤3% unphotographed, but the 2000s sit at 37% and the 2010s at 84% — in the frozen 2014 snapshot, the newest works are the least visible.

## Originality

Not a GitHub-code-archaeology project (the obvious attractor the rules warn about). The subject is museum metadata; the "neglect" being explored is double: works neglected *within* the collection, surfaced from a dataset neglected *by its own institution*. The `isHighlight` proxy (Run 11: highlight = "has a photograph") turned a missing field into the project's most informative axis.

## Coherence

One tool (`longtail.py`, six subcommands), one dataset (`experiments/tate_stratified.jsonl`), one converter (`tate_convert.py`), one deterministic fetcher (`tate_fetch.sh`), one test suite. `shelf.py` + `catalog.jsonl` remain as the Run 1–3 exploration instrument that led here — a working catalog of 7 candidate artifacts across 5 kinds, with liveness probes.

## Executability

- `python3 longtail.py rare` — zero-argument demo after plain clone.
- `python3 tests/test_longtail.py` — 10 regression tests, all passing (record counts, tag counts, seeded reproducibility, JSON output, exit codes, SIGPIPE behavior, the 2,902/556 photographed split, the 1850s `era` row and creditLine year parser).
- `experiments/tate_fetch.sh` regenerates the shipped sample byte-for-byte from the pinned upstream commit (a51d8af); `STRIDE=1` fetches all 69,202 records.

## Breadth before convergence

Runs 1–3 cataloged 7 artifacts across 5 kinds (old web pages, public-domain texts, APIs, datasets, cultural fragments). Run 4 nominated a direction with an explicit pivot condition. Runs 5–6 were honest acquisition science: Met (4 routes, all dead — LFS everywhere), Smithsonian (data deleted), MoMA (LFS pointers), CMOA (repo gone), Tate (plain blobs, CC0 — works). The convergence was forced by evidence, and the dead ends are documented in RESEARCH_LOG.md.

## Efficiency & elegance

Twelve runs, each ≤3 working files. No dependencies, no framework, no database — JSONL + stdlib argparse throughout (the rules' "files first" preference, held to the end). The most complex machinery in the repo is a sparse-checkout git incantation, and it exists because it was the *only* route to real data from this sandbox.

## Research quality

RESEARCH_LOG.md contains the Met API's actual design facts, the four-route acquisition failure analysis, and the cross-museum LFS survey. The research directly produced the pivot (Run 6) and the proxy validation (Run 11: CSV-vs-JSON agreement checked 199/199 before regenerating the dataset).

## License hygiene

Everything shipped is CC0 (Tate) or original. The one borrowed record (a Met API doc example) is logged in THIRD_PARTY_NOTICES.md. No GPL, no unlicensed copying, no bulk cloning without license verification — the Run 6 probes checked licenses *before* fetching data.

## What would come next

A continuation round would: scale to the full 69,202 records (the fetcher already supports it) and probe whether works surfaced by `rare` correlate with missing Wikipedia/Wikidata coverage — turning the toy into a to-do list for open-culture volunteers.

## Honest limitations

The sample is 5% of the collection (stratified, deterministic, but a sample). "Never photographed" is a proxy measured against a 2014 snapshot; Tate may have photographed works since. The collection is 70% Turner Bequest works on paper, so collection-wide statistics are Turner-dominated — per-classification views (`share`) are the honest lens.
