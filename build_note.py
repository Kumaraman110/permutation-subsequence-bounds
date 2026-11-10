#!/usr/bin/env python3
"""build_note.py -- regenerate the note, guide and runnable witness files.

Inputs: witnesses/n*.txt, NOTE.template.md, OEIS_SUBMISSION_GUIDE.template.txt, SHA256SUMS, EXPECTED_OUTPUT.txt,
BRUTE_RESULTS.txt (optional), priority_note.txt, review_note.txt.

Nothing here is needed to verify the witnesses.  The script only guarantees that the printed sequences and the
tables are produced mechanically from the witness files and from recorded program output, never typed by hand."""
import math
import json
import hashlib
from pathlib import Path
import os
import re
import prior_bounds as pb

DATE = "10 November 2026"
CONTRIBUTOR = "Kumar Aman"
NS = [11, 12, 13, 14, 15]
SYM = "0123456789abcdef"            # symbol value -> character (1..9, then a..f for 10..15)

SNIPPET = '''def complete(w, n):                   # explicit alphabet: integers 1..n
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    if any(type(x) is not int or not 1 <= x <= n for x in w):
        raise ValueError("symbol outside the prescribed alphabet")
    L = len(w)
    if len(set(w)) < n:
        return False                         # a prescribed symbol is absent
    nxt = [[L + 1] * (n + 1) for _ in range(L + 2)]
    for p in range(L - 1, -1, -1):
        nxt[p] = nxt[p + 1][:]
        nxt[p][w[p]] = p + 1
    E = [0] * (1 << n)
    for A in range(1, 1 << n):
        E[A] = max(nxt[E[A ^ (1 << x)]][x + 1] for x in range(n) if A >> x & 1)
    return E[-1] <= L
'''


def word(n):
    return [int(t) for t in open("witnesses/n%d.txt" % n).read().split()]


def compact(w):
    s = "".join(SYM[v] for v in w)
    blocks = [s[i:i + 10] for i in range(0, len(s), 10)]
    return "\n".join(" ".join(blocks[i:i + 5]) for i in range(0, len(blocks), 5))


def bounds_table():
    rows = ["| n | length of W_n | n² − 2n + 4 | [Zal11] n² − 2n + 3 | [Rad12] ⌈n² − 7n/3 + 19/3⌉ | [Tan22] Thm 23, s ≥ 2 "
            "| smallest among cited constructions | improvement | (n − 1)² |",
            "|---|---|---|---|---|---|---|---|---|"]
    for n in NS:
        L = len(word(n))
        t23 = ["%d (s = %d)" % (pb.tan23(n, s), s) for s in range(2, n) if pb.tan23(n, s) is not None]
        best = pb.best(n)
        assert L < best
        rows.append("| %d | **%d** | %d | %d | %d | %s | %d | %d | %d |" % (
            n, L, pb.classical(n), pb.zalinescu(n), pb.radomirovic(n), ", ".join(t23) if t23 else "—",
            best, best - L, (n - 1) ** 2))
    return "\n".join(rows)


def recorded_results():
    """Program output recorded in EXPECTED_OUTPUT.txt (run_all.sh) and BRUTE_RESULTS.txt (run_brute_parallel.sh)."""
    info = {n: {} for n in NS}
    for line in open("EXPECTED_OUTPUT.txt"):
        m = re.match(r"(verify\.py|verify_dp|verify_brute): witnesses/n(\d+)\.txt: (.*)", line)
        if m and int(m.group(2)) in info:
            info[int(m.group(2))][m.group(1)] = m.group(3).strip()
    if os.path.exists("BRUTE_RESULTS.txt"):
        for line in open("BRUTE_RESULTS.txt"):
            m = re.match(r"n=(\d+) length=(\d+) jobs=(\d+) permutations examined=(\d+) expected=(\d+) missing=(\d+) => (.*)", line)
            if m and int(m.group(1)) in info:
                info[int(m.group(1))]["parallel"] = tuple(int(g) for g in m.groups()[:6]) + (m.group(7).strip(),)
    return info


