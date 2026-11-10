# Independent review reproduced in this session

These programs were written separately from the uploaded search/checker code.
The counting checker groups distinct permutation prefixes by their earliest
embedding endpoint and counts every permutation exactly once. The reverse
checker uses rightmost embeddings and subset minima. They provide exact
verification, not random sampling. These reviews were performed by AI agents,
not human referees.

Run from the bundle root:

The counting checker requires Python 3.10 or newer because it uses
`int.bit_count()`. This additional requirement does not apply to the default
`sh run_all.sh` checks.

```
python3 independent_review/count_by_endpoint.py witnesses/n11.txt witnesses/n12.txt witnesses/n13.txt witnesses/n14.txt witnesses/n15.txt
python3 independent_review/reverse_greedy.py witnesses/n11.txt witnesses/n12.txt witnesses/n13.txt witnesses/n14.txt witnesses/n15.txt
python3 independent_review/reverse_greedy.py --self-test
```

The C++ checker verifies every single-term deletion, reconstructs a missing
permutation, and confirms its absence with a direct scan. Its inputs_zero_based
files are the canonical witnesses minus one. To rerun it without overwriting
the archived certificates, create an empty scratch directory, copy
inputs_zero_based/ there under the name inputs/, compile check_deletions.cpp
with a C++17 compiler, and pass the scratch directory as its single argument.
All 731 deletion certificates were reproduced and directly checked here.

Archived direct-enumeration logs are kept separately in ../legacy_evidence/.
They were supplied in the upload; their expensive computations were not
repeated in this review. See ../LEGACY_ENUMERATION_REVIEW.json for structural
checks and limitations.
