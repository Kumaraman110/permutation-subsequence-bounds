# Explicit upper bounds for permutation-complete sequences at n = 11, 12, 13, 14, 15

Revised draft of {{DATE}}, prepared for independent review and as supporting material for an OEIS contribution.
Contributor: Kumar Aman. The original search and draft were prepared with Claude (Anthropic); this revision and independent checks were prepared with Codex (OpenAI). These tools are not listed as authors; see §7.

Submission status as of 10 November 2026: a comment and supporting file were submitted to OEIS A062714 by Kumar Aman. The supporting file was revised following usability feedback and the update was marked proposed in revision 139. Editorial approval is pending. The revised attachment is https://oeis.org/A062714/a062714_1.txt.

## 1. Statement

Write [n] = {1, 2, …, n}. A finite sequence w over [n] is **complete** if each of the n! permutations of [n] is a subsequence of w (its terms occur in w in the same order, not necessarily adjacently). Let a(n) be the least length of a complete sequence over [n]. This is OEIS A062714 [OEIS]; the problem is attributed to R. M. Karp [CKK72, Problem 36]. The OEIS entry lists a(1), …, a(9) = 1, 3, 7, 12, 19, 28, 39, 52, 66 and no further terms.

**Theorem.** a(11) ≤ 101, a(12) ≤ 121, a(13) ≤ 144, a(14) ≤ 169 and a(15) ≤ 196.

*Proof.* The sequences W11, …, W15 printed in §3 have these lengths and each of them is complete. Completeness of a given sequence is a finite verification; §4 gives a proved recurrence verifying all five witnesses, independent exact checks reproduced in this review, and additional archived direct-enumeration reports. ∎

**Corollary.** a(n) ≤ (n − 1)² for every n ≥ 12.

*Proof.* W12, W13, W14, W15 have lengths 11², 12², 13², 14². For n ≥ 16 use Radomirović's bound a(n) ≤ ⌈n² − 7n/3 + 19/3⌉ [Rad12]: because (n − 1)² is an integer, ⌈n² − 7n/3 + 19/3⌉ ≤ (n − 1)² is equivalent to n² − 7n/3 + 19/3 ≤ n² − 2n + 1, that is, to n ≥ 16. ∎

W11 has length 101 = 10² + 1, so n = 11 is not covered by the Corollary. For n ≤ 9 the known values satisfy a(n) > (n − 1)². For n = 10 and n = 11 the constructions compared here give upper bounds 83 and 101, against 81 and 100; these constructions do not establish the square bound for either alphabet size.

**Not claimed.** (i) *Optimality.* These are upper bounds. No lower bound is proved here, and a(n) is not known for any n ≥ 10. (ii) *Priority.* §2 compares with the bounds found in the literature and in the OEIS on {{DATE}}. Whether equally short or shorter sequences had been found earlier and not published where we looked is a separate question, which this note cannot settle.

## 2. Comparison with published upper bounds

{{TABLE_BOUNDS}}

The published bounds used, with their stated ranges (n is always the alphabet size):

