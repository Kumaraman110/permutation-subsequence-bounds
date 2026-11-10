#!/usr/bin/env python3
"""verify.py -- standalone checker (Python 3.6+, standard library only).

A sequence over {1..n} is COMPLETE if every permutation of {1..n} is a subsequence of it.

usage:  python3 verify.py FILE [FILE ...]        exact check by the subset recurrence (NOTE.md, Lemma 1)
        python3 verify.py --brute FILE ...       also test all n! permutations one by one (Python is slow: n <= 10)
        python3 verify.py --drop-last FILE ...   negative control: the sequence with its last term removed must be
                                                 incomplete; prints a permutation that is then missing

FILE holds one sequence: integers 1..n separated by whitespace.  n is taken to be the largest symbol in the file
and is printed, so check that it is the n you intend (n <= 20).

Exit status: 0 if every check gave the expected result; 1 if some check did not; 2 on bad input or usage.
"""
import re
import sys
from itertools import permutations

MAXN = 20


class BadInput(Exception):
    pass


def read_word(path):
    try:
        with open(path) as f:
            tokens = f.read().split()
    except OSError as e:
        raise BadInput("%s: cannot read file (%s)" % (path, e.strerror))
    if not tokens:
        raise BadInput("%s: empty" % path)
    if not all(re.match(r"^[0-9]+$", t) for t in tokens):
        raise BadInput("%s: every token must be a positive integer written in decimal digits" % path)
    w = [int(t) for t in tokens]
    n = max(w)
    if n > MAXN:
        raise BadInput("%s: symbol %d outside 1..%d" % (path, n, MAXN))
    if set(w) != set(range(1, n + 1)):
        raise BadInput("%s: the symbols must be exactly 1..n" % path)
    return w, n


def next_table(w, n):
    """nxt[p][x] = least position q with p < q <= L and w_q = x (positions are 1..L); L+1 if there is none."""
    L = len(w)
    row = [L + 1] * (n + 1)
    nxt = [None] * (L + 1)
    nxt[L] = row
    for p in range(L - 1, -1, -1):
        row = row[:]
        row[w[p]] = p + 1               # list index p holds the letter at position p+1
        nxt[p] = row
    return nxt


def worst_end(w, n):
    """E[A] = max, over orderings t of the set A, of the position at which the leftmost embedding of t ends
    (L+1 if some ordering of A is not a subsequence).  Bit x-1 of the index A stands for the letter x."""
    INF = len(w) + 1
    nxt = next_table(w, n)
    E = [0] * (1 << n)
    for A in range(1, 1 << n):
        m = 0
        for x in range(1, n + 1):
            if A >> (x - 1) & 1:
                e = E[A ^ (1 << (x - 1))]
                q = INF if e >= INF else nxt[e][x]
                if q > m:
                    m = q
        E[A] = m
    return E, nxt


def extremal_permutation(w, n, E, nxt):
    """A permutation whose leftmost embedding ends at E[full]; if the sequence is incomplete it is a missing one."""
    INF = len(w) + 1
    A = (1 << n) - 1
    rev = []
    while A:
        for x in range(1, n + 1):
            if A >> (x - 1) & 1:
                e = E[A ^ (1 << (x - 1))]
                q = INF if e >= INF else nxt[e][x]
                if q == E[A]:
                    rev.append(x)
                    A ^= 1 << (x - 1)
                    break
    return rev[::-1]


def is_subsequence(t, w):
    it = iter(w)
    return all(x in it for x in t)


def check(path, brute=False, drop_last=False):
    w, n = read_word(path)
    label = path
    if drop_last:
        w = w[:-1]
        label = path + " with last term removed"
    L = len(w)
    E, nxt = worst_end(w, n)
    e = E[(1 << n) - 1]
    complete = e <= L
    line = "verify.py: %s: n=%d length=%d E=%d => %s" % (label, n, L, e, "COMPLETE" if complete else "NOT COMPLETE")
    if drop_last and not complete:
        line += " (as expected)"
    if not complete:
        t = extremal_permutation(w, n, E, nxt)
        assert sorted(t) == list(range(1, n + 1)) and not is_subsequence(t, w)
        line += "; missing permutation: %s [confirmed by direct scan]" % " ".join(map(str, t))
    print(line)
    ok = (not complete) if drop_last else complete
    if brute:
        if n > 10:
            print("verify.py: %s: direct enumeration skipped (n > 10; use verify_brute)" % label)
        else:
            total = miss = 0
            for t in permutations(range(1, n + 1)):
                total += 1
                if not is_subsequence(t, w):
                    miss += 1
            print("verify.py: %s: direct enumeration: %d permutations, %d missing" % (label, total, miss))
            ok = ok and ((miss == 0) == complete)
    return ok


def main(argv):
    options = [a for a in argv if a.startswith("--")]
    files = [a for a in argv if not a.startswith("--")]
    if not files or any(o not in ("--brute", "--drop-last") for o in options):
        sys.stderr.write(__doc__)
        return 2
    try:
        results = [check(f, "--brute" in options, "--drop-last" in options) for f in files]
    except BadInput as e:
        sys.stderr.write("verify.py: %s\n" % e)
        return 2
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
