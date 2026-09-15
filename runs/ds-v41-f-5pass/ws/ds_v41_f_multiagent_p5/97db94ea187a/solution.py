import sys
import numpy as np

def interpolate(vals, D, P):
    arr = [v % P for v in vals]
    c = []
    for k in range(D + 1):
        c.append(arr[0])
        for i in range(D - k):
            arr[i] = (arr[i + 1] - arr[i]) % P
    fact = [1] * (D + 1)
    for i in range(1, D + 1):
        fact[i] = fact[i - 1] * i % P
    inv_fact = [1] * (D + 1)
    inv_fact[D] = pow(fact[D], P - 2, P)
    for i in range(D, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % P
    poly = [0] * (D + 1)
    fall = [0] * (D + 1)
    fall[0] = 1
    for k in range(D + 1):
        dk = c[k] * inv_fact[k] % P
        if dk:
            for i in range(k + 1):
                fi = fall[i]
                if fi:
                    poly[i] = (poly[i] + dk * fi) % P
        if k < D:
            new_fall = [0] * (D + 1)
            for i in range(k + 1):
                fi = fall[i]
                if fi:
                    new_fall[i + 1] = (new_fall[i + 1] + fi) % P
                    new_fall[i] = (new_fall[i] - k * fi) % P
            fall = new_fall
    return poly

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    P = int(data[1])
    H = N // 2
    D = N * (N - 1) // 2
    L = D + 1
    base = np.arange(1, L + 1, dtype=np.int64)
    maxv = max(D, N)
    pow_any = np.zeros((maxv + 1, L), dtype=np.int64)
    pow_any[0] = 1
    for v in range(1, maxv + 1):
        pow_any[v] = pow_any[v - 1] * base % P
    T = np.zeros((N + 1, N + 1, L), dtype=np.int64)
    for a in range(1, N + 1):
        qa = (pow_any[a] - 1) % P
        cur = np.ones(L, dtype=np.int64)
        for b in range(0, N + 1):
            T[a, b] = cur * pow_any[b * (b - 1) // 2] % P
            cur = cur * qa % P
    C = [[0] * (N + 1) for _ in range(N + 1)]
    for n in range(N + 1):
        C[n][0] = C[n][n] = 1
        for k in range(1, n):
            C[n][k] = (C[n - 1][k - 1] + C[n - 1][k]) % P
    dp = np.zeros((N + 1, H + 1, N + 1, 2, L), dtype=np.int64)
    dp[1, 0, 1, 0, :] = 1
    tmp = np.empty(L, dtype=np.int64)
    for used in range(1, N):
        dp[used] %= P
        rem = N - used
        odd_min = max(0, used - H)
        odd_max = min(H, used)
        for odd in range(odd_min, odd_max + 1):
            for last in range(1, used + 1):
                for par in (0, 1):
                    vec = dp[used, odd, last, par]
                    if not vec.any():
                        continue
                    if par == 0:
                        b_max = H - odd
                        if b_max > rem:
                            b_max = rem
                    else:
                        b_max = H - (used - odd)
                        if b_max > rem:
                            b_max = rem
                    if b_max < 1:
                        continue
                    for b in range(1, b_max + 1):
                        new_used = used + b
                        if par == 0:
                            new_odd = odd + b
                        else:
                            new_odd = odd
                        new_par = 1 - par
                        binom = C[rem][b]
                        np.multiply(vec, T[last, b], out=tmp)
                        tmp %= P
                        np.multiply(tmp, binom, out=tmp)
                        tmp %= P
                        dp[new_used, new_odd, b, new_par] += tmp
    dp[N] %= P
    A = np.zeros(L, dtype=np.int64)
    for last in range(1, N + 1):
        for par in (0, 1):
            A += dp[N, H, last, par]
    A %= P
    vals = [int(x) for x in A]
    poly = interpolate(vals, D, P)
    out = [str(poly[M] % P) for M in range(N - 1, D + 1)]
    sys.stdout.write(" ".join(out) + "\n")

if __name__ == "__main__":
    solve()