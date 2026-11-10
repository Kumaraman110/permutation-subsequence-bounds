# A062714: witnesses for a(11) <= 101, a(12) <= 121, a(13) <= 144, a(14) <= 169, a(15) <= 196.
# Kumar Aman, November 2026.
#
# This entire file is valid Python 3. Run it without editing:
#     python3 a062714.txt
# or, in the GitHub bundle:
#     python3 a062714.py
#
# Each Wn is a literal Python list over the symbols 1..n.
# In complete(w, n), n is the alphabet size, not the length of w.
# Repeated symbols are allowed; their order matters, and gaps are allowed.
# The function returns True exactly when every permutation of 1..n is
# a subsequence of w. These witnesses prove upper bounds, not optimality.
#
# The recurrence is valid for every positive integer n. There is no hard
# upper limit in this Python function. For L = len(w), worst-case time is
# O(n*L + n*2**n) and memory is O(n*L + 2**n). Large n can exhaust memory
# or take a very long time; resource failure is not a False verdict.

def complete(w, n):                   # explicit alphabet: integers 1..n
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


# Small example over the three symbols 1, 2, 3:
W3 = [1, 2, 3, 1, 2, 1, 3]
# complete(W3, 3) returns True: all six permutations occur as subsequences.
# complete([1, 2, 3], 3) returns False: for example, 3, 2, 1 is absent.
# complete(W3, 4) returns False: the prescribed symbol 4 is absent.

# n = 11, length 101; complete(W11, 11) returns True.
W11 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 3, 2, 1, 4, 5, 8, 7, 6, 9,
    2, 10, 3, 11, 1, 4, 7, 5, 8, 2, 6, 9, 3, 10, 4, 1, 11, 5, 7, 2,
    8, 9, 6, 3, 4, 10, 1, 5, 2, 7, 11, 8, 3, 9, 6, 4, 10, 1, 2, 5,
    7, 3, 8, 9, 11, 4, 6, 2, 1, 10, 5, 3, 7, 9, 8, 1, 4, 2, 11, 6,
    3, 10, 5, 9, 7, 4, 8, 1, 2, 3, 11, 6, 10, 5, 7, 9, 8, 1, 4, 2,
    3,
]

# n = 12, length 121; complete(W12, 12) returns True.
W12 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 4, 5, 7, 8, 6, 3,
    10, 9, 2, 11, 1, 12, 5, 6, 7, 4, 8, 3, 2, 10, 9, 1, 11, 7, 5, 4,
    6, 12, 8, 2, 3, 10, 1, 9, 5, 4, 7, 11, 6, 2, 8, 12, 3, 1, 10, 5,
    4, 9, 7, 2, 6, 11, 8, 1, 3, 12, 10, 5, 4, 7, 2, 9, 6, 1, 8, 11,
    3, 10, 5, 4, 12, 2, 7, 9, 1, 6, 8, 4, 5, 10, 3, 11, 2, 12, 9, 1,
    7, 6, 8, 3, 5, 4, 10, 2, 1, 11, 12, 9, 10, 6, 7, 3, 8, 4, 5, 2,
    1,
]

# n = 13, length 144; complete(W13, 13) returns True.
W13 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 6, 2, 3, 5, 7, 9,
    4, 8, 12, 11, 10, 1, 13, 3, 2, 7, 5, 6, 4, 9, 8, 12, 1, 11, 6, 10,
    13, 7, 5, 3, 2, 4, 9, 1, 8, 12, 6, 11, 3, 13, 5, 7, 10, 2, 1, 9,
    4, 8, 6, 12, 7, 5, 11, 3, 13, 1, 2, 10, 9, 4, 6, 8, 7, 5, 3, 12,
    11, 1, 13, 2, 9, 10, 6, 4, 5, 7, 8, 3, 12, 1, 11, 13, 2, 6, 9, 10,
    5, 3, 7, 8, 4, 1, 12, 6, 13, 11, 2, 9, 7, 5, 8, 3, 10, 6, 1, 4,
    12, 2, 11, 13, 7, 9, 8, 5, 3, 1, 6, 10, 12, 4, 11, 8, 13, 2, 5, 9,
    7, 1, 6, 3,
]

