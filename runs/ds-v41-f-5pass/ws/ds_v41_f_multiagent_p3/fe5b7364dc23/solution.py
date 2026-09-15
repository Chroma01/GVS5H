import sys
from math import comb

MOD = 998244353


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    A = data[2:2 + n]

    # coeff[t] = C(k, t) * (-1)^(k-t) mod MOD
    coeff = [0] * (k + 1)
    for t in range(k + 1):
        c = comb(k, t) % MOD
        if (k - t) & 1:
            c = (-c) % MOD
        coeff[t] = c

    # M[e] = sum of P_i^e over already processed prefix indices i < j
    M = [0] * (k + 1)
    M[0] = 1  # P_0 = 0

    ans = 0
    pref = 0
    powers = [0] * (k + 1)

    for a in A:
        pref = (pref + a) % MOD

        powers[0] = 1
        for t in range(1, k + 1):
            powers[t] = powers[t - 1] * pref % MOD

        total = 0
        for t in range(k + 1):
            total += coeff[t] * powers[t] % MOD * M[k - t] % MOD

        ans = (ans + total) % MOD

        for e in range(k + 1):
            M[e] += powers[e]
            if M[e] >= MOD:
                M[e] -= MOD

    print(ans % MOD)


if __name__ == "__main__":
    main()