* n² − 2n + 4 for n ≥ 3: Newey [New73]; also Adleman [Adl74], Koutas and Hu [KH75], Galbiati and Preparata [GP76], Mohanty [Moh80]. Newey showed that this is the exact value for 3 ≤ n ≤ 7.
* n² − 2n + 3 for n ≥ 10: Zălinescu [Zal11].
* ⌈n² − 7n/3 + 19/3⌉ for n ≥ 7: Radomirović [Rad12].
* Tan [Tan22]. The theorem numbering and formulas here refer to arXiv:2201.06306v2, revised 4 January 2025; the journal version appeared in 2022. That version of the preprint writes m for the alphabet size and states the hypotheses of its Theorem 23 for n = m − 1 (namely n ≥ 4s + 1 and n ≡ 3 (mod 2s − 1)); below everything is restated for the alphabet size, called n here, and s ≥ 1 is an integer parameter.
  * Theorem 23: if n ≥ 4s + 2 and n ≡ 4 (mod 2s − 1), then a(n) ≤ n² − ((5s − 3)/(2s − 1))·n + (2s² + 9s − 7)/(2s − 1). For s = 1 this is n² − 2n + 4; for s = 2 it is n² − 7n/3 + 19/3, with n ≡ 1 (mod 3) and n ≥ 10.
  * Theorem 26: if n ≥ 4s + 2, then a(n) ≤ ⌈n² − ((5s − 3)/(2s − 1))·n + (4s³ − 10s² + 21s − 11)/(2s − 1)⌉.
  * Theorem 28: for every n, a(n) ≤ ⌈n² − (5/2)n + (3/2)(n/2)^(2/3) + (n/2)^(1/3) + 7⌉.

  For 11 ≤ n ≤ 15 the only instances of Theorem 23 with s ≥ 2 are (n, s) = (13, 2), giving 145, and (14, 3), giving 170. Theorems 26 and 28 give values larger than [Rad12] for every n from 10 to 20.

Hence the smallest upper bounds among the cited constructions for n = 11, …, 15 are 102, 123, 145, 170, 197, each of them given by [Rad12]. `python3 prior_bounds.py` evaluates all the formulas above, with their conditions, for 10 ≤ n ≤ 20.

Exact values. a(n) for 3 ≤ n ≤ 7 is due to Newey [New73]. a(8) = 52 was proved by Tan [Tan25]. a(9) = 66 is recorded in [OEIS] as computed by V. Garnashevich (October 2025).

## 3. The witnesses

Each sequence is written with the symbols 1, …, 9, a, b, c, d, e, f, where a, …, f stand for 10, …, 15 (the convention already used in the comments of the OEIS entry). Spaces and line breaks are for readability only. The sequences are normalized so that the symbols make their first appearances in increasing order; relabelling the alphabet does not affect completeness.

**W11** (n = 11, length 101)

```
{{W11}}
```

**W12** (n = 12, length 121)

```
{{W12}}
```

**W13** (n = 13, length 144)

```
{{W13}}
```

**W14** (n = 14, length 169)

```
{{W14}}
```

**W15** (n = 15, length 196)

```
{{W15}}
```

The same sequences as whitespace-separated integers are in `witnesses/n11.txt`, …, `witnesses/n15.txt`. The proposed OEIS supporting file `a062714.txt` supplies literal Python lists, the function `complete(w, n)`, and executable examples; the identical program is also provided as `a062714.py`. Run `python3 a062714.txt` or `python3 a062714.py` without editing. SHA-256 of the whitespace-separated witness files:

```
{{SHA}}
```

## 4. Verification

### 4.1 Direct enumeration

`verify_brute.c` examines every permutation of [n]. It walks the tree of prefixes depth-first, matching each further letter at the leftmost position after the previous match. By the Fact below, a prefix is a subsequence of w exactly when this matching does not run off the end. So every permutation is individually found present (it is reached as a leaf) or missing (it lies below a prefix that failed, and all completions of that prefix are then counted as missing). The program prints the number of permutations examined, which must equal n!, and the number missing. It uses no dynamic programming.

### 4.2 A subset recurrence

Let w = w₁w₂…w_L. For 0 ≤ p ≤ L and x ∈ [n] let next(p, x) be the least q with p < q ≤ L and w_q = x, and let next(p, x) = ∞ if there is no such q; also put next(∞, x) = ∞. For a sequence τ of distinct letters define end(τ) recursively by end(empty sequence) = 0 and end(τx) = next(end(τ), x).

**Fact (leftmost embedding).** τ is a subsequence of w if and only if end(τ) < ∞, and then end(τ) is the smallest position at which an occurrence of τ in w can end.

