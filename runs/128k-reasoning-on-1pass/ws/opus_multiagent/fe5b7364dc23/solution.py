import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); k = int(data[1])
    p = 998244353
    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        A = np.array(data[2:2 + n], dtype=np.int64)
        A %= p
        # prefix sums: values < 2^30, n <= 2e5 -> cumsum <= 2^48, safe in int64
        pref = np.cumsum(A, dtype=np.int64) % p
        S = np.empty(n + 1, dtype=np.int64)
        S[0] = 0
        S[1:] = pref
        # power arrays
        P = [None] * (k + 1)
        P[0] = np.ones(n + 1, dtype=np.int64)
        for m in range(1, k + 1):
            P[m] = (P[m - 1] * S) % p
        # exclusive prefix sums: T[m][r-1] = sum_{q=0}^{r-1} P[m][q]
        T = [None] * (k + 1)
        for m in range(k + 1):
            T[m] = np.cumsum(P[m]) % p
        # binomial coefficients
        C = [1] * (k + 1)
        for j in range(1, k + 1):
            C[j] = C[j - 1] * (k - j + 1) // j
        ans = 0
        for j in range(k + 1):
            coeff = C[j] % p
            if (k - j) & 1:
                coeff = (-coeff) % p
            if coeff == 0:
                continue
            prod = (P[j][1:] * T[k - j][:-1]) % p
            s = int(prod.sum() % p)
            ans = (ans + coeff * s) % p
        print(ans % p)
        return

    # pure python fallback
    A = list(map(int, data[2:2 + n]))
    C = [1] * (k + 1)
    for j in range(1, k + 1):
        C[j] = C[j - 1] * (k - j + 1) // j
    coeffs = []
    for j in range(k + 1):
        c = C[j] % p
        if (k - j) & 1:
            c = (-c) % p
        coeffs.append(c)
    T = [0] * (k + 1)
    ans = 0
    s = 0
    # powers of S_0 = 0
    pw = [1] + [0] * k
    for i in range(n):
        for m in range(k + 1):
            T[m] = (T[m] + pw[m]) % p
        s = (s + A[i]) % p
        pw = [1] * (k + 1)
        cur = 1
        for m in range(1, k + 1):
            cur = cur * s % p
            pw[m] = cur
        tot = 0
        for j in range(k + 1):
            tot += coeffs[j] * pw[j] % p * T[k - j]
        ans = (ans + tot) % p
    print(ans % p)

main()