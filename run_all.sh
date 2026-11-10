#!/bin/sh
# run_all.sh -- repeat the checks reported in NOTE.md, section 4.
# The output is deterministic:      sh run_all.sh | diff - EXPECTED_OUTPUT.txt
# BRUTE_MAX (default 0) opts into direct enumeration up to the given n.
# The default uses exact dynamic programming and never starts factorial-time work.
# Set BRUTE_MAX explicitly to run slow checks; for n >= 13 use run_brute_parallel.sh.
# Needs: POSIX sh, a C compiler as `cc` (or set CC), python3, and shasum or sha256sum.
set -e
cd "$(dirname "$0")"
BRUTE_MAX=${BRUTE_MAX:-0}
case "$BRUTE_MAX" in
  ''|*[!0-9]*) echo "BRUTE_MAX must be an integer from 0 through 20" >&2; exit 2 ;;
esac
[ "$BRUTE_MAX" -le 20 ] || { echo "BRUTE_MAX must be at most 20" >&2; exit 2; }
${CC:-cc} -O2 -o verify_dp verify_dp.c
${CC:-cc} -O2 -o verify_brute verify_brute.c

# Preserve the prescribed alphabet size if a file loses its largest letter.
python3 - <<'PY'
from verify import read_word
for n in (11, 12, 13, 14, 15):
    path = "witnesses/n%d.txt" % n
    _, actual = read_word(path)
    if actual != n:
        raise SystemExit("%s: expected alphabet 1..%d, found 1..%d" % (path, n, actual))
PY

echo "== checksums of the witness files"
if command -v shasum >/dev/null 2>&1; then shasum -a 256 witnesses/n*.txt; else sha256sum witnesses/n*.txt; fi | diff - SHA256SUMS
echo "witness files match SHA256SUMS"

echo "== published bounds"
python3 prior_bounds.py

for n in 11 12 13 14 15; do
  f=witnesses/n$n.txt
  echo "== n = $n"
  python3 verify.py "$f"
  ./verify_dp --irreducible "$f"
  if [ "$n" -le "$BRUTE_MAX" ]; then
    ./verify_brute "$f"
  else
    echo "verify_brute: not run here for n=$n (BRUTE_MAX=$BRUTE_MAX); see run_brute_parallel.sh and BRUTE_RESULTS.txt"
  fi
done

echo "== negative controls (last term removed)"
python3 verify.py --drop-last witnesses/n11.txt witnesses/n12.txt witnesses/n13.txt witnesses/n14.txt witnesses/n15.txt

echo "== all checks passed"
