# Agent Rules

## Core Operating Rules

The agent may explore widely, but every run must improve the repository in a concrete way.

The agent should prefer:

- working artifacts over planning
- small prototypes over broad frameworks
- public evidence over vibes
- executable behavior over documentation-only changes
- simple experiments over grand architecture
- fresh implementation over unexamined copying
- a broad search space before premature narrowing

Documentation-only changes may not happen twice in a row.

Every third run must produce or improve something executable, testable, queryable, playable, viewable, or otherwise usable.

The agent may change the project direction, but must record the reason in `DECISIONS.md`.

## Anti-Fixation Rule

Do not assume the project must be about GitHub, abandoned repositories, old code, or open-source archaeology.

Public repositories are valid research sources, but they are only one category among many. The agent should also consider public-domain archives, open datasets, old web pages, APIs, documents, games, simulations, educational materials, creative fragments, and other neglected public artifacts.

If the project narrows to old repositories or code salvage, it must justify that narrowing in `DECISIONS.md` with evidence from research or artifact-building — not merely because the seed mentioned public repositories as an example.

## Change Limits

Each run may change at most 3 files unless `AGENT_STATE.md` explicitly records why a larger atomic change is necessary.

Each run must update:

- `AGENT_STATE.md`
- `CHANGELOG.md`

Each run should add or update a machine-readable run record under `RUNS/` when practical.

## Public Research Rules

The agent may search public sources for ideas, examples, APIs, implementation patterns, datasets, lists, and neglected artifacts.

Useful sources may include:

- public repositories
- open data portals
- public-domain collections
- internet archives
- documentation sites
- old web pages
- public APIs
- papers and reports
- tutorials and examples
- creative commons or permissively licensed materials

The agent may not copy code, text, datasets, or media from another source unless all of the following are true:

1. The source has a clear license compatible with reuse, or the material is public domain.
2. The copied material is small, specific, and necessary.
3. The source is recorded in `THIRD_PARTY_NOTICES.md` with:
   - source URL
   - file/path/item identifier if available
   - commit SHA, release version, archive date, or access date when relevant
   - license or public-domain status
   - what was copied or adapted
4. The relevant license text is copied into `/licenses/` if required.
5. The agent does not copy from sources with:
   - no license
   - unclear license
   - GPL
   - AGPL
   - commercial/proprietary/custom license
   - terms that forbid reuse

Preferred order:

1. Learn from the source and write a fresh implementation.
2. Use source material as metadata or inspiration only.
3. Add a maintained package dependency.
4. Adapt a small permissively licensed snippet with attribution.
5. Vendor material only if no better option exists.

The agent may not bulk-clone repositories or bulk-import datasets without a clear license and a concrete reason.

## External Services

The agent may not add Supabase, hosted databases, paid APIs, queues, auth systems, or external infrastructure until the project has a working local artifact.

External infrastructure may be proposed only after the agent documents:

1. the current local limitation,
2. why files are no longer sufficient,
3. the minimum schema or service needed,
4. what new capability the service enables,
5. how the project still works in degraded/local mode.

Default preference:

1. files first
2. JSONL second
3. SQLite third
4. hosted services only when clearly justified

## Anti-Fiddling Rule

Once the project has a working artifact, the agent may not make cosmetic, organizational, or documentation-only changes unless one of the following is true:

- the change helps a user run the project
- the change fixes ambiguity in the project purpose
- the change documents a real behavior that already exists
- the change is part of final packaging

After MVP exists, every run must either:

- fix a real defect
- add a user-visible capability
- improve test coverage
- improve installation/use
- prepare the final report

No endless refactors. No naming churn. No roadmap gardening.
