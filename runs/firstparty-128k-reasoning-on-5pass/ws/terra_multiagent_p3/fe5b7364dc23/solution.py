import sys
from math import comb

MOD = 998244353


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:]

    # moments[t] = sum of S_j^t over all previous prefix sums S_j.
    moments = [0] * (k + 1)
    moments[0] = 1  # Initial prefix sum S_0 = 0.

    # (x - y)^K = sum_t coeff[t] * x^(K-t) * y^t
    coeff = [0] * (k + 1)
    for t in range(k + 1):
        c = comb(k, t)
        if t & 1:
            c = -c
        coeff[t] = c % MOD

    prefix = 0
    answer = 0

    for value in a:
        prefix = (prefix + value) % MOD

        powers = [1] * (k + 1)
        for p in range(1, k + 1):
            powers[p] = powers[p - 1] * prefix % MOD

        contribution = 0
        for t in range(k + 1):
            contribution += coeff[t] * powers[k - t] * moments[t]
        answer = (answer + contribution) % MOD

        for t in range(k + 1):
            moments[t] = (moments[t] + powers[t]) % MOD

    print(answer)


if __name__ == "__main__":
    solve()