def direct_report(n):
    """Distinguish newly hash-bound run records from unbound uploaded reports."""
    witness = Path("witnesses/n%d.txt" % n)
    L, fact = len(word(n)), math.factorial(n)
    digest = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if Path("BRUTE_MANIFEST.json").exists():
        payload = json.loads(Path("BRUTE_MANIFEST.json").read_text())
        record = payload.get("records", {}).get(str(n))
        if record is not None:
            wanted = (n, L, n, fact, fact, 0, "ALL PRESENT")
            actual = tuple(record[k] for k in ("n", "length", "jobs", "permutations_examined",
                                               "permutations_expected", "missing", "verdict"))
            if actual != wanted or record["witness_sha256"] != digest(witness) or record["verifier_sha256"] != digest("verify_brute.c"):
                raise ValueError("Enumeration manifest does not match current files")
            jobs = record["per_first_letter"]
            if sorted(j["first"] for j in jobs) != list(range(1, n + 1)):
                raise ValueError("Enumeration manifest has missing or duplicate jobs")
            for job in jobs:
                if (job["examined"], job["expected"], job["missing"], job["verdict"]) != (math.factorial(n-1), math.factorial(n-1), 0, "ALL PRESENT"):
                    raise ValueError("Bad job count in enumeration manifest")
                if digest(job["output_file"]) != job["output_sha256"]:
                    raise ValueError("Enumeration job output changed")
            return "hash-bound run log"
    legacy = Path("LEGACY_ENUMERATION_REVIEW.json")
    if legacy.exists():
        record = json.loads(legacy.read_text()).get("records", {}).get(str(n))
        if record and record["status"] == "archived_report_consistent":
            if (record["length"], record["permutations_reported"], record["missing_reported"], record["current_witness_sha256"]) != (L, fact, 0, digest(witness)):
                raise ValueError("Archived report audit is stale")
            return "archived report (not rerun)"
    return None


def verif_table(info):
    rows = ["| n | length L | n! | direct enumeration (`verify_brute`) | recurrence, C (`verify_dp`) | recurrence, Python (`verify.py`) | irreducible |",
            "|---|---|---|---|---|---|---|"]
    for n in NS:
        L = len(word(n))
        d = info[n]
        py = re.match(r"n=%d length=%d E=(\d+) => COMPLETE$" % (n, L), d["verify.py"])
        c = re.match(r"n=%d length=%d E=(\d+) => COMPLETE; single-term deletions that stay complete: (\d+) of %d => IRREDUCIBLE$"
                     % (n, L, L), d["verify_dp"])
        assert py and c and int(py.group(1)) == L and int(c.group(1)) == L and int(c.group(2)) == 0
        fact = "{:,}".format(math.factorial(n))
        status = direct_report(n)
        brute = ("%s: %s examined, 0 missing" % (status, fact)) if status else "no completed run record"
        rows.append("| %d | %d | %s | %s | complete, E([n]) = %d | complete, E([n]) = %d | yes (0 of %d single deletions stay complete) |"
                    % (n, L, fact, brute, int(c.group(1)), int(py.group(1)), L))
    return "\n".join(rows)


