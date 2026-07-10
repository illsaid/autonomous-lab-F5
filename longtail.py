#!/usr/bin/env python3
"""longtail.py — query the neglected long tail of CC0 GLAM collection metadata.

Answers the three questions from DECISIONS.md (Run 4 sketch):

  tail   Show N random never-highlighted public-domain objects,
         optionally filtered by department and date range.
  share  Per-department share of never-highlighted public-domain objects.
  tags   Subject-tag frequency across records; --rare lists one-off tags
         and the objects that carry them.
  rare   Neglected-artifact generator: pick one random singleton tag and
         show the single artwork that carries it.
  era    Long-tail share by acquisition decade, with the acquisition year
         parsed from creditLine (Tate records carry no explicit field).
  show   Print one record as JSON by objectID.

Data is JSONL, one object per line, using the Met Collection API field
names (objectID, isHighlight, isPublicDomain, department, tags, ...).
Default data file is experiments/tate_stratified.jsonl — 3,458 real CC0
records from the Tate collection snapshot (see experiments/tate_fetch.sh
to regenerate or scale it). Use --data to point at any other extract,
e.g. experiments/met_fixture.jsonl.

Usage:
  python3 longtail.py tail [-n N] [--department D] [--begin YEAR] [--end YEAR] [--seed S]
  python3 longtail.py share
  python3 longtail.py tags [--rare]
  python3 longtail.py rare [--seed S]
  python3 longtail.py era
  python3 longtail.py show OBJECTID
  (all commands accept --data PATH)
"""
import argparse
import json
import random
import re
import signal
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Die quietly when output is piped to head/less etc. (POSIX only).
if hasattr(signal, "SIGPIPE"):
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

DEFAULT_DATA = Path(__file__).parent / "experiments" / "tate_stratified.jsonl"


def load(path):
    p = Path(path)
    if not p.exists():
        sys.exit(f"data file not found: {p}")
    records = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"{p} line {i}: invalid JSON: {e}")
    return records


def is_long_tail(r):
    return r.get("isPublicDomain") is True and r.get("isHighlight") is not True


def fmt(r):
    date = r.get("objectDate") or f"{r.get('objectBeginDate','?')}–{r.get('objectEndDate','?')}"
    artist = r.get("artistDisplayName") or r.get("culture") or "unknown maker"
    mark = " [synthetic fixture]" if r.get("fixture") else ""
    return (f"  {r.get('objectID')}: {r.get('title','(untitled)')} — {artist}, {date}\n"
            f"      {r.get('department','?')} | {r.get('medium','?')}{mark}")


def cmd_tail(args):
    rs = [r for r in load(args.data) if is_long_tail(r)]
    if args.department:
        rs = [r for r in rs if args.department.lower() in (r.get("department") or "").lower()]
    if args.begin is not None:
        rs = [r for r in rs if isinstance(r.get("objectEndDate"), int) and r["objectEndDate"] >= args.begin]
    if args.end is not None:
        rs = [r for r in rs if isinstance(r.get("objectBeginDate"), int) and r["objectBeginDate"] <= args.end]
    if not rs:
        print("no never-highlighted public-domain objects match")
        return
    rng = random.Random(args.seed)
    picks = rng.sample(rs, min(args.n, len(rs)))
    print(f"{len(picks)} of {len(rs)} matching long-tail objects:")
    for r in picks:
        print(fmt(r))


def cmd_share(args):
    by_dept = defaultdict(lambda: [0, 0])  # dept -> [total, long_tail]
    for r in load(args.data):
        d = r.get("department") or "(no department)"
        by_dept[d][0] += 1
        if is_long_tail(r):
            by_dept[d][1] += 1
    rows = sorted(by_dept.items(), key=lambda kv: (-(kv[1][1] / kv[1][0]), kv[0]))
    w = max(len(d) for d, _ in rows)
    print(f"{'department':<{w}}  total  long-tail  share")
    for d, (total, lt) in rows:
        print(f"{d:<{w}}  {total:>5}  {lt:>9}  {lt/total:>5.0%}")
    print("(long tail = isPublicDomain and never isHighlight)")


