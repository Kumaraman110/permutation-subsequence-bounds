/* verify_brute.c -- definition-level check; no dynamic programming.
 *
 * Enumerates the permutations of {1..n} by depth-first search over their prefixes.  Each further letter is
 * matched at the leftmost position after the previous match; a sequence of distinct letters is a subsequence of
 * w exactly when this leftmost matching does not run off the end.  Every one of the n! permutations is accounted
 * for: it is either reached as a leaf (present) or lies below a prefix that failed (missing).
 *
 * usage:  verify_brute FILE        all n! permutations
 *         verify_brute FILE k      only the (n-1)! permutations whose first letter is k
 *                                  (splits the work into n independent jobs; see run_brute_parallel.sh)
 * exit status: 0 iff no examined permutation is missing; 1 otherwise; 2 on bad input.
 * Needs a compiler providing __builtin_ctz and __builtin_popcount (GCC, Clang).
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAXL 2000
#define MAXN 20

static int n, L;
static int w[MAXL + 2];
static int nxt[MAXL + 2][MAXN];           /* nxt[p][x-1] = least q > p with w[q] == x, or L+1 if none */
static uint64_t examined, missing, fact[MAXN + 1];
static int cur[MAXN], example[MAXN], example_len;

/* pos = position of the last matched letter (0 at the start); unused = set of letters not yet used (bit x-1) */
static void dfs(int pos, uint32_t unused, int depth)
{
    if (unused == 0) { examined++; return; }
    for (uint32_t m = unused; m; m &= m - 1) {
        int x = __builtin_ctz(m);                       /* the letter x+1 */
        int q = nxt[pos][x];
        cur[depth] = x + 1;
        if (q > L) {                                    /* prefix not a subsequence: all completions are missing */
            uint64_t c = fact[__builtin_popcount(unused) - 1];
            if (!example_len) {
                example_len = depth + 1;
                for (int i = 0; i <= depth; i++) example[i] = cur[i];
            }
            examined += c;
            missing += c;
        } else {
            dfs(q, unused & ~((uint32_t)1 << x), depth + 1);
        }
    }
}

int main(int argc, char **argv)
{
    int seen[MAXN + 1] = {0};
    long v;
    char first[16] = "all";
    uint64_t expected;

    if (argc != 2 && argc != 3) { fprintf(stderr, "usage: verify_brute FILE [first-letter]\n"); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 2; }
    while (fscanf(f, "%ld", &v) == 1) {
        if (v < 1 || v > MAXN) { fprintf(stderr, "%s: symbol %ld outside 1..%d\n", argv[1], v, MAXN); return 2; }
        if (L >= MAXL) { fprintf(stderr, "%s: more than %d terms\n", argv[1], MAXL); return 2; }
        w[++L] = (int)v;
        if (v > n) n = (int)v;
        seen[v] = 1;
    }
    if (!feof(f)) { fprintf(stderr, "%s: unexpected character in input\n", argv[1]); return 2; }
    fclose(f);
    if (L == 0) { fprintf(stderr, "%s: empty\n", argv[1]); return 2; }
    for (int x = 1; x <= n; x++)
        if (!seen[x]) { fprintf(stderr, "%s: symbol %d does not occur (symbols must be exactly 1..n)\n", argv[1], x); return 2; }

    for (int x = 0; x < n; x++) nxt[L][x] = L + 1;
    for (int p = L - 1; p >= 0; p--) {
        for (int x = 0; x < n; x++) nxt[p][x] = nxt[p + 1][x];
        nxt[p][w[p + 1] - 1] = p + 1;
    }
    fact[0] = 1;
    for (int i = 1; i <= MAXN; i++) fact[i] = fact[i - 1] * (uint64_t)i;

    uint32_t full = ((uint32_t)1 << n) - 1;
    if (argc == 3) {
        int k = atoi(argv[2]);
        if (k < 1 || k > n) { fprintf(stderr, "first letter must be in 1..%d\n", n); return 2; }
        snprintf(first, sizeof first, "%d", k);
        expected = fact[n - 1];
        cur[0] = k;
        dfs(nxt[0][k - 1], full & ~((uint32_t)1 << (k - 1)), 1);   /* letter k occurs, so nxt[0][k-1] <= L */
    } else {
        expected = fact[n];
        dfs(0, full, 0);
    }
    int ok = (missing == 0 && examined == expected);
    printf("verify_brute: %s: n=%d length=%d first=%s examined=%llu expected=%llu missing=%llu => %s\n",
           argv[1], n, L, first, (unsigned long long)examined, (unsigned long long)expected,
           (unsigned long long)missing, ok ? "ALL PRESENT" : "NOT COMPLETE");
    if (example_len) {
        printf("verify_brute: no permutation beginning");
        for (int i = 0; i < example_len; i++) printf(" %d", example[i]);
        printf(" is a subsequence\n");
    }
    return ok ? 0 : 1;
}
