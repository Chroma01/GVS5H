import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]

    coeff = [0] * (K + 1)
    c = 1
    for j in range(K + 1):
        if j:
            c = c * (K - j + 1) // j
        if j & 1:
            coeff[j] = (-c) % MOD
        else:
            coeff[j] = c % MOD

    B = [0] * (K + 1)
    B[0] = 1

    p = [1] * (K + 1)

    S = 0
    ans = 0
    mod = MOD
    k = K

    for x in A:
        S += x
        if S >= mod:
            S -= mod

        for t in range(1, k + 1):
            p[t] = (p[t - 1] * S) % mod

        total = 0
        for j in range(k + 1):
            total = (total + coeff[j] * p[k - j] % mod * B[j]) % mod

        ans += total
        if ans >= mod:
            ans -= mod

        for j in range(k + 1):
            v = B[j] + p[j]
            if v >= mod:
                v -= mod
            B[j] = v

    print(ans)

if __name__ == "__main__":
    main()