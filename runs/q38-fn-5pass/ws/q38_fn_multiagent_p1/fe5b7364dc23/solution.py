import sys

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]

    # Binomial coefficients C(K, t)
    comb = [1] * (K + 1)
    for t in range(1, K + 1):
        comb[t] = comb[t - 1] * (K - t + 1) // t

    # Signed coefficient for S_j^t * (-S_i)^(K-t)
    coeff = [
        comb[t] if ((K - t) & 1) == 0 else -comb[t]
        for t in range(K + 1)
    ]

    # power_sums[p] = sum of previous prefix sums^p
    power_sums = [0] * (K + 1)
    power_sums[0] = 1  # prefix sum S_0 = 0, and 0^0 is treated as 1 here

    powers = [1] * (K + 1)
    prefix = 0
    ans = 0

    mod = MOD
    k = K
    k1 = K + 1

    for a in A:
        prefix += a
        if prefix >= mod:
            prefix -= mod

        powers[0] = 1
        total = coeff[0] * power_sums[k]

        prev = 1
        for p in range(1, k1):
            prev = (prev * prefix) % mod
            powers[p] = prev
            total += coeff[p] * prev * power_sums[k - p]

        ans = (ans + total) % mod

        for p in range(k1):
            v = power_sums[p] + powers[p]
            if v >= mod:
                v -= mod
            power_sums[p] = v

    print(ans)

if __name__ == "__main__":
    solve()