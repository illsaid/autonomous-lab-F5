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
