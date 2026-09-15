import sys

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]

    mod = MOD
    K1 = K + 1
    rng = range(K1)
    rng1 = range(1, K1)

    # Binomial coefficients C(K, j), exact integers (K <= 10).
    comb = [1] * K1
    for j in range(1, K1):
        comb[j] = comb[j - 1] * (K - j + 1) // j

    # Signed binomial coefficients: C(K, j) * (-1)^j modulo mod.
    coeff = [0] * K1
    for j in rng:
        if j & 1:
            coeff[j] = (-comb[j]) % mod
        else:
            coeff[j] = comb[j] % mod

    # rev[j] = K - j, used for powers of the current prefix.
    rev = [K - j for j in rng]

    # power_sum[j] = sum of P_t^j over all already processed prefixes t.
    # Initially only P_0 = 0 is present. P_0^0 is treated as 1.
    power_sum = [0] * K1
    power_sum[0] = 1

    # Reusable array for powers of the current prefix.
    powers = [1] * K1

    prefix = 0
    ans = 0

    for a in A:
        prefix += a
        if prefix >= mod:
            prefix -= mod

        # powers[j] = prefix^j mod mod
        for j in rng1:
            powers[j] = (powers[j - 1] * prefix) % mod

        # Contribution of all subarrays ending at this position:
        # sum_{t < r} (prefix - P_t)^K
        total = 0
        for j in rng:
            total += coeff[j] * power_sum[j] * powers[rev[j]]

        ans += total % mod
        if ans >= mod:
            ans -= mod

        # Add current prefix to the maintained power sums.
        for j in rng:
            x = power_sum[j] + powers[j]
            if x >= mod:
                x -= mod
            power_sum[j] = x

    print(ans)

if __name__ == "__main__":
    solve()