```python
import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    S = data[2]

    size = 1 << N
    pop = [0] * size
    for m in range(1, size):
        pop[m] = pop[m >> 1] + (m & 1)

    # Group the 26 letters by their match-pattern against S.
    patterns = {}
    for c in range(26):
        eq = 0
        for j, ch in enumerate(S):
            if ord(ch) - 97 == c:
                eq |= 1 << j
        patterns[eq] = patterns.get(eq, 0) + 1

    pats = list(patterns.keys())
    mult = [patterns[p] for p in pats]
    P = len(pats)

    # trans[mask][i] = next LCS-row mask after appending a letter with pattern pats[i]
    trans = [[0] * P for _ in range(size)]
    for mask in range(size):
        dp = [0] * (N + 1)
        for j in range(1, N + 1):
            dp[j] = dp[j - 1] + ((mask >> (j - 1)) & 1)

        for pi, eq in enumerate(pats):
            prev = 0
            nmask = 0
            for j in range(1, N + 1):
                v = dp[j]
                if prev > v:
                    v = prev
                cand = dp[j - 1] + ((eq >> (j - 1)) & 1)
                if cand > v:
                    v = cand
                if v > prev:
                    nmask |= 1 << (j - 1)
                prev = v
            trans[mask][pi] = nmask

    counts = [0] * size
    counts[0] = 1

    for _ in range(M):
        new = [0] * size
        for mask, cnt in enumerate(counts):
            if cnt:
                row = trans[mask]
                for pi in range(P):
                    nm = row[pi]
                    new[nm] = (new[nm] + cnt * mult[pi]) % MOD
        counts = new

    ans = [0] * (N + 1)
    for mask, cnt in enumerate(counts):
        ans[pop[mask]] = (ans[pop[mask]] + cnt) % MOD

    sys.stdout.write(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()
```