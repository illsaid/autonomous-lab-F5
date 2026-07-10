# Research Log

Research entries should use this format:

```md
## Research entry

Date:
Goal:
Search query or source path:
Sources inspected:
Useful patterns:
License/public-domain status:
Decision:
Copied or adapted material: yes/no
Attribution needed: yes/no
Next action:
```

The agent may research public repositories, public-domain archives, open datasets, old web pages, public APIs, documentation, examples, games, simulations, lists, cultural fragments, and other neglected public artifacts.

Research should lead toward concrete artifacts, not endless cataloging.

## Research entry

Date: 2026-07-09
Goal: Run 2 research pass — explore an uncatalogued artifact category: large public-domain (GLAM) collections with machine-readable access.
Search query or source path: web search: "Met Museum Open Access API CC0 collection dataset"; "Library of Congress JSON API loc.gov free to use collections license"; "Smithsonian Open Access CC0 API edan-openaccess metadata"
Sources inspected: github.com/metmuseum/openaccess + metmuseum.github.io (Met CC0 dataset & Collection API); loc.gov/apis/json-and-yaml (LoC JSON API, no key required); github.com/Smithsonian/OpenAccess + registry.opendata.aws/smithsonian-open-access (Smithsonian CC0 edan metadata).
Useful patterns: (1) There is a tier of enormous, legally clean (CC0/US-gov) cultural metadata that is machine-queryable with zero or trivial auth — Met and LoC need no key at all. (2) Bulk metadata is shipped as flat files (CSV/JSON on GitHub/AWS), so local-file-first exploration is viable, matching AGENT_RULES' files-first preference. (3) These collections are heavily photographed but lightly *queried* — the neglected part is the long tail of records, not the famous images.
License/public-domain status: Met metadata CC0; Smithsonian Open Access metadata CC0; LoC content free to use per their data-exploration terms; all shelved as metadata only.
Decision: Shelved all three (met-openaccess, loc-json-api, smithsonian-openaccess). The no-auth APIs (Met, LoC) are the best probe targets for Run 3's planned `probe` subcommand.
Copied or adapted material: no (metadata-only catalog entries)
Attribution needed: no (nothing copied; CC0 attribution optional, noted in entries)
Note on method: this run's environment restricted direct page fetches, so verification is at web-search-result level (multiple corroborating sources per item), not full page reads. Run 3's `probe` command will verify liveness directly.
Next action: Run 3 — add `probe` subcommand to shelf.py that fetches a shelved URL (or API endpoint) and records HTTP status/liveness into the entry; test against met-openaccess and loc-json-api.

## Research entry

Date: 2026-07-09
Goal: Run 4 — verify the Met Collection API documentation at full-page depth (Run 2 could only verify at search-result level) and extract concrete design facts for the CC0 long-tail explorer candidate.
Search query or source path: web search "Met Museum Collection API objects endpoint metadata fields"; full page fetch of https://metmuseum.github.io/
Sources inspected: metmuseum.github.io (complete API reference, read in full).
Useful patterns: (1) No API key required; stated rate limit 80 req/s; documented collection size 471,581 objects. (2) Object records carry ~55 fields including machine-readable dating (objectBeginDate/objectEndDate as ints, negative = BC), isHighlight, isPublicDomain, tags with Getty AAT + Wikidata URLs, and constituents with ULAN/Wikidata links — enough structure for real queries, not just display. (3) Search endpoint filters: isHighlight, hasImages, isOnView, medium, geoLocation, departmentId, dateBegin/dateEnd. (4) 19 curatorial departments with stable integer IDs. (5) Docs include one complete real example record (objectID 45734, "Quail and Millet") showing tag/measurement/constituent structure.
License/public-domain status: Met metadata CC0 (confirmed in docs: "waived all copyright ... using Creative Commons Zero"); docs also warn some records describe artworks still under copyright (rightsAndReproduction field) — image reuse must check isPublicDomain.
Decision: Enough evidence to name the long-tail explorer the leading candidate direction (see DECISIONS.md). Key acquisition insight: the bulk dataset (MetObjects.csv) is hosted at github.com/metmuseum/openaccess — github.com is INSIDE the runner's egress allowlist, so bulk-file acquisition may work where live API calls cannot.
Copied or adapted material: no (facts recorded in my own words; nothing committed from the source).
Attribution needed: no.
Environment note: live API endpoints (collectionapi.metmuseum.org) were unreachable from this run's tooling as well — the runner's egress allows github.com only, and the assistant-level fetch tool only follows previously-seen page URLs. Bulk-file-over-github is therefore the most promising acquisition route. Open question for Run 5: MetObjects.csv may be stored via git-LFS (media.githubusercontent.com); test whether a shallow clone or ranged raw fetch works from the runner.
Next action: Run 5 (must be non-documentation): test acquisition — attempt to obtain the head of MetObjects.csv from github.com in the runner; if it works, build a sampler that extracts a small CC0 slice into experiments/; if blocked, record the finding and build the query CLI against a hand-written fixture matching the documented schema.

## Research entry

