import sys

def main():
    MOD = 998244353
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]

    # Binomial coefficients C(K, t)
    C = [1] * (K + 1)
    for i in range(1, K + 1):
        C[i] = C[i - 1] * (K - i + 1) // i

    # coeff[t] = C(K, t) * (-1)^(K-t)
    coeff = [0] * (K + 1)
    for t in range(K + 1):
        if (K - t) & 1:
            coeff[t] = -C[t]
        else:
            coeff[t] = C[t]

    # ps[e] = sum of P_i^e over previous prefixes P_i
    ps = [0] * (K + 1)
    ps[0] = 1  # initial prefix P_0 = 0

    # pp[e] = current prefix^e
    pp = [1] * (K + 1)

    prefix = 0
    ans = 0
    mod = MOD
    rng = range(K + 1)
    rng1 = range(1, K + 1)

    for a in data[2:2 + N]:
        prefix += a
        if prefix >= mod:
            prefix -= mod

        val = 1
        s = coeff[0] * ps[K]  # t = 0 term, pp[0] = 1

        for t in rng1:
            val = (val * prefix) % mod
            pp[t] = val
            s += coeff[t] * val * ps[K - t]

        ans = (ans + s) % mod

        for e in rng:
            v = ps[e] + pp[e]
            if v >= mod:
                v -= mod
            ps[e] = v

    print(ans)

if __name__ == "__main__":
    main()