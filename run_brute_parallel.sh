#!/bin/sh
# Optional, potentially expensive direct enumeration: sh run_brute_parallel.sh N [JOBS].
# Resumes only caches bound to witness bytes, verifier source, compiler and flags.
# Legacy unbound prefix outputs are never reused. Requires Python 3 and a C compiler.
set -eu
cd "$(dirname "$0")"
exec python3 resumable_brute.py "$@"
