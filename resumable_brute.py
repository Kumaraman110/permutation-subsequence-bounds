#!/usr/bin/env python3
"""Optional direct enumeration: python3 resumable_brute.py N [JOBS].

Large N is expensive. The default run_all.sh does not invoke this program.
Requires Python 3.8+, POSIX file locks, and GCC/Clang (CC, default cc;
CFLAGS, default -O2). Resume caches are bound to input/source/compiler
hashes. Legacy unbound logs are never adopted. All totals use integers.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

VERSION = 1
PATTERN = re.compile(
    r"verify_brute: witness\.txt: n=(\d+) length=(\d+) first=(\d+) "
    r"examined=(\d+) expected=(\d+) missing=(\d+) => (ALL PRESENT|NOT COMPLETE)"
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def write_atomic(path, raw):
    fd, name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as output:
            output.write(raw)
            output.flush()
            os.fsync(output.fileno())
        os.replace(name, str(path))
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write_json(path, data):
    write_atomic(path, (json.dumps(data, indent=2, sort_keys=True) + "\n").encode())


def locked(path):
    handle = open(str(path), "a+")
    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        handle.close()
        raise ValueError("another process holds %s" % path)
    return handle


def parse_word(raw, n):
    tokens = raw.split()
    if not tokens or not all(re.fullmatch(br"[0-9]+", token) for token in tokens):
        raise ValueError("witness must contain decimal integers separated by whitespace")
    word = [int(token) for token in tokens]
    if len(word) > 2000 or set(word) != set(range(1, n + 1)):
        raise ValueError("witness must have at most 2000 terms and alphabet exactly 1..%d" % n)
    return word


def validate_job(path, base, n, length, first):
    raw = path.read_bytes()
    lines = [line for line in raw.decode("utf-8").splitlines() if line.strip()]
    match = PATTERN.fullmatch(lines[0]) if len(lines) == 1 else None
    if match is None:
        raise ValueError("invalid or incomplete prefix output: %s" % path)
    values = tuple(map(int, match.groups()[:6]))
    required = math.factorial(n - 1)
    if values != (n, length, first, required, required, 0) or match.group(7) != "ALL PRESENT":
        raise ValueError("prefix output does not certify this job: %s" % path)
    return {
        "first": first, "examined": values[3], "expected": values[4],
        "missing": values[5], "verdict": match.group(7),
        "output_file": str(path.relative_to(base)), "output_sha256": sha(raw),
    }


def run_job(directory, base, n, length, first):
    final = directory / ("%d.txt" % first)
    if final.exists():
        return validate_job(final, base, n, length, first)
    fd, temporary = tempfile.mkstemp(prefix="job-%d-" % first, suffix=".tmp", dir=str(directory))
    stderr_path = directory / ("%d.stderr.txt" % first)
    try:
        with os.fdopen(fd, "wb") as output, open(str(stderr_path), "wb") as errors:
            result = subprocess.run(["./verify_brute", "witness.txt", str(first)],
                                    cwd=str(directory), stdout=output, stderr=errors)
        if result.returncode != 0:
            failed = directory / ("%d.failed.txt" % first)
            os.replace(temporary, str(failed))
            raise ValueError("prefix %d exited %d; see %s and %s" % (
                first, result.returncode, failed, stderr_path))
        validate_job(Path(temporary), base, n, length, first)
        os.replace(temporary, str(final))
        if stderr_path.stat().st_size == 0:
            stderr_path.unlink()
        return validate_job(final, base, n, length, first)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def publish(base, summary):
    # Serialize index updates when different runs finish concurrently.
    with locked(base / ".brute_results.lock"):
        path = base / "BRUTE_MANIFEST.json"
        manifest = json.loads(path.read_text()) if path.exists() else {"format_version": VERSION, "records": {}}
        if manifest.get("format_version") != VERSION or not isinstance(manifest.get("records"), dict):
            raise ValueError("unsupported BRUTE_MANIFEST.json format")
        manifest["records"][str(summary["n"])] = summary
        write_json(path, manifest)
        result_path = base / "BRUTE_RESULTS.txt"
        lines = result_path.read_text().splitlines() if result_path.exists() else []
        lines = [line for line in lines if not line.startswith("n=%d " % summary["n"])]
        line = ("n={n} length={length} jobs={jobs} permutations examined={permutations_examined} "
                "expected={permutations_expected} missing={missing} => {verdict}").format(**summary)
        lines.append(line)
        lines.sort(key=lambda item: int(re.match(r"n=(\d+)", item).group(1)))
        write_atomic(result_path, ("\n".join(lines) + "\n").encode())
    print(line, flush=True)
    print("Hash-bound execution record: BRUTE_MANIFEST.json", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int)
    parser.add_argument("jobs", type=int, nargs="?", default=4)
    args = parser.parse_args()
    if not 1 <= args.n <= 20 or args.jobs < 1:
        parser.error("N must be from 1 through 20 and JOBS must be positive")
    base = Path(__file__).resolve().parent
    witness, source = base / "witnesses" / ("n%d.txt" % args.n), base / "verify_brute.c"
    witness_raw, source_raw = witness.read_bytes(), source.read_bytes()
    word = parse_word(witness_raw, args.n)
    compiler = shlex.split(os.environ.get("CC", "cc"))
    if not compiler or shutil.which(compiler[0]) is None:
        raise ValueError("C compiler not found")
    compiler[0] = shutil.which(compiler[0])
    flags = shlex.split(os.environ.get("CFLAGS", "-O2"))
    version = subprocess.run(compiler + ["--version"], cwd=str(base), stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, check=True).stdout.decode("utf-8", "replace")
    identity = {
        "format_version": VERSION, "n": args.n, "length": len(word),
        "witness_sha256": sha(witness_raw), "verifier_sha256": sha(source_raw),
        "compiler_command": compiler, "compiler_flags": flags, "compiler_version": version,
        "platform": platform.system(), "machine": platform.machine(),
    }
    fingerprint = sha(json.dumps(identity, sort_keys=True, separators=(",", ":")).encode())
    directory = base / ("brute_n%d.jobs" % args.n) / ("run-" + fingerprint)
    directory.mkdir(parents=True, exist_ok=True)
    with locked(directory / "run.lock"):
        metadata_path = directory / "metadata.json"
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text())
            if any(metadata.get(key) != value for key, value in identity.items()):
                raise ValueError("cache metadata mismatch")
        else:
            metadata = dict(identity, fingerprint_sha256=fingerprint, created_utc=now(),
                            execution="direct enumeration partitioned by first letter",
                            compile_command=compiler + flags + ["-o", "verify_brute", "verify_brute.c"])
            write_json(metadata_path, metadata)
        for name, raw in (("witness.txt", witness_raw), ("verify_brute.c", source_raw)):
            destination = directory / name
            if destination.exists() and destination.read_bytes() != raw:
                raise ValueError("cache snapshot mismatch: " + str(destination))
            if not destination.exists():
                write_atomic(destination, raw)
        executable = directory / "verify_brute"
        if executable.exists():
            if sha(executable.read_bytes()) != metadata.get("binary_sha256"):
                raise ValueError("cached executable hash mismatch")
        else:
            subprocess.run(compiler + flags + ["-o", "verify_brute.tmp", "verify_brute.c"],
                           cwd=str(directory), check=True)
            os.replace(str(directory / "verify_brute.tmp"), str(executable))
            metadata["binary_sha256"] = sha(executable.read_bytes())
            write_json(metadata_path, metadata)
        with ThreadPoolExecutor(max_workers=min(args.jobs, args.n)) as pool:
            futures = [pool.submit(run_job, directory, base, args.n, len(word), first)
                       for first in range(1, args.n + 1)]
            for future in as_completed(futures):
                future.result()
        records = [validate_job(directory / ("%d.txt" % first), base, args.n, len(word), first)
                   for first in range(1, args.n + 1)]
        if witness.read_bytes() != witness_raw or source.read_bytes() != source_raw:
            raise ValueError("input/source changed during the run; no summary published")
        examined, missing = sum(r["examined"] for r in records), sum(r["missing"] for r in records)
        required = math.factorial(args.n)
        if examined != required or missing:
            raise ValueError("prefix jobs do not cover exactly N! permutations")
        summary = {
            "format_version": VERSION, "n": args.n, "length": len(word), "jobs": args.n,
            "permutations_examined": examined, "permutations_expected": required,
            "missing": missing, "verdict": "ALL PRESENT",
            "witness_sha256": identity["witness_sha256"], "verifier_sha256": identity["verifier_sha256"],
            "fingerprint_sha256": fingerprint, "cache_directory": str(directory.relative_to(base)),
            "metadata_file": str(metadata_path.relative_to(base)), "per_first_letter": records,
            "completed_utc": now(),
        }
        write_json(directory / "summary.json", summary)
        publish(base, summary)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("resumable_brute.py: " + str(error), file=sys.stderr)
        sys.exit(1)
