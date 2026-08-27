import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1])
    S = data[2].strip()

    size = 1 << N
    # Precompute transitions: trans[mask][letter_index] -> new mask
    trans = [[0] * 26 for _ in range(size)]
    for mask in range(size):
        # d[j] = LCS of processed prefix of T with S[:j] = popcount(mask & ((1<<j)-1))
        # d[0] = 0
        d = [0] * (N + 1)
        for j in range(1, N + 1):
            d[j] = d[j - 1] + ((mask >> (j - 1)) & 1)
        for c in range(26):
            nd = [0] * (N + 1)
            for j in range(1, N + 1):
                v = d[j]
                if nd[j - 1] > v:
                    v = nd[j - 1]
                if (ord(S[j - 1]) - 97) == c:
                    t = d[j - 1] + 1
                    if t > v:
                        v = t
                nd[j] = v
            nmask = 0
            for j in range(1, N + 1):
                if nd[j] > nd[j - 1]:
                    nmask |= (1 << (j - 1))
            trans[mask][c] = nmask

    # Count length-M strings ending in each state
    dp = [0] * size
    dp[0] = 1
    for _ in range(M):
        ndp = [0] * size
        for mask in range(size):
            cur = dp[mask]
            if cur:
                row = trans[mask]
                for c in range(26):
                    ndp[row[c]] = (ndp[row[c]] + cur) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for mask in range(size):
        k = bin(mask).count('1')
        ans[k] = (ans[k] + dp[mask]) % MOD

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

solve()