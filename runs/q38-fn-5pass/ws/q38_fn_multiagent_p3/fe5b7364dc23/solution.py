import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]

    # Binomial coefficients C(K, t), small enough to compute exactly.
    comb = [1] * (K + 1)
    for i in range(1, K + 1):
        comb[i] = comb[i - 1] * (K - i + 1) // i

    # Signed binomial coefficients: (-1)^t * C(K, t).
    signed = [comb[i] if (i & 1) == 0 else -comb[i] for i in range(K + 1)]

    # power_sum[t] = sum of S_i^t over already processed prefixes S_i.
    # Initially only S_0 = 0 exists, so power_sum[0] = 1 and others are 0.
    power_sum = [0] * (K + 1)
    power_sum[0] = 1

    # Reused array for powers of the current prefix sum.
    powers = [0] * (K + 1)
    powers[0] = 1

    s = 0
    ans = 0
    mod = MOD

    rng = range(K + 1)
    rng1 = range(1, K + 1)

    for a in A:
        s += a
        if s >= mod:
            s -= mod

        # powers[e] = s^e mod MOD
        for e in rng1:
            powers[e] = (powers[e - 1] * s) % mod

        # Add contribution of all pairs (i, current_j):
        # (S_j - S_i)^K = sum_t (-1)^t C(K,t) S_j^{K-t} S_i^t
        total = 0
        for t in rng:
            total += signed[t] * powers[K - t] * power_sum[t]

        ans = (ans + total) % mod

        # Include current prefix sum into the maintained power sums.
        for t in rng:
            v = power_sum[t] + powers[t]
            if v >= mod:
                v -= mod
            power_sum[t] = v

    print(ans)

if __name__ == "__main__":
    main()