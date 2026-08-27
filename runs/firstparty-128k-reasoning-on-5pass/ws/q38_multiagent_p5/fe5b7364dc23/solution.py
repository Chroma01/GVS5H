import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]
    mod = MOD

    # C[m] = binom(K, m) modulo mod
    C = [0] * (K + 1)
    C[0] = 1
    for i in range(1, K + 1):
        for j in range(i, 0, -1):
            C[j] = (C[j] + C[j - 1]) % mod

    # signC[m] = (-1)^m * C(K, m) modulo mod
    signC = [0] * (K + 1)
    for m in range(K + 1):
        if m & 1:
            signC[m] = (mod - C[m]) % mod
        else:
            signC[m] = C[m]

    # Q[m] = sum of P_t^m over already processed prefixes t
    Q = [0] * (K + 1)
    Q[0] = 1  # empty prefix P_0 = 0

    P = 0
    ans = 0
    powP = [1] * (K + 1)
    rng = range(K + 1)

    for a in A:
        P += a
        if P >= mod:
            P -= mod

        for i in range(1, K + 1):
            powP[i] = (powP[i - 1] * P) % mod

        contrib = 0
        for m in rng:
            contrib += (signC[m] * powP[K - m] % mod) * Q[m] % mod
            Q[m] += powP[m]
            if Q[m] >= mod:
                Q[m] -= mod

        ans = (ans + contrib) % mod

    print(ans)

if __name__ == "__main__":
    main()