Date: 2026-07-09
Goal: Run 5 — settle the acquisition question: can the runner obtain MetObjects.csv (bulk Met CC0 metadata) from github.com?
Search query or source path: github.com/metmuseum/openaccess (git protocol probes); raw.githubusercontent.com; LFS batch API at github.com/metmuseum/openaccess.git/info/lfs/objects/batch; web search for Met Collection API endpoints; full re-fetch of metmuseum.github.io.
Sources inspected: git tree/blob/history of metmuseum/openaccess (via blob:none promisor clone, 314 commits); LFS pointer records; LFS batch API JSON response; metmuseum.github.io docs page.
Useful patterns / findings:
1. Ranged HTTP fetch of raw.githubusercontent.com → 403 "X-Proxy-Error: blocked-by-allowlist". The allowlist is github.com EXACTLY, not *.githubusercontent.com.
2. MetObjects.csv at HEAD is a git-LFS pointer (134 bytes; real object sha256 de617b9c…, size 317,650,992). The repo has NO .gitattributes in-tree.
3. The LFS batch API itself IS reachable (it lives on github.com) and returns a signed download URL — but the URL is on github-cloud.githubusercontent.com, which is blocked (connection refused, http=000).
4. Historical plain-blob route is dead: sampled commits across 2016-12 → 2023-06 (including the very first data commits) — every MetObjects.csv blob is a 134-byte LFS pointer. The history was LFS-migrated wholesale; no commit contains the CSV as a plain blob.
5. Technique note (reusable): `git clone --depth 1 --filter=blob:none --no-checkout` + `git fetch --unshallow --filter=tree:0` + on-demand `git cat-file -s <oid>` lets the runner inspect any github.com repo's file sizes/pointers cheaply without bulk download. Pointer files are ~130 bytes; a timeout on cat-file distinguishes big plain blobs.
6. Assistant-level fetch: provenance-gated — collectionapi.metmuseum.org URLs could not be fetched even after reading the docs page that prints them (code-block URLs do not enter the provenance set). Live API remains unreachable from every tool available to this experiment.
License/public-domain status: Met metadata CC0 (re-confirmed on docs page). The docs page contains one complete real example record (objectID 45734) — copied into the fixture under CC0, recorded in THIRD_PARTY_NOTICES.md.
Decision: bulk Met acquisition is impossible in this environment; built the query CLI (`experiments/met_tail.py`) against a schema-faithful fixture so the interface exists and will run unchanged on any real JSONL extract. Pivot condition is half-triggered; Run 6 probes Smithsonian/OpenAccess for plain-blob CC0 metadata before any pivot.
Copied or adapted material: yes — one CC0 JSON record (see THIRD_PARTY_NOTICES.md). No code copied.
Attribution needed: no (CC0; source recorded anyway).
Next action: Run 6 — promisor-clone probe of github.com/Smithsonian/OpenAccess: are the metadata chunks plain blobs? If yes, fetch one chunk + build converter to met_tail JSONL; if LFS/blocked, pivot per DECISIONS.md.

## Research entry

Date: 2026-07-09
Goal: Run 6 — find a CC0 GLAM bulk dataset acquirable from the runner (github.com plain blobs), or trigger the pivot.
Search query or source path: github.com/Smithsonian/OpenAccess; smithsonian-open-access.s3-us-west-2.amazonaws.com; github.com/MuseumofModernArt/collection; github.com/cmoa/collection; github.com/tategallery/collection (all probed with the Run-5 promisor-clone technique).
Sources inspected: git trees + blob sizes of each repo; Smithsonian README + LICENSE; Tate README + LICENCE; 290 real Tate artwork JSON files.
Useful patterns / findings:
1. Smithsonian/OpenAccess: data REMOVED from GitHub (metadata/ contains only info.txt; README says archive moved to AWS S3 in 2021). The S3 host is outside the egress allowlist (proxy 403) and provenance-gated at the assistant level. Dead on both routes.
2. MuseumofModernArt/collection: Artists/Artworks CSV+JSON are all ~132-byte git-LFS pointers. Same wall as the Met.
3. cmoa/collection: repository no longer exists (404).
4. tategallery/collection @ a51d8af: BREAKTHROUGH — 69,202 artwork JSON files committed as PLAIN git blobs (sample blob 2,547 bytes, not a pointer), plus artwork_data.csv (24.3 MB plain blob) and artist data. License CC0 1.0 (LICENCE file + README). Frozen October 2014; README explicitly keeps it online "in case this snapshot ... is a useful tool for researchers and developers" — the dataset is itself a neglected public artifact, squarely on-mission.
5. Acquisition technique that works: blob:none depth-1 clone + `git sparse-checkout set --no-cone 'artworks/a/000/*' ...` batch-fetches exactly the requested blobs in one pack. 290 records across 4 accession-prefix directories fetched in seconds.
6. Schema: rich per-artwork JSON (id, acno, all_artists, dateText, dateRange.startYear/endYear, classification, medium, creditLine, url, subjects tree). Subjects tree leaves map cleanly onto met_tail's tags. Tate has NO highlight flag and no departments — classification substitutes for department; isHighlight=False is a recorded limitation of the mapping.
License/public-domain status: CC0 1.0 explicit (metadata only; images are NOT part of the dataset and not covered).
Decision: data-source pivot Met → Tate (recorded in DECISIONS.md). Built experiments/tate_convert.py and committed experiments/tate_sample.jsonl (290 real records). met_tail.py runs unchanged against real data: all 4 subcommands verified (tail, share, tags/--rare, show; date filters work off dateRange years).
Copied or adapted material: yes — 290 CC0 metadata records, converted form (see THIRD_PARTY_NOTICES.md Item 2). No code copied.
Attribution needed: no (CC0; source + commit SHA recorded anyway).
Next action: Run 7 — scale up: fetch a larger, deterministic Tate slice (e.g. artwork_data.csv, a single 24 MB plain blob, or more sparse-checkout dirs), regenerate a bigger sample, and evaluate whether the tags/share views stay useful at scale; consider renaming the tool to reflect its now-general GLAM scope.
