import sys

MOD = 998244353

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]

    # Binomial coefficients C(n, k) for 0 <= n, k <= K.
    comb = [[0] * (K + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        comb[i][0] = comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = (comb[i - 1][j - 1] + comb[i - 1][j]) % MOD

    # coeff[q] = C(K, q) * (-1)^q modulo MOD.
    coeff = [0] * (K + 1)
    for q in range(K + 1):
        c = comb[K][q]
        if q & 1:
            c = (-c) % MOD
        coeff[q] = c

    # S[q] = sum of previous prefix sums raised to q.
    # Include the empty prefix P_0 = 0, so S[0] = 1 and S[q] = 0 for q > 0.
    S = [0] * (K + 1)
    S[0] = 1

    pwr = [1] * (K + 1)
    prefix = 0
    ans = 0

    for x in A:
        prefix += x
        if prefix >= MOD:
            prefix -= MOD

        # Powers of the current prefix: pwr[q] = prefix^q.
        pwr[0] = 1
        for q in range(1, K + 1):
            pwr[q] = (pwr[q - 1] * prefix) % MOD

        # Add sum over previous prefixes i:
        # (prefix - P_i)^K = sum_q C(K,q) * prefix^(K-q) * (-P_i)^q.
        total = 0
        for q in range(K + 1):
            total += (coeff[q] * pwr[K - q] % MOD) * S[q]

        ans = (ans + total) % MOD

        # Add current prefix to the moment sums.
        for q in range(K + 1):
            v = S[q] + pwr[q]
            if v >= MOD:
                v -= MOD
            S[q] = v

    print(ans)

if __name__ == "__main__":
    main()