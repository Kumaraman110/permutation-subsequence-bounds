#!/usr/bin/env python3
"""prior_bounds.py -- published upper bounds for a(n) (OEIS A062714), each with its stated range of validity.

n is always the alphabet size.  Run without arguments to print every applicable bound for 10 <= n <= 20.
Sources: see the References of NOTE.md.  (Tan's paper writes m for the alphabet size and states the hypotheses
of its Theorem 23 for n = m - 1, namely n >= 4s+1 and n = 3 (mod 2s-1); here they are restated for m.)"""
from fractions import Fraction
from decimal import Decimal, getcontext, ROUND_CEILING


def _ceil(q):
    q = Fraction(q)
    return -((-q.numerator) // q.denominator)


def classical(n):
    """n^2 - 2n + 4 for n >= 3 (Newey 1973; Adleman 1974; Koutas-Hu 1975; Galbiati-Preparata 1976; Mohanty 1980)."""
    return n * n - 2 * n + 4 if n >= 3 else None


def zalinescu(n):
    """n^2 - 2n + 3 for n >= 10 (Zalinescu 2011)."""
    return n * n - 2 * n + 3 if n >= 10 else None


def radomirovic(n):
    """ceil(n^2 - 7n/3 + 19/3) for n >= 7 (Radomirovic 2012)."""
    return _ceil(Fraction(3 * n * n - 7 * n + 19, 3)) if n >= 7 else None


def tan23(n, s):
    """Tan 2022, Theorem 23: for n >= 4s+2 and n = 4 (mod 2s-1),
    n^2 - (5s-3)/(2s-1) n + (2s^2+9s-7)/(2s-1)   (an integer under these conditions)."""
    if s < 1 or n < 4 * s + 2 or (n - 4) % (2 * s - 1) != 0:
        return None
    v = n * n - Fraction((5 * s - 3) * n, 2 * s - 1) + Fraction(2 * s * s + 9 * s - 7, 2 * s - 1)
    assert v.denominator == 1
    return int(v)


def tan26(n, s):
    """Tan 2022, Theorem 26: for n >= 4s+2, ceil(n^2 - (5s-3)/(2s-1) n + (4s^3-10s^2+21s-11)/(2s-1))."""
    if s < 1 or n < 4 * s + 2:
        return None
    return _ceil(n * n - Fraction((5 * s - 3) * n, 2 * s - 1)
                 + Fraction(4 * s ** 3 - 10 * s * s + 21 * s - 11, 2 * s - 1))


def tan28(n):
    """Tan 2022, Theorem 28: for every n, ceil(n^2 - 5n/2 + (3/2)(n/2)^(2/3) + (n/2)^(1/3) + 7).
    Evaluated with 60 significant digits and rounded to 40 decimals before taking the ceiling, so that an
    exactly integral value (e.g. n = 16, where (n/2)^(1/3) = 2) is not pushed up by rounding error."""
    getcontext().prec = 60
    c = (Decimal(n) / 2) ** (Decimal(1) / Decimal(3))
    v = Decimal(n * n) - Decimal(5 * n) / 2 + Decimal(3) / 2 * c * c + c + 7
    v = v.quantize(Decimal(1).scaleb(-40))
    return int(v.to_integral_value(rounding=ROUND_CEILING))


def all_bounds(n):
    out = [("n^2-2n+4", classical(n)), ("Zalinescu", zalinescu(n)), ("Radomirovic", radomirovic(n)),
           ("Tan Thm 28", tan28(n))]
    for s in range(1, n):
        out.append(("Tan Thm 23 s=%d" % s, tan23(n, s)))
        out.append(("Tan Thm 26 s=%d" % s, tan26(n, s)))
    return [(k, v) for k, v in out if v is not None]


def best(n):
    return min(v for _, v in all_bounds(n))


def main():
    print("Published upper bounds for a(n), 10 <= n <= 20 ('-' = the result does not apply to this n)")
    print("%3s %9s %10s %12s %-24s %-16s %11s %9s" % ("n", "n^2-2n+4", "Zalinescu", "Radomirovic",
          "Tan Thm 23 (s>=2)", "Tan Thm 26 (min)", "Tan Thm 28", "smallest"))
    for n in range(10, 21):
        t23 = ["%d (s=%d)" % (tan23(n, s), s) for s in range(2, n) if tan23(n, s) is not None]
        t26 = [(tan26(n, s), s) for s in range(1, n) if tan26(n, s) is not None]
        v26, s26 = min(t26)
        print("%3d %9d %10d %12d %-24s %-16s %11d %9d" % (n, classical(n), zalinescu(n), radomirovic(n),
              ", ".join(t23) if t23 else "-", "%d (s=%d)" % (v26, s26), tan28(n), best(n)))


if __name__ == "__main__":
    main()
