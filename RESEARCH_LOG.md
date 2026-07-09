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
