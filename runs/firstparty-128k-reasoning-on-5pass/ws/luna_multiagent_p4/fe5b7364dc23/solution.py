import sys
import math

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:2 + n]

    moments = [0] * (k + 1)
    moments[0] = 1  # P_0 = 0, so its zeroth power contributes once

    coefficients = [math.comb(k, t) * (-1 if t & 1 else 1) for t in range(k + 1)]

    prefix = 0
    answer = 0

    for value in a:
        prefix = (prefix + value) % MOD

        powers = [1] * (k + 1)
        for t in range(1, k + 1):
            powers[t] = powers[t - 1] * prefix % MOD

        contribution = 0
        for t in range(k + 1):
            contribution += coefficients[t] * powers[k - t] * moments[t]
        answer = (answer + contribution) % MOD

        for t in range(k + 1):
            moments[t] = (moments[t] + powers[t]) % MOD

    print(answer)

if __name__ == "__main__":
    solve()