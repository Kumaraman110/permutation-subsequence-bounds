# Upper bounds for permutation-complete sequences

Contributor: **Kumar Aman**.

This repository supplies five explicit sequences containing every permutation
of their respective alphabets as a subsequence, together with exact checkers
and reproduction instructions. Subsequence symbols need not be adjacent.

| Alphabet size n | Witness length, hence upper bound for a(n) | Smallest bound among the cited constructions |
|---|---|---|
| 11 | 101 | 102 |
| 12 | 121 | 123 |
| 13 | 144 | 145 |
| 14 | 169 | 170 |
| 15 | 196 | 197 |

These are upper bounds, not proved optimal lengths. The note compares the
constructions actually inspected; worldwide record priority is not established.

## Submission status

On **10 November 2026**, Kumar Aman submitted a comment and supporting file
to [OEIS A062714](https://oeis.org/A062714). The draft was marked **proposed**
in revision **137**. The revised supporting file was added in revision **138**
and resubmitted for review in revision **139**. Andrew Howroyd confirmed that
the revised file is easier to use. Editorial approval is pending as of that date.
The existing list of exact OEIS terms was not extended.

The [revised OEIS supporting file](https://oeis.org/A062714/a062714_1.txt)
contains the runnable Python witness lists and checker. It is the same program
provided here as `a062714.py` and `a062714.txt`.

Start with [NOTE.md](NOTE.md) for the mathematics and
[REVIEW_REPORT.md](REVIEW_REPORT.md) for the original review findings.
[RELEASE_NOTES.md](RELEASE_NOTES.md) records the later submission and packaging
updates. The note remains a research draft for independent human review.

## Provenance

Claude (Anthropic) prepared the original search, code and draft in a session
directed by Kumar Aman. Codex (OpenAI) revised the note, repaired the optional
enumeration runner, and performed additional exact checks with separately
written verifiers. The internal reviewers were AI agents, not human referees.
Kumar Aman subsequently reproduced the default `sh run_all.sh` checks on his
Mac and submitted the OEIS contribution. Verification establishes completeness
of the witnesses; it does not establish optimality or discovery priority.
The original session's total token expenditure was not available.

## Fast reproduction

For the Python-only checker, run:

```
python3 a062714.py
```

This prints a small complete example, two incomplete examples, and the result
for each of the five witnesses. The file contains ordinary Python lists and
can also be imported: `from a062714 import complete, W11`, followed by
`complete(W11, 11)`. The OEIS supporting file `a062714.txt` contains the same
program and can be run with `python3 a062714.txt`.

The pure Python function has no fixed upper limit on the positive alphabet
size n. Its worst-case time is O(nL + n*2^n) and memory is O(nL + 2^n), for
word length L. The bundled C and older command-line checkers retain their
documented implementation limits.

For the full default checks:

Requirements: POSIX shell, C compiler (GCC or Clang), Python 3.8+, and
shasum or sha256sum. The default does not run factorial-time enumeration.
The optional independent counting checker requires Python 3.10+;
see [independent_review/README.md](independent_review/README.md).

```
sh run_all.sh | diff - EXPECTED_OUTPUT.txt
python3 build_note.py
```

`run_all.sh` checks the witness hashes, prescribed alphabets, cited bound
formulas, C/Python exact subset verifiers, all 731 one-term deletions, and
negative controls. A clean-copy run reproduces EXPECTED_OUTPUT.txt.

## Files

- NOTE.template.md and build_note.py generate the research note.
- witnesses/ contains the five one-based integer sequences.
- SHA256SUMS authenticates their exact bytes.
- a062714.py and a062714.txt are identical runnable programs containing the
  five literal witness lists, an exact checker and small usage examples.
  They are supporting data and code; the contributor remains responsible
  for understanding and verifying submitted material.
- OEIS_SUBMISSION_GUIDE.txt contains facts and conventions for the human
  contributor; it is not text to paste into OEIS comments.
- independent_review/ contains independently written checkers, fresh
  results, and 731 explicitly checked missing-permutation certificates.
- legacy_evidence/ preserves supplied historical enumeration reports.
- LEGACY_ENUMERATION_REVIEW.json records their structural validation and
  the limitation that the original runner did not record input/source hashes.
- run_brute_parallel.sh and resumable_brute.py provide optional, expensive,
  resumable direct enumeration with input/source/compiler-bound caches,
  validated workers, atomic results, and integer-exact aggregation.

Do not restart the large enumerations merely to reproduce the exact upper
bounds: the proved finite subset verification is sufficient. If optional
new enumerations are run, BRUTE_MANIFEST.json records their provenance.
The supplied archived n=15 jobs already report full coverage; this review
has not rerun that historical computation.

Generated binaries are omitted from the distribution and rebuilt by the
scripts. Original uploaded bytes are identified by SOURCE_ARCHIVE_SHA256.txt.
No network service is used by the reproduction scripts.