# n = 14, length 169; complete(W14, 14) returns True.
W14 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 8, 3, 2, 1, 6, 4,
    5, 7, 10, 11, 12, 9, 13, 2, 4, 3, 8, 14, 6, 1, 5, 7, 11, 10, 12, 3,
    9, 2, 4, 13, 8, 5, 6, 1, 7, 14, 11, 10, 3, 12, 2, 4, 9, 13, 8, 1,
    5, 6, 7, 3, 10, 11, 14, 2, 4, 12, 8, 9, 13, 1, 6, 5, 3, 7, 11, 10,
    4, 2, 14, 8, 12, 6, 1, 13, 3, 9, 5, 11, 7, 10, 2, 4, 6, 8, 14, 1,
    12, 3, 13, 5, 9, 2, 7, 11, 10, 4, 8, 6, 12, 1, 3, 14, 13, 2, 5, 7,
    11, 9, 8, 4, 3, 1, 6, 10, 12, 2, 13, 14, 5, 7, 11, 4, 8, 6, 1, 3,
    9, 10, 2, 12, 5, 13, 14, 7, 4, 6, 8, 3, 1, 11, 2, 9, 10, 5, 13, 12,
    14, 3, 6, 1, 11, 7, 8, 4, 2,
]

# n = 15, length 196; complete(W15, 15) returns True.
W15 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 1, 4, 8, 6, 3,
    5, 2, 7, 11, 10, 13, 9, 12, 14, 1, 15, 4, 2, 6, 3, 7, 8, 5, 11, 13,
    10, 9, 12, 1, 14, 7, 15, 3, 2, 4, 8, 6, 13, 11, 5, 9, 1, 10, 12, 15,
    4, 3, 7, 8, 2, 14, 11, 1, 13, 6, 5, 9, 4, 10, 3, 8, 15, 2, 7, 12,
    1, 11, 13, 14, 6, 5, 4, 9, 8, 7, 3, 10, 2, 15, 1, 12, 13, 11, 14, 6,
    4, 5, 3, 8, 9, 7, 2, 10, 1, 15, 13, 12, 11, 4, 6, 5, 14, 3, 7, 2,
    8, 9, 1, 10, 15, 13, 11, 5, 4, 12, 6, 14, 7, 3, 8, 2, 1, 9, 4, 15,
    11, 10, 5, 13, 7, 12, 8, 3, 6, 14, 2, 1, 4, 9, 11, 5, 15, 10, 3, 6,
    7, 12, 8, 13, 2, 1, 4, 14, 5, 9, 11, 15, 12, 10, 3, 6, 7, 8, 1, 4,
    2, 13, 5, 15, 9, 11, 14, 10, 3, 7, 12, 2, 6, 1, 8, 4,
]

WITNESSES = {11: W11, 12: W12, 13: W13, 14: W14, 15: W15}


# Verification provenance.
# Archived enumeration reports exist for n = 11, 12, 13, 14 and 15; see NOTE.md.
# Those historical runs were not repeated and lack input/source hashes.
# Separately written counting and reverse-greedy methods rechecked completeness.
# Exact recurrence checks also confirm completeness and that every single-term
# deletion fails. Irreducibility is local minimality, not global optimality.
#
# Recurrence: next(p, x) is the first position after p occupied by x, or L+1.
# Set E(empty) = 0 and E(A) = max(next(E(A minus {x}), x) for x in A).
# E(A) is the worst greedy embedding endpoint among all orderings of A.
# The sequence is complete iff E({1,..,n}) <= L. See NOTE.md for the proof.


if __name__ == "__main__":
    print("complete(W3, 3) =", complete(W3, 3))                 # True
    print("complete([1, 2, 3], 3) =", complete([1, 2, 3], 3))   # False
    print("complete(W3, 4) =", complete(W3, 4))                 # False
    if not complete(W3, 3) or complete([1, 2, 3], 3) or complete(W3, 4):
        raise SystemExit("The small examples failed.")
    for n, w in WITNESSES.items():
        result = complete(w, n)
        print("n=%d length=%d complete=%s" % (n, len(w), result))
        if not result:
            raise SystemExit("A witness failed.")
