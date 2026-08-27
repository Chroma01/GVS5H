import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1])
    S = data[2].strip()

    # State: mask of N bits. bit i (0-indexed) = d[i+1] - d[i], where
    # d[i] = LCS(processed prefix of T, S[:i]). d[0] = 0, d is nondecreasing
    # with increments 0/1, so mask fully determines the DP row.

    # Precompute transition for each (mask, letter): returns new mask.
    # trans[mask] = dict mapping new_mask -> number of letters (out of 26)
    # that produce new_mask.
    size = 1 << N
    trans = [None] * size
    for mask in range(size):
        # reconstruct d values
        d = [0] * (N + 1)
        for i in range(N):
            d[i + 1] = d[i] + ((mask >> i) & 1)
        groups = {}
        for c in range(26):
            ch = chr(ord('a') + c)
            e = [0] * (N + 1)
            for i in range(1, N + 1):
                v = e[i - 1]
                if d[i] > v:
                    v = d[i]
                if S[i - 1] == ch:
                    w = d[i - 1] + 1
                    if w > v:
                        v = w
                e[i] = v
            nm = 0
            for i in range(N):
                if e[i + 1] > e[i]:
                    nm |= (1 << i)
            groups[nm] = groups.get(nm, 0) + 1
        trans[mask] = list(groups.items())

    dp = {0: 1}
    for _ in range(M):
        ndp = {}
        for mask, cnt in dp.items():
            for nm, mult in trans[mask]:
                ndp[nm] = (ndp.get(nm, 0) + cnt * mult) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for mask, cnt in dp.items():
        k = bin(mask).count('1')
        ans[k] = (ans[k] + cnt) % MOD

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

main()