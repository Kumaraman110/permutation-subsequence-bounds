# GitHub preparation — 10 November 2026

This copy was prepared from the reviewed verification bundle after Kumar Aman
submitted an OEIS A062714 comment and supporting file. The initial submission
was proposed in revision 137 and the revised supporting-file update was proposed
in revision 139. Approval is pending as of 10 November 2026.

The contributor name and submission status were updated in the README, note
template, supporting-file generator and retained submission guide. The original
review report now has a dated status update; its historical findings are retained.
Generated documents were rebuilt from their templates. The five witness files
and original standalone verifier sources retain their reviewed bytes.

After OEIS feedback from Andrew Howroyd, the supporting file was made directly
runnable as Python: witness sequences are literal lists, small positive and
negative examples show how to call `complete(w, n)`, and the same program is
provided as `a062714.py`. The compact Python function now accepts every positive
integer alphabet size without an artificial upper cap, and its exponential
resource requirements are documented. Missing prescribed symbols return False;
invalid alphabet sizes or symbols raise ValueError. The C and older command-line
checkers retain their implementation limits.

Kumar Aman ran the revised standalone file on his Mac and obtained the expected
small examples and five complete witnesses. Text copied by the contributor from
the revised OEIS attachment matches the tested program, allowing for the omitted
final newline. Andrew Howroyd confirmed that he could use the revised file; this
records usability feedback, not mathematical acceptance. The supporting attachment
is https://oeis.org/A062714/a062714_1.txt.

The original search was conducted with Claude. Codex performed the subsequent
revision and additional exact verification. Kumar Aman personally reran the
default verification script on his Mac, which reported all checks passed.
AI-agent reviews are not represented as independent human peer review.

The mathematical claims remain explicit upper bounds and improvements over the
cited constructions. Neither global optimality nor worldwide priority is claimed.
The original session's total cost is unknown.

`SHA256SUMS` identifies the five witness files. `PACKAGE_SHA256SUMS` identifies
the packaged files in this release, excluding the package manifest itself.
`BUILD_REVIEW.json` records the generated-document hashes and packaging checks.
`SOURCE_ARCHIVE_SHA256.txt` identifies the originally uploaded archive, not this
later GitHub preparation.
