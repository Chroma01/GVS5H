import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n - 1]))

    # smallest prime factor sieve up to 1000
    LIM = 1000
    spf = list(range(LIM + 1))
    spf[0] = 0
    spf[1] = 1
    i = 2
    while i * i <= LIM:
        if spf[i] == i:
            for j in range(i * i, LIM + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    # per prime: list of (edge_index (1-based), exponent)
    prime_edges = defaultdict(list)
    for idx, a in enumerate(A, start=1):
        x = a
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0:
                x //= p
                e += 1
            prime_edges[p].append((idx, e))

    ans = 1
    for p, edges in prime_edges.items():
        total_e = sum(e for _, e in edges)
        pw = [1] * (total_e + 1)
        for k in range(1, total_e + 1):
            pw[k] = pw[k - 1] * p % MOD

        # dp[h] = aggregate weight p^{sum of v_j over positions accounted so far}
        # h = u_i - min(u) >= 0 at the current frontier
        dp = [1]  # h = 0, weight 1
        maxh = 0
        prev = 0  # index of previous edge containing p (0 = none yet)
        for idx, e in edges:
            gap = idx - prev - 1  # positions prev+2 .. idx, all at current height h
            pi = pow(p, idx, MOD)  # p^idx, used for min-drop shift factors
            new_maxh = maxh + e
            ndp = [0] * (new_maxh + 1)
            for h in range(maxh + 1):
                val = dp[h]
                if not val:
                    continue
                # account for gap positions at height h
                if gap and h:
                    val = val * pow(pw[h], gap, MOD) % MOD
                # delta = +e : min unchanged, new position has v = h+e
                nh = h + e
                w = val * pw[nh] % MOD
                ndp[nh] = (ndp[nh] + w) % MOD
                # delta = -e
                nh = h - e
                if nh >= 0:
                    # min unchanged, new position has v = nh
                    w = val * pw[nh] % MOD
                    ndp[nh] = (ndp[nh] + w) % MOD
                else:
                    # min drops by s = -nh: all idx positions so far gain s,
                    # new position has v = 0
                    s = -nh
                    w = val * pow(pi, s, MOD) % MOD
                    ndp[0] = (ndp[0] + w) % MOD
            dp = ndp
            maxh = new_maxh
            prev = idx

        # tail positions last+2 .. N, all at final height h
        tail = n - prev - 1
        if tail > 0:
            F = 0
            for h in range(maxh + 1):
                val = dp[h]
                if val:
                    if h:
                        val = val * pow(pw[h], tail, MOD) % MOD
                    F = (F + val) % MOD
        else:
            F = sum(dp) % MOD

        ans = ans * F % MOD

    print(ans)

main()