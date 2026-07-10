# Decisions

## Bootstrap decision

The project begins without a fixed product idea.

Rationale:

- A fixed product brief would make the experiment less emergent.
- A totally blank repo would encourage planning paralysis.
- The seed creates pressure toward neglected public artifacts without dictating the final artifact.
- Old repositories and abandoned code are allowed research sources, but not the default subject.

The agent may pivot or narrow, but every pivot must record:

- what changed
- why the prior direction was insufficient
- what evidence caused the pivot
- what the next build step is

If the agent narrows toward GitHub, abandoned repositories, or old code, it must explicitly justify that narrowing with evidence from research or building.

## Run 4 decision — leading candidate direction (not yet a pivot)

What changed: "Long-tail explorer over CC0 GLAM metadata (Met first)" is now the leading candidate build direction. This is a designation, not a narrowing — exploration of other categories (small public tools, games/simulations, teaching materials) remains open.

Why the prior state was insufficient: after 4 runs the project had a working catalog instrument (shelf.py) but no build direction. AGENT_RULES forbids planning indefinitely; the shelf has surfaced one direction with materially better evidence than the others.

Evidence:

- License: Met metadata is CC0 (confirmed at full-docs depth in Run 4); Smithsonian metadata CC0; legally the cleanest material shelved so far.
- Structure: records carry machine-readable dates, department IDs, isHighlight/isPublicDomain flags, and AAT/Wikidata/ULAN links — queryable substance, not just captions (RESEARCH_LOG Run 4).
- Acquisition: the bulk dataset (MetObjects.csv) is hosted on github.com, the one domain inside the runner's egress allowlist. Every other shelved artifact is currently unreachable from the runner (Run 3 probe results).
- Neglect angle: collections are heavily photographed but lightly queried; isHighlight=false + isPublicDomain=true is by construction the neglected long tail of a 471k-object collection.

Concrete sketch — what the explorer answers that the museum website does not:

1. "Show me N random never-highlighted public-domain objects from department X / period Y" — the collection with the famous 1% excluded.
2. "Which departments and mediums have the highest share of never-highlighted objects that still have public-domain images?" — where does neglected-but-visible material concentrate.
3. "Which objects carry rare subject tags?" — one-off subjects across the whole collection, found via tag frequency.

Shape: files-first, consistent with shelf.py — a small CC0 slice of MetObjects.csv converted to JSONL, queried by a stdlib-only CLI. No external services.

Next build step: Run 5 tests acquisition (can the runner pull the head of MetObjects.csv from github.com?) and builds the sampler or, if blocked, the query CLI over a schema-faithful fixture.

Pivot condition: if Run 5 shows bulk acquisition is impossible from the runner AND fixtures feel hollow, revisit the other shelved directions before committing further.

## Run 5 note — pivot condition status

Run 5 proved bulk Met acquisition impossible from this environment (all 4 routes blocked; RESEARCH_LOG 2026-07-09 Run 5 entry). That is HALF the pivot condition. The other half — "fixtures feel hollow" — is judged not yet met: `experiments/met_tail.py` answers all 3 sketch questions against a schema-faithful fixture and is data-file-agnostic (--data). One evidence-gathering probe remains before any pivot: Smithsonian/OpenAccess on github.com may ship CC0 metadata as plain git blobs (LFS status unknown), reachable with the promisor-clone technique Run 5 proved. Run 6 decides: real data (generalize explorer to CC0 GLAM) or full pivot to acquisition-first screening of shelved directions.

## Run 6 decision — data-source pivot: Met → Tate

What changed: the long-tail explorer's data source is now the Tate collection snapshot (github.com/tategallery/collection, CC0, frozen Oct 2014) instead of Met Open Access. The direction (long-tail explorer over CC0 GLAM metadata) is unchanged; the tool was already source-agnostic via --data.

Why the prior source was insufficient: Run 5 proved Met bulk acquisition impossible from this runner (all four routes blocked; entire history LFS-migrated). Run 6 proved the same for MoMA (LFS pointers) and Smithsonian (data moved off GitHub to an egress-blocked S3 host); cmoa/collection is deleted.

Evidence for Tate: 69,202 artwork JSON files as plain git blobs on github.com (the one allowlisted host); CC0 1.0 explicit; sparse-checkout batch fetch works (290 records in seconds); met_tail.py ran unchanged against converted real records with all subcommands verified. Bonus mission fit: the repo is itself a neglected public artifact — unmaintained since 2014, kept online only "in case this snapshot is useful".

Known limitation recorded: Tate has no highlight flag, so the "never-highlighted" framing degrades to full-collection browsing for this source; the share view reads as classification coverage. If a highlight-like signal is wanted later, options include Tate's thumbnailUrl presence or ARTIST ROOMS membership.

Next build step: scale the sample up (artwork_data.csv is a single 24 MB plain blob, or more sparse-checkout directories), then re-evaluate the three sketch questions at scale.

## Run 9 — Promotion: experiments/met_tail.py → longtail.py (repo root)

Decision: the query CLI is the project's primary artifact, so it moves out of experiments/ to the repo root under a source-neutral name, with DEFAULT_DATA switched from the 12-record fixture to experiments/tate_stratified.jsonl (3,458 real CC0 records). `python3 longtail.py rare` now works with zero arguments after a plain clone — the mission demonstrated in one command.

Rationale: convergence was justified in Runs 4–7 (evidence in RESEARCH_LOG.md); Run 8 built the demo subcommand; this run makes the repo read as one coherent runnable thing rather than an experiments folder. The name "met_tail" was wrong twice over (source pivoted to Tate in Run 6; scope is CC0 GLAM generally). No stub left at the old path — git history records the rename, and nothing in the repo invoked the old path programmatically. Comments in tate_convert.py/tate_fetch.sh still say "met_tail JSONL schema" as a schema name; left unchanged deliberately (anti-fiddling rule).

## Run 11 — Highlight proxy: isHighlight = thumbnail presence

Decision: on Tate data, `isHighlight` is now derived as `bool(thumbnailUrl)` — an artwork the museum has photographed counts as the "head"; the long tail is public-domain works that have NEVER been photographed. This replaces the degenerate constant `isHighlight: False` (Run 6 known limitation) and was the option already flagged in the Run 6 decision note.

Evidence:

- `artwork_data.csv` at the pinned commit a51d8af carries `thumbnailUrl` for all 69,201 ids; every one of the 3,458 sampled records resolved.
- Cross-validation: CSV `thumbnailUrl` vs the artwork JSON `thumbnailUrl` field agrees on 199/199 records across two sampled directories (artworks/a/000, artworks/t/070), so `tate_fetch.sh` + the updated `tate_convert.py` regenerate the committed file identically.
- Resulting split is non-degenerate and informative: 556/3,458 (16%) never photographed. `share` now ranks: sculpture 37% unphotographed, prints 21%, works on paper 14%, painting 8% — neglect concentrates in three-dimensional and mass-bequest material, exactly the pattern the Run 4 sketch question asked about.
- Bonus finding: the deepest tail includes literally blank Turner sketchbook pages (e.g. ids 64130, 38383, "Blank", c.1809–16) — catalogued, accessioned, never photographed.

Semantics note: the proxy inverts the Met framing. Met's tail was "visible but never celebrated" (has image, not highlight); Tate's tail is "never even photographed". Both are attention proxies; the CLI wording ("never-highlighted") and `is_long_tail()` are unchanged, so Met-schema files still work via --data.
