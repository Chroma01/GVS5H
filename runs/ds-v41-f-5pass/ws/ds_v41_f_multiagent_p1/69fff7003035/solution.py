import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    L = len(str(N))
    c = [0] * (L + 1)
    V = [0] * (L + 1)
    for e in range(1, L + 1):
        low = 10 ** (e - 1)
        high = min(N, 10 ** e - 1)
        cnt = high - low + 1
        c[e] = cnt
        total = (low + high) * cnt // 2
        V[e] = total % MOD

    a = [0] * (L + 1)
    for e in range(1, L + 1):
        a[e] = (pow(10, e, MOD) - 1) % MOD

    def mul_linear(poly, ae):
        res = [0] * (len(poly) + 1)
        for i, val in enumerate(poly):
            res[i] = (res[i] + val) % MOD
            res[i + 1] = (res[i + 1] + val * ae) % MOD
        return res

    Q = [1]
    for e in range(1, L + 1):
        Q = mul_linear(Q, a[e])

    R = [0] * L
    for e in range(1, L + 1):
        term = c[e] * a[e] % MOD
        poly = [1]
        for f in range(1, L + 1):
            if f != e:
                poly = mul_linear(poly, a[f])
        for j, val in enumerate(poly):
            R[j] = (R[j] + term * val) % MOD

    inv = [0] * (N + 1)
    if N >= 1:
        inv[1] = 1
        for i in range(2, N + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    p = [0] * (N + 1)
    p[0] = 1
    for m in range(N):
        total = 0
        for j in range(L):
            idx = m - j
            if idx >= 0:
                total += R[j] * p[idx]
        for i in range(1, L + 1):
            idx = m - i + 1
            if idx >= 0:
                total -= Q[i] * (m - i + 1) * p[idx]
        total %= MOD
        p[m + 1] = total * inv[m + 1] % MOD

    fact = 1
    for i in range(2, N + 1):
        fact = fact * i % MOD

    ans = 0
    for d in range(1, L + 1):
        ad = a[d]
        s = 0
        prev = 0
        for k in range(N):
            qk = (p[k] - ad * prev) % MOD
            s = (s + qk * inv[k + 1]) % MOD
            prev = qk
        W = fact * s % MOD
        ans = (ans + V[d] * W) % MOD

    print(ans)

if __name__ == "__main__":
    main()