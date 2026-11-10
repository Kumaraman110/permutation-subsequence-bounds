#!/usr/bin/env python3
"""Validate archived enumeration reports, without rerunning their computations.

Old logs were not cryptographically bound to input/source bytes. Structural
consistency is not a substitute for that missing historical provenance.
"""
from hashlib import sha256
from math import factorial
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
PATTERN = re.compile(
    r"^verify_brute: witnesses/n(\d+)\.txt: n=(\d+) length=(\d+) "
    r"first=(all|\d+) examined=(\d+) expected=(\d+) missing=(\d+) => ALL PRESENT$"
)


def parse(line, n, length, first):
    match = PATTERN.fullmatch(line.strip())
    if match is None:
        raise ValueError("Malformed or unsuccessful archived job: " + line)
    fn, nn, ll, ff, examined, expected, missing = match.groups()
    target = factorial(n) if first == "all" else factorial(n - 1)
    if (int(fn), int(nn), int(ll), ff, int(examined), int(expected), int(missing)) != (
        n, n, length, str(first), target, target, 0
    ):
        raise ValueError("Inconsistent archived job: " + line)
    return target


def main():
    legacy = ROOT / "legacy_evidence"
    initial = (legacy / "EXPECTED_OUTPUT.txt").read_text().splitlines()
    totals = {}
    for line in (legacy / "BRUTE_RESULTS.txt").read_text().splitlines():
        match = re.fullmatch(
            r"n=(\d+) length=(\d+) jobs=(\d+) permutations examined=(\d+) "
            r"expected=(\d+) missing=(\d+) => ALL PRESENT", line
        )
        if match is None:
            raise ValueError("Malformed archived summary: " + line)
        values = tuple(map(int, match.groups()))
        if values[0] in totals:
            raise ValueError("Duplicate archived summary")
        totals[values[0]] = values
    records = {}
    for n in range(11, 16):
        word_file = ROOT / "witnesses" / ("n%d.txt" % n)
        raw = word_file.read_bytes()
        word = list(map(int, raw.split()))
        length = len(word)
        if set(word) != set(range(1, n + 1)):
            raise ValueError("Wrong witness alphabet")
        files = []
        if n in (11, 12):
            candidates = [line for line in initial if line.startswith(
                "verify_brute: witnesses/n%d.txt:" % n)]
            if len(candidates) != 1:
                raise ValueError("Expected exactly one archived whole-run line")
            examined = parse(candidates[0], n, length, "all")
            files.append("legacy_evidence/EXPECTED_OUTPUT.txt")
        else:
            folder = legacy / ("brute_n%d.jobs" % n)
            expected_names = {"%d.txt" % k for k in range(1, n + 1)}
            if {p.name for p in folder.iterdir()} != expected_names:
                raise ValueError("Unexpected or missing archived shards")
            examined = 0
            for first in range(1, n + 1):
                path = folder / ("%d.txt" % first)
                examined += parse(path.read_text(), n, length, first)
                files.append(str(path.relative_to(ROOT)))
            if totals.get(n) != (n, length, n, examined, factorial(n), 0):
                raise ValueError("Archived aggregate disagrees with shards")
        if examined != factorial(n):
            raise ValueError("Archived count does not cover n!")
        records[str(n)] = {
            "n": n, "length": length, "permutations_reported": examined,
            "missing_reported": 0, "status": "archived_report_consistent",
            "files": files, "current_witness_sha256": sha256(raw).hexdigest(),
            "recomputed_in_this_review": False,
            "historical_input_and_source_hash_binding": False,
        }
    payload = {
        "format_version": 1,
        "limitation": "These uploaded logs are internally consistent. The original "
                      "runner did not record input/source hashes, so they do not "
                      "independently bind the historical runs to the current files.",
        "records": records,
    }
    (ROOT / "LEGACY_ENUMERATION_REVIEW.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("Archived enumeration reports are structurally consistent for n=11..15; "
          "historical hash binding is unavailable.")


if __name__ == "__main__":
    main()
