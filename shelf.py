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
  python3 shelf.py probe [ID ...] [--all] [--timeout SECONDS]
"""
import argparse
import datetime
import json
import random
import sys
import urllib.error
import urllib.request
from pathlib import Path

CATALOG = Path(__file__).parent / "catalog.jsonl"
USER_AGENT = "wide-shelf-probe/0.1 (+https://github.com/illsaid/autonomous-lab-F5)"


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


def save_all(entries):
    tmp = CATALOG.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    tmp.replace(CATALOG)


def cmd_list(args):
    entries = load()
    if args.kind:
        entries = [e for e in entries if e.get("kind") == args.kind]
    if not entries:
        print("(shelf is empty)")
        return
    for e in entries:
        status = e.get("last_status")
        badge = f" [{status} @ {e.get('last_checked')}]" if status is not None else ""
        print(f"[{e.get('kind','?')}] {e.get('id')}: {e.get('title')}{badge}")
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
    probed = sum(1 for e in entries if e.get("last_status") is not None)
    alive = sum(1 for e in entries if isinstance(e.get("last_status"), int)
                and 200 <= e["last_status"] < 400)
    for e in entries:
        kinds[e.get("kind", "?")] = kinds.get(e.get("kind", "?"), 0) + 1
    print(f"total: {len(entries)}")
    for k in sorted(kinds):
        print(f"  {k}: {kinds[k]}")
    print(f"probed: {probed}  alive: {alive}")


def probe_url(url, timeout):
    """Return an int HTTP status, or a short error string."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read(1)  # confirm the body is actually readable
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return f"error: {getattr(e, 'reason', e)}"
    except Exception as e:  # timeout, bad handshake, etc.
        return f"error: {type(e).__name__}: {e}"


def cmd_probe(args):
    entries = load()
    if not entries:
        sys.exit("shelf is empty")
    if args.all:
        targets = entries
    elif args.ids:
        by_id = {e.get("id"): e for e in entries}
        missing = [i for i in args.ids if i not in by_id]
        if missing:
            sys.exit(f"not on shelf: {', '.join(missing)}")
        targets = [by_id[i] for i in args.ids]
    else:
        sys.exit("give one or more IDs, or --all")
    today = datetime.date.today().isoformat()
    for e in targets:
        status = probe_url(e["url"], args.timeout)
        e["last_status"] = status
        e["last_checked"] = today
        ok = isinstance(status, int) and 200 <= status < 400
        mark = "ok " if ok else "!! "
        print(f"{mark}{e['id']}: {status}")
    save_all(entries)
    print(f"({len(targets)} probed, catalog updated)")


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
    sp = sub.add_parser("probe")
    sp.add_argument("ids", nargs="*")
    sp.add_argument("--all", action="store_true")
    sp.add_argument("--timeout", type=float, default=10.0)
    sp.set_defaults(fn=cmd_probe)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
