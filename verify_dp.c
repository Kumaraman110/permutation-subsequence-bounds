/* verify_dp.c -- exact completeness check by the subset recurrence of NOTE.md (Lemma 1).
 *
 *   next(p, x) = least position q > p with w_q = x          (L+1 if there is none; next(L+1, x) = L+1)
 *   E(A)       = largest position at which the leftmost embedding of an ordering of the set A ends
 *              = max over x in A of next(E(A minus x), x),    E(empty set) = 0.
 *   The sequence w_1..w_L over {1..n} contains every permutation of {1..n}  iff  E({1..n}) <= L.
 *
 * usage:  verify_dp FILE                  check one sequence (integers 1..n separated by whitespace)
 *         verify_dp --irreducible FILE    also check that deleting any single term destroys completeness
 * exit status: 0 iff the sequence is complete (and irreducible, when requested); 1 otherwise; 2 on bad input.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXL 2000
#define MAXN 20

static int nxt[MAXL + 2][MAXN + 1];
static uint16_t *E;

/* w[1..L] over letters 1..n (a letter may be absent).  Returns E({1..n}); the value L+1 means "not complete". */
static int worst_end(const int *w, int L, int n)
{
    int INF = L + 1;
    uint32_t full = ((uint32_t)1 << n) - 1;
    for (int x = 1; x <= n; x++) nxt[L][x] = INF;
    for (int p = L - 1; p >= 0; p--) {
        memcpy(nxt[p], nxt[p + 1], sizeof nxt[p]);
        nxt[p][w[p + 1]] = p + 1;
    }
    E[0] = 0;
    for (uint32_t A = 1; A <= full; A++) {
        int m = 0;
        for (int x = 1; x <= n; x++)
            if (A >> (x - 1) & 1) {
                int e = E[A ^ ((uint32_t)1 << (x - 1))];
                int q = (e >= INF) ? INF : nxt[e][x];
                if (q > m) m = q;
            }
        E[A] = (uint16_t)m;
    }
    return E[full];
}

int main(int argc, char **argv)
{
    static int w[MAXL + 2], t[MAXL + 2];
    int irreducible = 0, ai = 1, L = 0, n = 0, bad = 0;
    int seen[MAXN + 1] = {0};
    long v;

    if (argc > 1 && strcmp(argv[1], "--irreducible") == 0) { irreducible = 1; ai = 2; }
    if (argc != ai + 1) { fprintf(stderr, "usage: verify_dp [--irreducible] FILE\n"); return 2; }
    const char *path = argv[ai];
    FILE *f = fopen(path, "r");
    if (!f) { perror(path); return 2; }
    while (fscanf(f, "%ld", &v) == 1) {
        if (v < 1 || v > MAXN) { fprintf(stderr, "%s: symbol %ld outside 1..%d\n", path, v, MAXN); return 2; }
        if (L >= MAXL) { fprintf(stderr, "%s: more than %d terms\n", path, MAXL); return 2; }
        w[++L] = (int)v;
        if (v > n) n = (int)v;
        seen[v] = 1;
    }
    if (!feof(f)) { fprintf(stderr, "%s: unexpected character in input\n", path); return 2; }
    fclose(f);
    if (L == 0) { fprintf(stderr, "%s: empty\n", path); return 2; }
    for (int x = 1; x <= n; x++)
        if (!seen[x]) { fprintf(stderr, "%s: symbol %d does not occur (symbols must be exactly 1..n)\n", path, x); return 2; }

    E = malloc(sizeof(uint16_t) << n);
    if (!E) { fprintf(stderr, "out of memory\n"); return 2; }

    int e = worst_end(w, L, n);
    int complete = (e <= L);
    printf("verify_dp: %s: n=%d length=%d E=%d => %s", path, n, L, e, complete ? "COMPLETE" : "NOT COMPLETE");
    if (irreducible && complete) {
        for (int i = 1; i <= L; i++) {
            int k = 0;
            for (int j = 1; j <= L; j++) if (j != i) t[++k] = w[j];
            if (worst_end(t, L - 1, n) <= L - 1) bad++;
        }
        printf("; single-term deletions that stay complete: %d of %d => %s", bad, L, bad ? "REDUCIBLE" : "IRREDUCIBLE");
    }
    printf("\n");
    return (complete && !bad) ? 0 : 1;
}
