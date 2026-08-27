import sys

def solve():
    import numpy as np
    MOD = 998244353
    data = sys.stdin.read().split()
    N = int(data[0])
    A = list(map(int, data[1:1 + N - 1]))

    # sieve smallest prime factor up to 1000
    LIM = 1000
    spf = list(range(LIM + 1))
    for i in range(2, int(LIM ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, LIM + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # group (edge_index, exponent) per prime; edge index i is 1-based
    prime_edges = {}
    for idx, a in enumerate(A, start=1):
        x = a
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            prime_edges.setdefault(p, []).append((idx, e))

    ans = 1
    for p, edges in prime_edges.items():
        H = 0
        maxe = 0
        for _, e in edges:
            H += e
            if e > maxe:
                maxe = e
        M = max(H, (N - 1) * maxe)
        pw = [1] * (M + 1)
        for k in range(1, M + 1):
            pw[k] = pw[k - 1] * p % MOD
        pw_arr = np.array(pw, dtype=np.int64)

        dp = np.zeros(H + 1, dtype=np.int64)
        dp[0] = 1
        for i, e in edges:
            new = np.zeros(H + 1, dtype=np.int64)
            n = H + 1 - e
            # up step: h -> h+e, weight p^(h+e)
            new[e:] = (dp[:n] * pw_arr[e:H + 1]) % MOD
            # down step (staying >= 0): h -> h-e, weight p^(h-e)
            new[:n] += (dp[e:] * pw_arr[:n]) % MOD
            new %= MOD
            # down step crossing below the running minimum:
            # min drops by d = e-h, all i previous positions rise by d
            s = 0
            base = i * e
            for h in range(e):
                if dp[h]:
                    s = (s + dp[h] * pw[base - i * h]) % MOD
            new[0] = (new[0] + s) % MOD
            dp = new
        ans = ans * int(dp.sum() % MOD) % MOD

    print(ans)

solve()