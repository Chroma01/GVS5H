import sys
from math import comb

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:]

    coeff = [comb(k, t) % MOD for t in range(k + 1)]
    signed_coeff = [
        coeff[t] if t % 2 == 0 else (MOD - coeff[t])
        for t in range(k + 1)
    ]

    # moments[t] = sum of S_j^t over all previous prefix sums S_j.
    # Initially contains S_0 = 0.
    moments = [0] * (k + 1)
    moments[0] = 1

    prefix = 0
    answer = 0

    for value in a:
        prefix = (prefix + value) % MOD

        powers = [1] * (k + 1)
        for exponent in range(1, k + 1):
            powers[exponent] = powers[exponent - 1] * prefix % MOD

        contribution = 0
        for t in range(k + 1):
            contribution += signed_coeff[t] * powers[k - t] % MOD * moments[t]
        answer = (answer + contribution) % MOD

        for t in range(k + 1):
            moments[t] = (moments[t] + powers[t]) % MOD

    print(answer)

if __name__ == "__main__":
    solve()