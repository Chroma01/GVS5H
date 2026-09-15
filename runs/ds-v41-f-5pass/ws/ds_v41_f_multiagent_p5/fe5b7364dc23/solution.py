import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0]); K = int(data[1])
    A = data[2:2 + n]
    MOD = 998244353

    # Binomial coefficients C[K][t]
    C = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        C[i][0] = 1
        for t in range(1, i + 1):
            C[i][t] = (C[i - 1][t - 1] + C[i - 1][t]) % MOD

    Ck = C[K]
    sign = [1 if t % 2 == 0 else MOD - 1 for t in range(K + 1)]

    # M[t] = sum of P_i^t over processed prefix indices i (< current j)
    M = [0] * (K + 1)
    M[0] = 1  # P_0 = 0, so P_0^0 = 1

    ans = 0
    P = 0
    pw = [1] * (K + 1)

    for a in A:
        P = (P + int(a)) % MOD
        pw[0] = 1
        for t in range(1, K + 1):
            pw[t] = pw[t - 1] * P % MOD

        term = 0
        for t in range(K + 1):
            term += Ck[t] * sign[t] % MOD * M[t] % MOD * pw[K - t] % MOD
        ans = (ans + term) % MOD

        for t in range(K + 1):
            M[t] = (M[t] + pw[t]) % MOD

    sys.stdout.write(str(ans % MOD) + "\n")

main()