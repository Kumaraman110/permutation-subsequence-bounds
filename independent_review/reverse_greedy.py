#!/usr/bin/env python3
"""Independent reverse-greedy subset certificate for permutation completeness.

This checker does not import any search code or another verifier.
"""
from bisect import bisect_left
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import json
import sys


def is_subsequence(word, permutation):
    j = 0
    for symbol in word:
        if j < len(permutation) and symbol == permutation[j]:
            j += 1
    return j == len(permutation)


def check(word, n):
    # lo[S] is the earliest starting position over the rightmost greedy
    # embeddings of every permutation of S; -1 denotes a missing ordering.
    occurrences = [[] for _ in range(n)]
    for pos, symbol in enumerate(word):
        if not 0 <= symbol < n:
            raise ValueError("Symbol outside the claimed alphabet")
        occurrences[symbol].append(pos)
    lo = [len(word)] * (1 << n)
    first = [-1] * (1 << n)
    for subset in range(1, 1 << n):
        remaining = subset
        best = len(word)
        choice = -1
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            symbol = bit.bit_length() - 1
            boundary = lo[subset ^ bit]
            index = bisect_left(occurrences[symbol], boundary) - 1
            start = occurrences[symbol][index] if index >= 0 else -1
            if start < best:
                best, choice = start, symbol
        lo[subset], first[subset] = best, choice
    subset = (1 << n) - 1
    witness = []
    while subset:
        symbol = first[subset]
        witness.append(symbol)
        subset ^= 1 << symbol
    complete = lo[-1] >= 0
    if not complete:
        assert sorted(witness) == list(range(n))
        assert not is_subsequence(word, witness)
    else:
        assert is_subsequence(word, witness)
    return {"complete": complete, "earliest_worst_start": lo[-1],
            "witness": witness}


def small_exhaustive_test():
    tested = 0
    for n in (1, 2, 3):
        for length in range(0, 7):
            for word in product(range(n), repeat=length):
                expected = all(is_subsequence(word, p)
                               for p in permutations(range(n)))
                assert check(word, n)["complete"] == expected
                tested += 1
    return tested


def main():
    names = sys.argv[1:]
    if names == ["--self-test"]:
        print("small exhaustive words:", small_exhaustive_test())
        return 0
    if not names:
        raise SystemExit("usage: python3 reverse_greedy.py witnesses/n11.txt [...] | --self-test")
    results = []
    for name in names:
        path = Path(name)
        n = int(path.stem[1:])
        raw = path.read_bytes()
        word = [int(t) - 1 for t in raw.split()]
        if set(word) != set(range(n)):
            raise ValueError("Input alphabet does not match filename")
        result = check(word, n)
        row = {"file": path.name, "n": n, "length": len(word),
               "sha256": sha256(raw).hexdigest(), "verification": result}
        results.append(row)
        print(json.dumps(row, sort_keys=True))
    return 0 if all(r["verification"]["complete"] for r in results) else 1

if __name__ == "__main__":
    raise SystemExit(main())