def cmd_tags(args):
    records = load(args.data)
    freq = Counter()
    carriers = defaultdict(list)
    for r in records:
        for t in r.get("tags") or []:
            term = t.get("term")
            if term:
                freq[term] += 1
                carriers[term].append(r)
    if not freq:
        print("no tags in data")
        return
    if args.rare:
        rare = sorted(t for t, c in freq.items() if c == 1)
        print(f"{len(rare)} tags appear exactly once:")
        for t in rare:
            r = carriers[t][0]
            print(f"  {t}: {r.get('objectID')} {r.get('title','(untitled)')}")
    else:
        print(f"{len(freq)} distinct tags across {len(records)} records:")
        for t, c in freq.most_common():
            print(f"  {c:>3}  {t}")


def cmd_rare(args):
    records = load(args.data)
    freq = Counter()
    carrier = {}
    for r in records:
        for t in r.get("tags") or []:
            term = t.get("term")
            if term:
                freq[term] += 1
                carrier.setdefault(term, r)
    singletons = sorted(t for t, c in freq.items() if c == 1)
    if not singletons:
        print("no singleton tags in data")
        return
    rng = random.Random(args.seed)
    tag = rng.choice(singletons)
    r = carrier[tag]
    print(f"Of {len(freq)} tags across {len(records)} records, "
          f"{len(singletons)} appear exactly once.")
    print(f"Singleton tag: \u201c{tag}\u201d \u2014 carried by one artwork:")
    print(fmt(r))
    if r.get("objectURL"):
        print(f"      {r['objectURL']}")


def acq_year(r):
    """Acquisition year parsed from creditLine, e.g. 'Presented by ... 1922'.

    Tate metadata has no explicit acquisition-year field in our extract;
    the credit line conventionally ends with the year. Take the last
    plausible 4-digit year (1700-2019) anywhere in the string, which also
    handles lines like 'Purchased 2006. The Artangel Collection at Tate'.
    """
    years = re.findall(r"\b(1[7-9]\d\d|20[01]\d)\b", r.get("creditLine") or "")
    return int(years[-1]) if years else None


def cmd_era(args):
    by_dec = defaultdict(lambda: [0, 0])  # decade -> [total, long_tail]
    unknown = 0
    for r in load(args.data):
        y = acq_year(r)
        if y is None:
            unknown += 1
            continue
        d = y // 10 * 10
        by_dec[d][0] += 1
        if is_long_tail(r):
            by_dec[d][1] += 1
    if not by_dec:
        print("no acquisition years parsed from creditLine")
        return
    print(f"{'acquired':<9}  total  long-tail  share")
    for d in sorted(by_dec):
        total, lt = by_dec[d]
        print(f"{str(d) + 's':<9}  {total:>5}  {lt:>9}  {lt/total:>5.0%}")
    if unknown:
        print(f"(no year parsed from creditLine for {unknown} records)")
    print("(acquisition year parsed from creditLine; long tail = isPublicDomain and never isHighlight)")


def cmd_show(args):
    for r in load(args.data):
        if r.get("objectID") == args.objectID:
            json.dump(r, sys.stdout, indent=2, ensure_ascii=False)
            print()
            return
    sys.exit(f"objectID {args.objectID} not in data")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data", default=str(DEFAULT_DATA), help="JSONL data file")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("tail", help="random never-highlighted public-domain objects")
    sp.add_argument("-n", type=int, default=5)
    sp.add_argument("--department")
    sp.add_argument("--begin", type=int, help="objects ending at/after this year (negative = BC)")
    sp.add_argument("--end", type=int, help="objects beginning at/before this year")
    sp.add_argument("--seed", type=int, help="random seed for reproducible output")
    sp.set_defaults(fn=cmd_tail)
    sub.add_parser("share", help="per-department long-tail share").set_defaults(fn=cmd_share)
    sp = sub.add_parser("tags", help="tag frequency")
    sp.add_argument("--rare", action="store_true", help="tags appearing exactly once")
    sp.set_defaults(fn=cmd_tags)
    sp = sub.add_parser("rare", help="one random singleton tag and its lone artwork")
    sp.add_argument("--seed", type=int, help="random seed for reproducible output")
    sp.set_defaults(fn=cmd_rare)
    sub.add_parser("era", help="long-tail share by acquisition decade").set_defaults(fn=cmd_era)
    sp = sub.add_parser("show", help="print one record")
    sp.add_argument("objectID", type=int)
    sp.set_defaults(fn=cmd_show)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