*Proof.* Induction on the length of τ; the empty sequence is clear. Suppose τx occurs in w at positions i₁ < … < i_k < i (with i₀ = 0 when τ is empty). Then τ occurs ending at i_k, so by induction end(τ) ≤ i_k < i; since w_i = x, next(end(τ), x) ≤ i. Hence end(τx) < ∞ and end(τx) is at most the end of any occurrence. Conversely, if end(τx) < ∞ then end(τ) < ∞, and appending the position end(τx) to an occurrence of τ that ends at end(τ) gives an occurrence of τx ending at end(τx). ∎

For A ⊆ [n] let E(A) be the maximum of end(τ) over all orderings τ of A, with E(∅) = 0.

**Lemma 1.** For every non-empty A ⊆ [n], E(A) = max over x ∈ A of next(E(A ∖ {x}), x). Consequently w is complete if and only if E([n]) ≤ L, and E([n]) can be computed with O(n·2ⁿ) evaluations of next.

*Proof.* For fixed x the map p ↦ next(p, x) is non-decreasing on {0, 1, …, L, ∞}, because enlarging p shrinks the set of admissible q. The orderings of A that end in x are exactly the τx with τ an ordering of A ∖ {x}; therefore the maximum of end(τx) = next(end(τ), x) over these τ equals next(max end(τ), x) = next(E(A ∖ {x}), x). Taking the maximum over x ∈ A gives the recurrence. By the Fact, w is complete if and only if end(τ) < ∞ for every ordering τ of [n], that is, E([n]) < ∞, that is, E([n]) ≤ L. ∎

`verify_dp.c` and `verify.py` are two separate implementations of this recurrence, with L + 1 in the role of ∞. When a sequence is not complete, `verify.py` also reconstructs from the recurrence a specific permutation τ with end(τ) = ∞ and confirms by a direct scan that it is not a subsequence.

The standalone Python function `complete(w, n)` in `a062714.py` uses an explicit positive alphabet size and has no fixed upper bound on n. Its dynamic tables require O(nL + 2ⁿ) memory and O(nL + n·2ⁿ) worst-case time for a word of length L. Large alphabets may therefore be impractical; a resource failure does not certify incompleteness. For example, `complete([1, 2, 3, 1, 2, 1, 3], 3)` returns `True`, while `complete([1, 2, 3], 3)` returns `False`. The full supporting file can be run directly and prints these examples followed by the results for all five witnesses.

### 4.3 Results

{{VERIF_TABLE}}

The direct-enumeration column labels the provenance of its run records. The uploaded archive includes completed reports for all 15 first-letter jobs at n = 15, with a total of 1,307,674,368,000 permutations and zero reported missing; the original generated draft had not incorporated those completed files. `audit_legacy_runs.py` checks every archived job's alphabet size, length, first letter, expected count and aggregate. These historical computations were not rerun in this review. Their original wrapper did not record witness/source hashes, so the archived logs do not independently establish which exact file bytes were used. They are retained as historical supporting reports, separate from the fresh exact checks below. Fresh runs made with the repaired wrapper are hash-bound to input and source snapshots.

"Irreducible" means that deleting any single term leaves a sequence that is not complete; `verify_dp --irreducible` checks this for every position. It is a statement of local minimality only and does not show that no shorter complete sequence exists.

Negative controls: for each witness, the sequence with its last term removed is reported as not complete, together with an explicit missing permutation (see `EXPECTED_OUTPUT.txt`).

### 4.4 How to reproduce

Requirements for the full default checks: a POSIX shell; a C compiler available as `cc` (GCC or Clang; `verify_brute.c` uses `__builtin_ctz` and `__builtin_popcount`); Python 3.8 or later (standard library only); `shasum` or `sha256sum`; and, for `run_brute_parallel.sh`, Python handles parallel jobs and integer-exact aggregation. The existing command-line checkers retain an operational limit n ≤ 20; the C checkers additionally limit sequences to 2000 terms. These implementation limits do not apply to the standalone Python function in `a062714.py`. The optional independent counting checker requires Python 3.10 or newer.

