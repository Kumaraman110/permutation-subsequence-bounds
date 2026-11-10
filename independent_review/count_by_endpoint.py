"""Independent exact counting verifier; input symbols are 1..n, n from filename nNN.txt."""
from bisect import bisect_right
from collections import defaultdict
from hashlib import sha256
from math import factorial
from pathlib import Path
import json
import sys

def check(path):
    raw = path.read_bytes()
    word = [int(token) - 1 for token in raw.split()]
    n = int(path.stem[1:])
    assert set(word) == set(range(n)), (path.name, "wrong alphabet")
    occurrences = [[] for _ in range(n)]
    for position, letter in enumerate(word, 1):
        occurrences[letter].append(position)
    full = (1 << n) - 1
    dp = [defaultdict(int) for _ in range(1 << n)]
    dp[0][0] = 1
    failed = 0
    visited = 0
    largest_endpoint = 0
    for mask in range(1 << n):
        visited += len(dp[mask])
        remaining = full ^ mask
        continuation_count = factorial(n - mask.bit_count() - 1) if remaining else 1
        for endpoint, count in dp[mask].items():
            todo = remaining
            while todo:
                bit = todo & -todo
                todo -= bit
                letter = bit.bit_length() - 1
                positions = occurrences[letter]
                index = bisect_right(positions, endpoint)
                if index == len(positions):
                    # The first failed letter partitions missing full permutations.
                    failed += count * continuation_count
                else:
                    dp[mask | bit][positions[index]] += count
        if mask == full:
            contained = sum(dp[mask].values())
            largest_endpoint = max(dp[mask], default=None)
        # No subsequent transition can return to an already processed subset.
        dp[mask].clear()
    required = factorial(n)
    assert contained + failed == required, (n, contained, failed, required)
    return {
        "file": path.name,
        "n": n,
        "length": len(word),
        "alphabet": sorted(set(word)),
        "sha256": sha256(raw).hexdigest(),
        "permutations_contained": contained,
        "permutations_required": required,
        "missing": failed,
        "complete": contained == required,
        "largest_greedy_endpoint": largest_endpoint,
        "states_visited": visited,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 count_by_endpoint.py witnesses/n11.txt [...]")
    results = [check(Path(name)) for name in sys.argv[1:]]
    for result in results:
        print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if all(r["complete"] for r in results) else 1)
