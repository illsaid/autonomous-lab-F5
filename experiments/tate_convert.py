#!/usr/bin/env python3
"""tate_convert.py — convert Tate collection artwork JSON to met_tail JSONL.

Source: github.com/tategallery/collection (CC0 1.0, frozen Oct 2014 —
itself a neglected public artifact: ~70k artwork records kept online
"in case this snapshot ... is useful"). Artwork files are plain git
blobs, so acquisition works from this runner (unlike Met/MoMA/Smithsonian,
whose bulk data is LFS- or egress-blocked; see RESEARCH_LOG.md Run 6).

Field mapping (Tate -> met_tail schema):
  id                -> objectID
  title             -> title
  all_artists       -> artistDisplayName
  dateText          -> objectDate
  dateRange.startYear/endYear -> objectBeginDate/objectEndDate
  classification    -> department   (Tate has no departments; its coarse
                                     classification plays the same role)
  medium            -> medium
  creditLine        -> creditLine
  acno              -> accessionNumber
  url               -> objectURL
  subjects tree leaves -> tags [{"term": name}]
  isPublicDomain    -> True  (metadata is CC0; images NOT included/covered)
  isHighlight       -> False (Tate publishes no highlight flag; recorded
                              as a known limitation — the 'share' view is
                              therefore classification coverage, not a
                              true highlight split)
  source            -> "tategallery/collection@HEAD (CC0)"

Usage:
  python3 tate_convert.py SRC_DIR [-o OUT.jsonl] [--limit N]
SRC_DIR is scanned recursively for *.json artwork files.
"""
import argparse
import json
import sys
from pathlib import Path

SOURCE = "tategallery/collection (CC0 1.0, snapshot Oct 2014)"


def leaf_terms(node, out):
    kids = node.get("children")
    if kids:
        for k in kids:
            leaf_terms(k, out)
    else:
        name = node.get("name")
        if name:
            out.append(name)


def convert(rec):
    dr = rec.get("dateRange") or {}
    tags = []
    leaf_terms(rec.get("subjects") or {}, tags)
    return {
        "objectID": rec.get("id"),
        "accessionNumber": rec.get("acno"),
        "isPublicDomain": True,
        "isHighlight": False,
        "title": rec.get("title") or "(untitled)",
        "artistDisplayName": rec.get("all_artists") or "",
        "objectDate": rec.get("dateText") or "",
        "objectBeginDate": dr.get("startYear"),
        "objectEndDate": dr.get("endYear"),
        "department": rec.get("classification") or "(unclassified)",
        "medium": rec.get("medium") or "",
        "creditLine": rec.get("creditLine") or "",
        "objectURL": rec.get("url") or "",
        "tags": [{"term": t} for t in sorted(set(tags))],
        "source": SOURCE,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("src", help="directory of Tate artwork JSON files")
    p.add_argument("-o", "--out", default="tate_sample.jsonl")
    p.add_argument("--limit", type=int, default=None)
    a = p.parse_args()
    files = sorted(Path(a.src).rglob("*.json"))
    if a.limit:
        files = files[: a.limit]
    if not files:
        sys.exit(f"no .json files under {a.src}")
    n = bad = 0
    with open(a.out, "w", encoding="utf-8") as f:
        for fp in files:
            try:
                rec = json.loads(fp.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"skip {fp}: {e}", file=sys.stderr)
                bad += 1
                continue
            f.write(json.dumps(convert(rec), ensure_ascii=False) + "\n")
            n += 1
    print(f"wrote {n} records to {a.out} ({bad} skipped)")


if __name__ == "__main__":
    main()
