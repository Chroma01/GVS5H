import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, K = data[0], data[1]
    A = data[2:2 + N]

    comb = [1] * (K + 1)
    for i in range(1, K + 1):
        comb[i] = comb[i - 1] * (K - i + 1) // i

    coeff = [0] * (K + 1)
    for t in range(K + 1):
        c = comb[t]
        if (K - t) & 1:
            c = -c
        coeff[t] = c

    moments = [0] * (K + 1)
    moments[0] = 1
    powers = [1] * (K + 1)

    prefix = 0
    ans = 0
    mod = MOD
    rng_pow = range(1, K + 1)
    rng_all = range(K + 1)

    for a in A:
        prefix += a
        if prefix >= mod:
            prefix -= mod

        s = coeff[0] * moments[K]
        for t in rng_pow:
            powers[t] = (powers[t - 1] * prefix) % mod
            s += coeff[t] * powers[t] * moments[K - t]

        ans = (ans + s) % mod

        for m in rng_all:
            v = moments[m] + powers[m]
            if v >= mod:
                v -= mod
            moments[m] = v

    print(ans)

if __name__ == "__main__":
    main()