```
python3 a062714.py                           # Python-only examples and all five witness checks
sh run_all.sh                                # fast default: checksums, bounds, both recurrence checkers,
                                             # irreducibility and negative controls; no factorial enumeration
BRUTE_MAX=12 sh run_all.sh                   # optional slow direct enumeration for n = 11 and 12
sh run_all.sh | diff - EXPECTED_OUTPUT.txt   # the output is deterministic; no difference is expected
sh run_brute_parallel.sh 13 4                # brute force for n = 13: 13 jobs (one per first letter), 4 at a time
sh run_brute_parallel.sh 14 4                # n = 14: 87,178,291,200 permutations
sh run_brute_parallel.sh 15 4                # n = 15: 1,307,674,368,000 permutations (hours of CPU time)
```

`run_brute_parallel.sh` uses `resumable_brute.py`, prints a one-line total, and records it in `BRUTE_RESULTS.txt` and `BRUTE_MANIFEST.json`. Each run uses a cache keyed by the witness bytes, verifier source and compilation environment. Its n first-letter jobs leave validated results under `brute_nN.jobs/run-<fingerprint>/`; only results for that matching run can be resumed. A failed worker or malformed/incomplete result makes the runner fail, and counts are aggregated with exact Python integers. Original unbound logs are kept in `legacy_evidence/` and are never reused as fresh cached results. A single file can be checked with `python3 verify.py FILE`, `./verify_dp FILE` or `./verify_brute FILE`. All three take n to be the largest symbol in the file, require each of the symbols 1, …, n to occur, and print n; a reader checking a file of their own should make sure that the printed n is the intended one. `build_note.py` regenerates this note, the OEIS guide and the supporting file from the witness files, the templates and the recorded program outputs (`EXPECTED_OUTPUT.txt`, `BRUTE_RESULTS.txt`), so that no sequence and no table entry is copied by hand. Run `python3 build_note.py` after refreshing the recorded check output. Regeneration checks archived-report consistency and validates hash-bound enumeration records when present.

### 4.5 Independent checks reproduced in this review

The portable programs in `independent_review/` were written separately from the uploaded search and checker implementations. `count_by_endpoint.py` groups distinct permutation prefixes by their earliest embedding endpoints and counts each ordering once; it obtained exactly n! embedded permutations, and zero missing, for every witness. `reverse_greedy.py` computes the earliest starting point among rightmost embeddings over subsets and also found every witness complete. Its implementation agrees with explicit permutation enumeration on 1,227 small test words.

A separate C++ checker tested all 731 possible single-term deletions across the five witnesses. Every deletion destroyed completeness. For each deletion it reconstructed a missing permutation and independently confirmed absence by scanning the shortened word. The certificate files and commands are included in `independent_review/`. These fresh checks establish the theorem without requiring a repeat of the historical trillion-permutation enumeration. They are exact computations, not sampling and not proof-assistant formalization.

## 5. How the witnesses were found

This section is not needed for the Theorem. The sequences came from simulated annealing on the exact number of permutations that are not subsequences. The search started from published constructions (the construction of length (n − 1)² + 3 described by J. E. Schoenfield in the comments of the OEIS entry, or the list T₂ of [Tan22]) and alternated between deleting the term whose removal leaves the fewest permutations missing and repair sweeps at the shorter length. The count is kept exact by dynamic programming over subsets: counting versions of the tables of §4.2, for prefixes and for suffixes, allow the candidate letters at one site to be scored with O(n·2ⁿ) operations when the needed prefix/suffix tables are available. Building those tables or refreshing invalidated rows can cost O(L·2ⁿ); the smaller bound is not an end-to-end claim for arbitrary cache rebuilding. The search programs and the logs of the runs that produced the five witnesses are in `search/`, and `PROVENANCE.txt` lists them. The searches used pseudo-random numbers and floating-point acceptance tests; they are not expected to be reproducible bit for bit on another machine.

