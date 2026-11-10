# Review report — 10 November 2026

**Later status update:** Kumar Aman reproduced the default `sh run_all.sh`
checks on his Mac and submitted a comment and supporting file to OEIS A062714.
The initial submission was proposed in revision 137; a supporting-file revision
following usability feedback was proposed in revision 139. Editorial approval
is pending as of 10 November 2026. The sections below preserve the findings and outstanding decisions
recorded at the original review, before that submission. See RELEASE_NOTES.md
for changes made in preparing this GitHub copy.

## Mathematical outcome

The five supplied witnesses establish a(11)<=101, a(12)<=121, a(13)<=144,
a(14)<=169, and a(15)<=196. They improve the bounds among the cited
constructions by 1,2,1,1,1. The corollary a(n)<=(n-1)^2 for every n>=12
is valid: the witnesses handle 12..15 and Radomirovic's published bound
handles every n>=16. W11 has length 101, so it is outside that corollary.
The finite greedy-embedding proof and subset recurrence are sound.

These are upper bounds. Neither global optimality nor worldwide record
priority is established here. No human peer review has occurred. All
internal reviewers were separate AI agent instances.

## Checks reproduced in this review

- Both textual representations of each sequence match its integer file.
- All final sequences are bijective relabelings of the previously uploaded
  witnesses, with no alteration of their position structure.
- The bundled C and Python recurrence checkers pass every witness.
- A separately written endpoint-counting checker obtains exactly n! distinct
  embedded permutations for every witness: 39,916,800; 479,001,600;
  6,227,020,800; 87,178,291,200; and 1,307,674,368,000.
- A separately written reverse-greedy checker also passes every witness.
  Its result agrees with explicit enumeration on 1,227 small test words.
- All 731 possible single-term deletions fail. For each, a reconstructed
  missing permutation was independently checked by direct scanning.
- A clean-copy default verification run matches EXPECTED_OUTPUT.txt.
- Regenerating the note, guide and supporting data is deterministic.

## Archived enumeration evidence

The upload already contained completed n=15 first-letter job reports,
although NOTE.md still said the computation was unfinished. We validated
all archived n=13,14,15 shards and totals, and the archived whole-run lines
for n=11,12. The counts and alphabet/length labels are internally consistent.
The original runner did not record witness/source hashes; therefore these
logs are historical supporting reports, not independently hash-bound proof
of which exact file bytes were enumerated. They were not rerun here.
The fresh exact verification above is sufficient without those histories.

## Corrections applied

- Scoped priority claims to the constructions and sources actually inspected.
- Corrected the statement about A351468: it includes Newey's general bound.
- Added Tan's 2022 journal reference and identified arXiv v2 (4 January 2025)
  as the source for the theorem numbering/formulas used in the comparison.
- Retained the already-correct Adleman, Galbiati–Preparata and Zalinescu page
  ranges. Tan 2025 remains cited as a preprint.
- Distinguished original Claude-reported history from current Codex review.
- Made the compact checker accept an explicit prescribed alphabet size.
- Labeled archived direct-run reports and their missing historical hash binding.
- Changed the default run to exact verification without factorial enumeration.
- Repaired the resumable brute-force wrapper: failed workers now fail the run;
  caches bind input/source/compiler identity; outputs are validated and
  promoted atomically; totals use exact integers rather than floating-point awk.
- Preserved the original logs and review/priority notes under legacy_evidence/.

## Remaining human decisions

The contributor must fill in their name, understand and take responsibility
for the checker and result, and write their own OEIS comment. The package
provides facts and supporting data, not AI-written comment text to paste.
An external mathematician/editor should assess priority and significance.
Nothing has been submitted or published by this review.

The interrupted session's actual spend was not available to us. This review
makes no claim that the complete original discovery run stayed within $100.
