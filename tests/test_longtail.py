#!/usr/bin/env python3
"""Regression tests for longtail.py (stdlib-only).

Run from the repo root:  python3 tests/test_longtail.py

Pins the known-good behavior of the CLI against the default data file
(experiments/tate_stratified.jsonl, 3,458 records) so future changes
that break loading, counting, seeding, or lookup are caught.
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "longtail.py"
DATA = ROOT / "experiments" / "tate_stratified.jsonl"

sys.path.insert(0, str(ROOT))
import longtail  # noqa: E402


def run_cli(*args):
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True, text=True, cwd=ROOT,
    )


class TestData(unittest.TestCase):
    def test_default_data_loads_3458_records(self):
        records = longtail.load(DATA)
        self.assertEqual(len(records), 3458)

    def test_tag_counts(self):
        records = longtail.load(DATA)
        freq = {}
        for r in records:
            for t in r.get("tags") or []:
                term = t.get("term")
                if term:
                    freq[term] = freq.get(term, 0) + 1
        self.assertEqual(len(freq), 2595)
        self.assertEqual(sum(1 for c in freq.values() if c == 1), 1345)

    def test_highlight_proxy_split_is_non_degenerate(self):
        # Run 11: isHighlight = thumbnail presence (DECISIONS.md); the long
        # tail is the never-photographed remainder, not the whole file.
        records = longtail.load(DATA)
        lt = sum(1 for r in records if longtail.is_long_tail(r))
        self.assertEqual(lt, 556)
        self.assertEqual(len(records) - lt, 2902)


class TestCLI(unittest.TestCase):
    def test_rare_seed_42_is_reproducible(self):
        r = run_cli("rare", "--seed", "42")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("trout", r.stdout)
        self.assertIn("Rebeyrolle", r.stdout)
        self.assertIn("12338", r.stdout)
        self.assertIn("tate.org.uk", r.stdout)

    def test_show_12338_returns_valid_json(self):
        r = run_cli("show", "12338")
        self.assertEqual(r.returncode, 0, r.stderr)
        rec = json.loads(r.stdout)
        self.assertEqual(rec["objectID"], 12338)
        self.assertEqual(rec["accessionNumber"], "T00116")

    def test_tail_seeded_runs(self):
        r = run_cli("tail", "-n", "3", "--seed", "1")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("matching long-tail objects", r.stdout)

    def test_show_missing_id_exits_nonzero(self):
        r = run_cli("show", "999999999")
        self.assertNotEqual(r.returncode, 0)

    def test_era_pins_1850s_row_and_parses_every_record(self):
        # acq_year: conventional trailing year and mid-string year both parse
        self.assertEqual(longtail.acq_year({"creditLine": "Presented by Mrs John Richmond 1922"}), 1922)
        self.assertEqual(longtail.acq_year({"creditLine": "Purchased 2006. The Artangel Collection at Tate"}), 2006)
        self.assertIsNone(longtail.acq_year({"creditLine": ""}))
        r = run_cli("era")
        self.assertEqual(r.returncode, 0)
        self.assertIn("1850s       1885        261    14%", r.stdout)
        # every record in the default data yields a year
        self.assertNotIn("no year parsed", r.stdout)

    def test_data_override_with_met_fixture(self):
        r = run_cli("--data", "experiments/met_fixture.jsonl", "share")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("department", r.stdout)

    def test_survives_closed_pipe(self):
        # regression: `longtail.py tags | head -1` used to die with BrokenPipeError
        proc = subprocess.Popen(
            [sys.executable, str(CLI), "tags"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT,
        )
        proc.stdout.read(64)
        proc.stdout.close()
        proc.wait(timeout=30)
        stderr = proc.stderr.read().decode()
        proc.stderr.close()
        self.assertNotIn("BrokenPipeError", stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
