import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    S = data[2].strip()

    size = 1 << N
    pop = [0] * size
    for mask in range(1, size):
        pop[mask] = pop[mask >> 1] + (mask & 1)

    # Aggregate the 26 possible next letters by their equality bitmask against S.
    pattern_count = {}
    for c in range(26):
        eq = 0
        for j, ch in enumerate(S):
            if ord(ch) - 97 == c:
                eq |= 1 << j
        pattern_count[eq] = pattern_count.get(eq, 0) + 1

    patterns = list(pattern_count.keys())
    mult = [pattern_count[p] for p in patterns]
    P = len(patterns)

    # trans[mask][i] = next increment-mask after appending a letter whose
    # equality pattern is patterns[i].
    trans = [[0] * P for _ in range(size)]
    for mask in range(size):
        dp = [0] * (N + 1)
        for j in range(1, N + 1):
            dp[j] = dp[j - 1] + ((mask >> (j - 1)) & 1)

        for pi, eq in enumerate(patterns):
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
        nxt = [0] * size
        for mask, cnt in enumerate(counts):
            if cnt:
                row = trans[mask]
                for pi in range(P):
                    nm = row[pi]
                    nxt[nm] = (nxt[nm] + cnt * mult[pi]) % MOD
        counts = nxt

    ans = [0] * (N + 1)
    for mask, cnt in enumerate(counts):
        ans[pop[mask]] = (ans[pop[mask]] + cnt) % MOD

    sys.stdout.write(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()