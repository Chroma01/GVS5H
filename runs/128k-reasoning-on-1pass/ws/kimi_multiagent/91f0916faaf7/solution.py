import sys
import numpy as np

MOD = 998244353


def arr_pow(base, k):
    # elementwise base**k % MOD, safe in int64 (values < MOD, products < MOD^2 < 2^63)
    res = np.ones(base.shape[0], dtype=np.int64)
    b = base.copy()
    while k:
        if k & 1:
            res = res * b % MOD
        b = b * b % MOD
        k >>= 1
    return res


def walk_sum(powp, steps, cap):
    # Sum of p**(h_1+...+h_N) over all walks with 0 <= h_i <= cap and
    # |h_{i+1} - h_i| = steps[i] (steps[i] = 0 means h_{i+1} = h_i).
    dp = powp[:cap + 1].copy()  # dp[h] = p**h: choose starting height h_1 = h
    zeros = 0
    for a in steps:
        if a == 0:
            zeros += 1
            continue
        if zeros:
            dp = dp * arr_pow(powp[:cap + 1], zeros) % MOD
            zeros = 0
        ndp = np.zeros(cap + 1, dtype=np.int64)
        ndp[:cap + 1 - a] += dp[a:] * powp[:cap + 1 - a]  # step down: h -> h - a
        ndp[a:] += dp[:cap + 1 - a] * powp[a:]            # step up:   h -> h + a
        dp = ndp % MOD
    if zeros:
        dp = dp * arr_pow(powp[:cap + 1], zeros) % MOD
    return int(dp.sum() % MOD)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    A = data[1:N]

    maxA = max(A)
    spf = list(range(maxA + 1))
    for i in range(2, int(maxA ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, maxA + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # group prime occurrences: p -> [(edge_index, exponent)]
    occ = {}
    for idx, x in enumerate(A):
        y = x
        while y > 1:
            p = spf[y]
            e = 0
            while y % p == 0:
                y //= p
                e += 1
            occ.setdefault(p, []).append((idx, e))

    ans = 1
    for p, lst in occ.items():
        steps = [0] * (N - 1)
        H = 0
        for idx, e in lst:
            steps[idx] = e
            H += e

        powp = np.empty(H + 1, dtype=np.int64)
        powp[0] = 1
        pm = p % MOD
        for h in range(1, H + 1):
            powp[h] = powp[h - 1] * pm % MOD

        gH = walk_sum(powp, steps, H)      # walks with 0 <= h_i <= H
        gH1 = walk_sum(powp, steps, H - 1)  # walks with 0 <= h_i <= H-1
        # F_p = sum_{min h = 0} p^area = G_H - p^N * G_{H-1}
        f = (gH - pow(p, N, MOD) * gH1) % MOD
        ans = ans * f % MOD

    print(ans)


if __name__ == "__main__":
    main()