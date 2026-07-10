# Third-Party Notices

This file records any third-party code, data, text, media, or adapted material used by the project.

The default state is: no third-party material copied.

For each copied or adapted item, record:

- Source URL
- Source file/path/item identifier if available
- Commit SHA, release version, archive date, or access date when relevant
- License or public-domain status
- What was copied or adapted
- Whether license text was added under `/licenses/`

The agent should prefer learning from public material and writing fresh implementations over copying.

## Item 1 — Met Collection API example record (objectID 45734)

- Source URL: https://metmuseum.github.io/ (official Met Collection API reference)
- Item: the complete example object record for objectID 45734 ("Quail and Millet", Kiyohara Yukinobu), reproduced in the docs.
- Access date: 2026-07-09
- License: CC0 (The Met has waived copyright in its Open Access metadata via Creative Commons Zero; stated in the same document)
- What was copied: the JSON record verbatim into `experiments/met_fixture.jsonl` as the one real record in the fixture (all other records are synthetic and marked `"fixture": true`).
- License text under /licenses/: not added (CC0 waiver; source and status recorded here).

## Item 2 — Tate collection metadata sample (290 records)

- Source URL: https://github.com/tategallery/collection
- Commit SHA: a51d8afc988ed083557e2950f4d0b644e7719f4a (dataset frozen October 2014)
- Access date: 2026-07-09
- License: CC0 1.0 Universal (LICENCE file in the source repo; README confirms metadata released under CC0. Images are NOT part of the dataset and NOT covered.)
- What was copied: 290 artwork metadata records from `artworks/{a,d,n,t}/000/`, converted (not verbatim) by `experiments/tate_convert.py` into `experiments/tate_sample.jsonl` using the field mapping documented in that script.
- License text under /licenses/: not added (CC0 waiver; source, SHA, and status recorded here).
