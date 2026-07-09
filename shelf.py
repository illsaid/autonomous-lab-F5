#!/usr/bin/env python3
"""shelf.py — a tiny catalog of neglected public artifacts.

The Wide Shelf: each entry records a neglected public artifact
(old web page, public-domain text, open dataset, dead API, small
tool, cultural fragment) as metadata only. Entries are one JSON
object per line in catalog.jsonl.

Usage:
  python3 shelf.py list [--kind KIND]
  python3 shelf.py add --id ID --kind KIND --title TITLE --url URL --why WHY [--license LICENSE]
  python3 shelf.py random
  python3 shelf.py stats
"""
import argparse
import datetime
import json
import random
import sys
from pathlib import Path

CATALOG = Path(__file__).parent / "catalog.jsonl"


def load():
    if not CATALOG.exists():
        return []
    entries = []
    for i, line in enumerate(CATALOG.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"catalog.jsonl line {i} is not valid JSON: {e}")
    return entries


def save_entry(entry):
    with CATALOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def cmd_list(args):
    entries = load()
    if args.kind:
        entries = [e for e in entries if e.get("kind") == args.kind]
    if not entries:
        print("(shelf is empty)")
        return
    for e in entries:
        print(f"[{e.get('kind','?')}] {e.get('id')}: {e.get('title')}")
        print(f"    {e.get('url')}")
        print(f"    why: {e.get('why')}")


def cmd_add(args):
    entries = load()
    if any(e.get("id") == args.id for e in entries):
        sys.exit(f"id already on shelf: {args.id}")
    entry = {
        "id": args.id,
        "kind": args.kind,
        "title": args.title,
        "url": args.url,
        "why": args.why,
        "license": args.license,
        "added": datetime.date.today().isoformat(),
    }
    save_entry(entry)
    print(f"shelved: {args.id}")


def cmd_random(args):
    entries = load()
    if not entries:
        sys.exit("shelf is empty")
    e = random.choice(entries)
    print(json.dumps(e, indent=2, ensure_ascii=False))


def cmd_stats(args):
    entries = load()
    kinds = {}
    for e in entries:
        kinds[e.get("kind", "?")] = kinds.get(e.get("kind", "?"), 0) + 1
    print(f"total: {len(entries)}")
    for k in sorted(kinds):
        print(f"  {k}: {kinds[k]}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("list"); sp.add_argument("--kind"); sp.set_defaults(fn=cmd_list)
    sp = sub.add_parser("add")
    for req in ("--id", "--kind", "--title", "--url", "--why"):
        sp.add_argument(req, required=True)
    sp.add_argument("--license", default="unknown (metadata only)")
    sp.set_defaults(fn=cmd_add)
    sub.add_parser("random").set_defaults(fn=cmd_random)
    sub.add_parser("stats").set_defaults(fn=cmd_stats)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
