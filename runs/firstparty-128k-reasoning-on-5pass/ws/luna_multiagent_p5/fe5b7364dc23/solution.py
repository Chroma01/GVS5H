import sys
from math import comb

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]
    a = data[2:2 + n]

    binom = [comb(k, j) % MOD for j in range(k + 1)]

    # Prefix P_0 = 0 is already among the previous prefixes.
    power_sums = [0] * (k + 1)
    power_sums[0] = 1

    prefix = 0
    answer = 0

    for value in a:
        prefix = (prefix + value) % MOD

        powers = [1] * (k + 1)
        for degree in range(1, k + 1):
            powers[degree] = powers[degree - 1] * prefix % MOD

        contribution = 0
        for j in range(k + 1):
            term = binom[j] * powers[k - j] % MOD
            term = term * power_sums[j] % MOD
            if j & 1:
                contribution -= term
            else:
                contribution += term

        answer = (answer + contribution) % MOD

        for degree in range(k + 1):
            power_sums[degree] = (power_sums[degree] + powers[degree]) % MOD

    print(answer % MOD)

if __name__ == "__main__":
    solve()