def english_list(items):
    items = [str(i) for i in items]
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def afile(info):
    ns = {}
    exec(SNIPPET, ns)                                   # the published snippet is itself tested here
    done = [n for n in NS if direct_report(n)]
    out = ["# A062714: witnesses for a(11) <= 101, a(12) <= 121, a(13) <= 144, a(14) <= 169, a(15) <= 196.",
           "# " + CONTRIBUTOR + ", November 2026.", "#",
           "# This entire file is valid Python 3. Run it without editing:",
           "#     python3 a062714.txt", "# or, in the GitHub bundle:",
           "#     python3 a062714.py", "#",
           "# Each Wn is a literal Python list over the symbols 1..n.",
           "# In complete(w, n), n is the alphabet size, not the length of w.",
           "# Repeated symbols are allowed; their order matters, and gaps are allowed.",
           "# The function returns True exactly when every permutation of 1..n is",
           "# a subsequence of w. These witnesses prove upper bounds, not optimality.", "#",
           "# The recurrence is valid for every positive integer n. There is no hard",
           "# upper limit in this Python function. For L = len(w), worst-case time is",
           "# O(n*L + n*2**n) and memory is O(n*L + 2**n). Large n can exhaust memory",
           "# or take a very long time; resource failure is not a False verdict.", ""]
    out += SNIPPET.rstrip("\n").split("\n")
    out += ["", "", "# Small example over the three symbols 1, 2, 3:",
            "W3 = [1, 2, 3, 1, 2, 1, 3]",
            "# complete(W3, 3) returns True: all six permutations occur as subsequences.",
            "# complete([1, 2, 3], 3) returns False: for example, 3, 2, 1 is absent.",
            "# complete(W3, 4) returns False: the prescribed symbol 4 is absent.", ""]
    for n in NS:
        w = word(n)
        assert ns["complete"](w, n) and not ns["complete"](w[:-1], n)
        out += ["# n = %d, length %d; complete(W%d, %d) returns True." % (n, len(w), n, n),
                "W%d = [" % n]
        out += ["    " + ", ".join(map(str, w[i:i + 20])) + "," for i in range(0, len(w), 20)]
        out += ["]", ""]
    out += ["WITNESSES = {11: W11, 12: W12, 13: W13, 14: W14, 15: W15}", "", "",
            "# Verification provenance.",
            "# Archived enumeration reports exist for n = %s; see NOTE.md." % english_list(done),
            "# Those historical runs were not repeated and lack input/source hashes.",
            "# Separately written counting and reverse-greedy methods rechecked completeness.",
            "# Exact recurrence checks also confirm completeness and that every single-term",
            "# deletion fails. Irreducibility is local minimality, not global optimality.", "#",
            "# Recurrence: next(p, x) is the first position after p occupied by x, or L+1.",
            "# Set E(empty) = 0 and E(A) = max(next(E(A minus {x}), x) for x in A).",
            "# E(A) is the worst greedy embedding endpoint among all orderings of A.",
            "# The sequence is complete iff E({1,..,n}) <= L. See NOTE.md for the proof.", "", "",
            'if __name__ == "__main__":',
            '    print("complete(W3, 3) =", complete(W3, 3))                 # True',
            '    print("complete([1, 2, 3], 3) =", complete([1, 2, 3], 3))   # False',
            '    print("complete(W3, 4) =", complete(W3, 4))                 # False',
            '    if not complete(W3, 3) or complete([1, 2, 3], 3) or complete(W3, 4):',
            '        raise SystemExit("The small examples failed.")',
            '    for n, w in WITNESSES.items():',
            '        result = complete(w, n)',
            '        print("n=%d length=%d complete=%s" % (n, len(w), result))',
            '        if not result:',
            '            raise SystemExit("A witness failed.")']
    return "\n".join(out) + "\n"


def fill(template, values):
    for k, v in values.items():
        assert "{{%s}}" % k in template, k
        template = template.replace("{{%s}}" % k, v)
    assert "{{" not in template, re.findall(r"\{\{.*?\}\}", template)
    return template


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    from audit_legacy_runs import main as audit_legacy
    audit_legacy()
    info = recorded_results()
    values = {"DATE": DATE, "TABLE_BOUNDS": bounds_table(), "VERIF_TABLE": verif_table(info),
              "SHA": open("SHA256SUMS").read().rstrip("\n"),
              "PRIORITY_NOTE": open("priority_note.txt").read().strip(),
              "REVIEW_NOTE": open("review_note.txt").read().strip()}
    for n in NS:
        values["W%d" % n] = compact(word(n))
    open("NOTE.md", "w").write(fill(open("NOTE.template.md").read(), values))
    open("OEIS_SUBMISSION_GUIDE.txt", "w").write(fill(open("OEIS_SUBMISSION_GUIDE.template.txt").read(), {"DATE": DATE}))
    witness_program = afile(info)
    open("a062714.txt", "w").write(witness_program)
    open("a062714.py", "w").write(witness_program)
    print("wrote NOTE.md, OEIS_SUBMISSION_GUIDE.txt, a062714.txt, a062714.py")


if __name__ == "__main__":
    main()
