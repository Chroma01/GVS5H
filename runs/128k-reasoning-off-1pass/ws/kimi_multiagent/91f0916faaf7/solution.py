import sys
from collections import defaultdict
import numpy as np

MOD = 998244353


def apply_gap(dp, g, p, H, harr):
    # multiply dp[h] by p^(h*g) mod MOD, vectorized via binary lifting on h
    base = pow(p, g, MOD)
    res = np.ones(H + 1, dtype=np.int64)
    cur = base
    b = 1
    while b <= H:
        mask = (harr & b) != 0
        res[mask] = res[mask] * cur % MOD
        cur = cur * cur % MOD
        b <<= 1
    return dp * res % MOD


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    A = list(map(int, data[1:1 + N - 1]))

    M = max(A) if A else 1
    spf = list(range(M + 1))
    i = 2
    while i * i <= M:
        if spf[i] == i:
            for j in range(i * i, M + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    # for each prime p: list of (step index i (1-based), exponent v_p(A_i))
    prime_steps = defaultdict(list)
    for idx, a in enumerate(A, 1):
        x = a
        while x > 1:
            p = spf[x]
            c = 0
            while x % p == 0:
                x //= p
                c += 1
            prime_steps[p].append((idx, c))

    ans = 1
    for p, steps in prime_steps.items():
        H = 0
        for _, c in steps:
            H += c
        # pw[k] = p^k mod MOD
        pw = np.empty(H + 1, dtype=np.int64)
        pw[0] = 1
        for k in range(1, H + 1):
            pw[k] = pw[k - 1] * p % MOD

        dp = np.zeros(H + 1, dtype=np.int64)
        dp[0] = 1
        harr = np.arange(H + 1)
        prev = 0  # last processed step index
        for (i, e) in steps:
            g = i - prev - 1
            if g:
                dp = apply_gap(dp, g, p, H, harr)
            # process step of size e at step index i; positions processed so far = i
            dp2 = np.zeros(H + 1, dtype=np.int64)
            # +e move: height h -> h+e, area += h+e
            dp2[e:] = (dp2[e:] + dp[:H + 1 - e] * pw[e:]) % MOD
            # -e move, h >= e: height h -> h-e, area += h-e
            dp2[:H + 1 - e] = (dp2[:H + 1 - e] + dp[e:] * pw[:H + 1 - e]) % MOD
            # -e move, h < e: min drops by delta=e-h, area += delta*i, new height 0
            add = 0
            for h in range(e):
                dh = dp[h]
                if dh:
                    add = (add + int(dh) * pow(p, (e - h) * i, MOD)) % MOD
            dp2[0] = (dp2[0] + add) % MOD
            dp = dp2
            prev = i
        g = (N - 1) - prev
        if g:
            dp = apply_gap(dp, g, p, H, harr)
        ans = ans * (int(dp.sum()) % MOD) % MOD

    print(ans)


main()