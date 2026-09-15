import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    K = int(data[1])
    A = list(map(int, data[2:2 + N]))

    # Binomial coefficients up to K
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for n in range(K + 1):
        C[n][0] = 1
        C[n][n] = 1
        for r in range(1, n):
            C[n][r] = (C[n - 1][r - 1] + C[n - 1][r]) % MOD

    # sign[t] = (-1)^(K-t) mod MOD
    sign = [1] * (K + 1)
    for t in range(K + 1):
        if (K - t) & 1:
            sign[t] = MOD - 1

    # S[p] = sum_{i=0}^{j-1} P[i]^p, where P is prefix sum
    S = [0] * (K + 1)
    S[0] = 1  # P[0]^0

    P = 0
    ans = 0
    pws = [0] * (K + 1)

    for a in A:
        P += a
        if P >= MOD:
            P -= MOD

        pws[0] = 1
        for p in range(1, K + 1):
            pws[p] = pws[p - 1] * P % MOD

        term = 0
        for t in range(K + 1):
            add = C[K][t] * sign[t] % MOD
            add = add * pws[t] % MOD
            add = add * S[K - t] % MOD
            term += add
        ans = (ans + term) % MOD

        for p in range(K + 1):
            S[p] += pws[p]
            if S[p] >= MOD:
                S[p] -= MOD

    print(ans % MOD)

if __name__ == "__main__":
    main()