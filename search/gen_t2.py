#!/usr/bin/env python3
"""Generate the best previously published construction for m = n+1 letters, m == 1 (mod 3):
x s1 x s2 ... x sn x  with (s1..sn) = Tan's T2(n) list (equivalent to Radomirovic 2012),
length m^2 - 7m/3 + 19/3.   usage: gen_t2.py m > file     (symbols 0..m-1, x = m-1)"""
import sys

def T2(n):
    assert n >= 6 and n % 3 == 0
    s = {}
    def sl(k, a, b):            # 1-based inclusive slice, negative = from the end
        q = s[k]; L = len(q)
        if a < 0: a = L + 1 + a
        if b < 0: b = L + 1 + b
        return q[a - 1:b]
    s[1] = list(range(1, n + 1))
    s[2] = list(range(1, n))
    s[3] = [s[1][-1]] + sl(2, 1, -2)
    for k in range(4, n - 2):
        if k % 3 == 1:
            if k == 4:
                s[k] = [s[k - 2][-1]] + sl(k - 1, 2, -3) + [n] + [s[k - 1][-2]]
            else:
                s[k] = [s[k - 2][-1]] + [s[k - 1][0]] + sl(k - 1, 3, -3) + [n] + [s[k - 1][-2]]
        elif k % 3 == 2:
            s[k] = [s[k - 2][-1]] + sl(k - 1, 1, -3)
        else:
            s[k] = [s[k - 2][-1]] + [n] + sl(k - 1, 1, -2)
    s[n - 2] = [s[n - 4][-1]] + [s[n - 3][0]] + sl(n - 3, 3, -2) + [n]
    s[n - 1] = [s[n - 3][-1]] + sl(n - 2, 1, -2)
    s[n] = [s[n - 2][-1]] + s[n - 1]
    return [s[k] for k in range(1, n + 1)]

if __name__ == '__main__':
    m = int(sys.argv[1]); n = m - 1
    segs = T2(n)
    seq = [n]
    for g in segs:
        seq += [v - 1 for v in g] + [n]
    print(' '.join(map(str, seq)))
    sys.stderr.write('m=%d length=%d formula=%s\n' % (m, len(seq), (3 * m * m - 7 * m + 19) / 3))
