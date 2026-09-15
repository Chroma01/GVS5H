import sys

MOD = 998244353

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]

    # coeff[j] = C(K, j) * (-1)^j
    coeff = [0] * (K + 1)
    c = 1
    for j in range(K + 1):
        coeff[j] = c if (j % 2 == 0) else -c
        if j < K:
            c = c * (K - j) // (j + 1)

    size = K + 1
    S = [0] * size
    S[0] = 1  # P_0^0 = 1

    powP = [1] * size
    P = 0
    ans = 0
    mod = MOD

    for a in A:
        P += a
        if P >= mod:
            P -= mod

        for e in range(1, size):
            powP[e] = (powP[e - 1] * P) % mod

        total = 0
        for j in range(size):
            total += coeff[j] * powP[K - j] * S[j]

        ans = (ans + total) % mod

        for j in range(size):
            S[j] += powP[j]
            if S[j] >= mod:
                S[j] -= mod

    print(ans)

if __name__ == "__main__":
    solve()