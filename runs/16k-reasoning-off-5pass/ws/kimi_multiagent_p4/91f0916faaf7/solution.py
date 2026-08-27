import sys


def solve_numpy(N, A, prime_edges, MOD):
    import numpy as np

    ans = 1
    for p, edges in prime_edges.items():
        B = 0
        ed = {}
        for t, e in edges:
            ed[t] = e
            B += e
        # pw[k] = p^k mod MOD, k = 0..B
        pw = [1] * (B + 1)
        for k in range(1, B + 1):
            pw[k] = pw[k - 1] * p % MOD
        pwa = np.array(pw, dtype=np.int64)

        dp = np.zeros(B + 1, dtype=np.int64)
        dp[0] = 1
        for t in range(1, N):
            e = ed.get(t)
            if e is None:
                # stay: d -> d, factor p^d
                dp = dp * pwa % MOD
            else:
                ndp = np.zeros(B + 1, dtype=np.int64)
                # up step: d -> d+e, factor p^(d+e)
                ndp[e:] = dp[:B + 1 - e] * pwa[e:] % MOD
                # down step with d >= e: d -> d-e, factor p^(d-e)
                ndp[:B + 1 - e] = (ndp[:B + 1 - e] + dp[e:] * pwa[:B + 1 - e]) % MOD
                # down step with d < e: new minimum, d -> 0, factor p^((e-d)*t)
                base = int(ndp[0])
                for d in range(e):
                    v = int(dp[d])
                    if v:
                        base = (base + v * pow(p, (e - d) * t, MOD)) % MOD
                ndp[0] = base
                dp = ndp
        ans = ans * (int(dp.sum()) % MOD) % MOD
    return ans


def solve_pure(N, A, prime_edges, MOD):
    ans = 1
    for p, edges in prime_edges.items():
        B = 0
        ed = {}
        for t, e in edges:
            ed[t] = e
            B += e
        pw = [1] * (B + 1)
        for k in range(1, B + 1):
            pw[k] = pw[k - 1] * p % MOD

        dp = [0] * (B + 1)
        dp[0] = 1
        for t in range(1, N):
            e = ed.get(t)
            if e is None:
                dp = [d * w % MOD for d, w in zip(dp, pw)]
            else:
                ndp = [0] * (B + 1)
                # up: d -> d+e
                src = dp[:B + 1 - e]
                wsrc = pw[e:]
                for i in range(B + 1 - e):
                    v = src[i]
                    if v:
                        ndp[i + e] = (ndp[i + e] + v * wsrc[i]) % MOD
                # down d >= e: d -> d-e
                src = dp[e:]
                wsrc = pw[:B + 1 - e]
                for i in range(B + 1 - e):
                    v = src[i]
                    if v:
                        ndp[i] = (ndp[i] + v * wsrc[i]) % MOD
                # down d < e: -> 0
                base = ndp[0]
                for d in range(e):
                    v = dp[d]
                    if v:
                        base = (base + v * pow(p, (e - d) * t, MOD)) % MOD
                ndp[0] = base
                dp = ndp
        ans = ans * (sum(dp) % MOD) % MOD
    return ans


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    A = [int(x) for x in data[1:1 + N - 1]]
    MOD = 998244353

    # smallest prime factor sieve up to 1000
    MAXA = 1000
    spf = list(range(MAXA + 1))
    i = 2
    while i * i <= MAXA:
        if spf[i] == i:
            for j in range(i * i, MAXA + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    prime_edges = {}
    for t in range(1, N):
        x = A[t - 1]
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            prime_edges.setdefault(p, []).append((t, e))

    try:
        import numpy  # noqa: F401
        ans = solve_numpy(N, A, prime_edges, MOD)
    except ImportError:
        ans = solve_pure(N, A, prime_edges, MOD)
    print(ans)


main()