## 6. Remarks

* The same search did not improve the published bounds 83 for n = 10 and 225 for n = 16: runs at lengths 82 and 224 ended with a few permutations still missing. This is an observation about one heuristic and is not evidence of optimality.
* Each witness is irreducible in the sense of §4.3.
* Literature and priority. {{PRIORITY_NOTE}}

## 7. Provenance and status

The original search programs, checkers and draft were prepared with Claude (Anthropic) in a contributor-directed session on an Apple M2 laptop, as reported in the supplied package. The current note was revised and additional independent checks were reproduced with Codex (OpenAI) in a Linux cloud workspace. Original reported execution history is kept distinct from the checks reproduced in this review. The Theorem rests only on the five sequences of §3 and the finite checks of §4, which do not depend on how the sequences were produced. No independent human mathematical peer review is claimed. Kumar Aman subsequently reproduced the default `sh run_all.sh` checks on his Mac and submitted a comment and supporting file to OEIS A062714 on 10 November 2026. Following usability feedback from Andrew Howroyd, the supporting file was made directly runnable and the update was marked proposed in revision 139. Howroyd confirmed that the revised file was usable; editorial approval remains pending. Aman also ran the revised standalone Python file on his Mac and reproduced its examples and five successful witness checks. OEIS policy requires a human author who takes responsibility for a contribution and does not permit AI-written comment text; `OEIS_SUBMISSION_GUIDE.txt` gives the contributor facts and conventions.

{{REVIEW_NOTE}}

## References

* [Adl74] L. Adleman, Short permutation strings, Discrete Mathematics 10 (1974), 197–200.
* [CKK72] V. Chvátal, D. A. Klarner and D. E. Knuth, Selected combinatorial research problems, Report STAN-CS-72-292, Computer Science Department, Stanford University, June 1972; Problem 36.
* [GP76] G. Galbiati and F. P. Preparata, On permutation-embedding sequences, SIAM Journal on Applied Mathematics 30 (1976), 421–423.
* [KH75] P. J. Koutas and T. C. Hu, Shortest string containing all permutations, Discrete Mathematics 11 (1975), 125–132.
* [KK76] D. J. Kleitman and D. J. Kwiatkowski, A lower bound on the length of a sequence containing all permutations as subsequences, Journal of Combinatorial Theory, Series A 21 (1976), 129–136. (Cited for context only: a(n) ≥ n² − C_ε·n^(7/4+ε).)
* [Moh80] S. P. Mohanty, Shortest string containing all permutations, Discrete Mathematics 31 (1980), 91–95.
* [New73] M. Newey, Notes on a problem involving permutations as subsequences, Stanford Artificial Intelligence Laboratory Memo AIM-190, Report STAN-CS-73-340, 1973.
* [OEIS] OEIS Foundation Inc., The On-Line Encyclopedia of Integer Sequences, sequence A062714, https://oeis.org/A062714 (consulted {{DATE}}).
* [Rad12] S. Radomirović, A construction of short sequences containing all permutations of a set as subsequences, Electronic Journal of Combinatorics 19(4) (2012), #P31.
* [Tan22] O. Tan, Skip letters for short supersequence of all permutations, Discrete Mathematics 345(12) (2022), article 113070, https://doi.org/10.1016/j.disc.2022.113070. Theorem numbering and formulas here follow the revised preprint arXiv:2201.06306v2, 4 January 2025, https://arxiv.org/abs/2201.06306v2.
* [Tan25] O. Tan, Conjecture on supersequence lower bound related to Connell sequence, arXiv:2501.11386v1, 20 January 2025, https://arxiv.org/abs/2501.11386. Cited as a preprint; no journal version is claimed here.
* [Zal11] E. Zălinescu, Shorter strings containing all k-element permutations, Information Processing Letters 111 (2011), 605–608.
