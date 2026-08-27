import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    mod = 998244353
    g = 3
    
    def ntt(a, invert):
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        length = 2
        while length <= n:
            wlen = pow(g, (mod - 1) // length, mod)
            if invert:
                wlen = pow(wlen, mod - 2, mod)
            for i in range(0, n, length):
                w = 1
                for j in range(i, i + length // 2):
                    u = a[j]
                    v = a[j + length // 2] * w % mod
                    a[j] = (u + v) % mod
                    a[j + length // 2] = (u - v) % mod
                    w = w * wlen % mod
            length <<= 1
        if invert:
            inv_n = pow(n, mod - 2, mod)
            for i in range(n):
                a[i] = a[i] * inv_n % mod
    
    def multiply(a, b, max_deg):
        n = 1
        while n < len(a) + len(b) - 1:
            n <<= 1
        fa = a + [0] * (n - len(a))
        fb = b + [0] * (n - len(b))
        ntt(fa, False)
        ntt(fb, False)
        for i in range(n):
            fa[i] = fa[i] * fb[i] % mod
        ntt(fa, True)
        res = fa[:max_deg + 1]
        return res
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    # Compute digit lengths
    cnt = [0] * 7  # index 1..6
    sum_v = [0] * 7
    for x in range(1, N + 1):
        d = 1
        if x >= 10: d = 2
        if x >= 100: d = 3
        if x >= 1000: d = 4
        if x >= 10000: d = 5
        if x >= 100000: d = 6
        cnt[d] += 1
        sum_v[d] = (sum_v[d] + x) % mod
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % mod
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], mod - 2, mod)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % mod
    
    # Precompute powers of 10
    pow10 = [0] * 7
    pow10[0] = 1
    for d in range(1, 7):
        pow10[d] = pow10[d - 1] * 10 % mod
    
    # Build initial polynomials for each digit length
    polys = []
    for d in range(1, 7):
        if cnt[d] == 0:
            continue
        m = cnt[d]
        c = pow10[d]
        poly = [0] * (m + 1)
        for k in range(m + 1):
            # C(m, k) * c^k
            binom = fact[m] * inv_fact[k] % mod * inv_fact[m - k] % mod
            poly[k] = binom * pow(c, k, mod) % mod
        polys.append(poly)
    
    # Multiply all polynomials to get P(x)
    if not polys:
        P = [1]
    else:
        P = polys[0]
        for i in range(1, len(polys)):
            P = multiply(P, polys[i], N)
    
    # Ensure P has length N+1
    if len(P) < N + 1:
        P.extend([0] * (N + 1 - len(P)))
    
    # Precompute weights w_k = k! * (N-1-k)!
    w = [0] * N
    for k in range(N):
        w[k] = fact[k] * fact[N - 1 - k] % mod
    
    # Compute answer
    ans = 0
    for d in range(1, 7):
        if cnt[d] == 0:
            continue
        c = pow10[d]
        # Compute Q_d via recurrence
        Q = [0] * N
        Q[0] = P[0]
        for k in range(1, N):
            Q[k] = (P[k] - c * Q[k - 1]) % mod
        # Compute S_d
        S = 0
        for k in range(N):
            S = (S + w[k] * Q[k]) % mod
        ans = (ans + sum_v[d] * S) % mod
    
    print(ans % mod)

if __name__ == "__main__":
    solve()