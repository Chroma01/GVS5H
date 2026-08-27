import sys

# Increase recursion depth just in case
sys.setrecursionlimit(3000)

MOD = 998244353
G = 3

def power(a, b, m=MOD):
    res = 1
    a %= m
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2
    return res

def inverse(n, m=MOD):
    return power(n, m - 2, m)

# Precompute roots of unity
MAX_LOG = 19
roots = [0] * MAX_LOG
roots[MAX_LOG - 1] = power(G, (MOD - 1) >> (MAX_LOG - 1))
for i in range(MAX_LOG - 2, -1, -1):
    roots[i] = (roots[i + 1] * roots[i + 1]) % MOD

def ntt(a, invert=False):
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
    log_len = 1
    while length <= n:
        w_len = roots[MAX_LOG - 1 - log_len]
        if invert:
            w_len = inverse(w_len)
        for i in range(0, n, length):
            w = 1
            for j in range(i, i + length // 2):
                u = a[j]
                v = (a[j + length // 2] * w) % MOD
                a[j] = (u + v) % MOD
                a[j + length // 2] = (u - v) % MOD
                w = (w * w_len) % MOD
        length <<= 1
        log_len += 1
    
    if invert:
        n_inv = inverse(n)
        for i in range(n):
            a[i] = (a[i] * n_inv) % MOD
    return a

def multiply(poly1, poly2):
    if not poly1 or not poly2:
        return []
    n = 1
    while n < len(poly1) + len(poly2) - 1:
        n <<= 1
    
    fa = poly1 + [0] * (n - len(poly1))
    fb = poly2 + [0] * (n - len(poly2))
    
    fa = ntt(fa)
    fb = ntt(fb)
    
    for i in range(n):
        fa[i] = (fa[i] * fb[i]) % MOD
        
    fa = ntt(fa, invert=True)
    return fa[:len(poly1) + len(poly2) - 1]

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    if N == 0:
        print(0)
        return

    cnt = [0] * 7
    S = [0] * 7
    for d in range(1, 7):
        L = 10**(d-1)
        R = min(N, 10**d - 1)
        if L > R:
            cnt[d] = 0
            S[d] = 0
        else:
            cnt[d] = R - L + 1
            inv2 = (MOD + 1) // 2
            S[d] = ((L + R) % MOD * cnt[d] % MOD * inv2) % MOD

    P = [1]
    
    max_cnt = max(cnt)
    inv = [1] * (max_cnt + 1)
    for i in range(2, max_cnt + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD
    
    for d in range(1, 7):
        if cnt[d] == 0:
            continue
        
        m = cnt[d]
        base = pow(10, d, MOD)
        F = [0] * (m + 1)
        binom = 1
        base_pow = 1
        for j in range(m + 1):
            F[j] = (binom * base_pow) % MOD
            if j < m:
                binom = (binom * (m - j)) % MOD
                binom = (binom * inv[j + 1]) % MOD
                base_pow = (base_pow * base) % MOD
        
        P = multiply(P, F)
        if len(P) > N:
            P = P[:N]
    
    if len(P) < N:
        P.extend([0] * (N - len(P)))
    
    fact = [1] * N
    for i in range(1, N):
        fact[i] = (fact[i-1] * i) % MOD
    
    pow10_d = [pow(10, d, MOD) for d in range(7)]
    
    total_sum = 0
    for d in range(1, 7):
        if cnt[d] == 0:
            continue
        
        B = [0] * N
        B[0] = P[0]
        for k in range(1, N):
            B[k] = (P[k] - pow10_d[d] * B[k-1]) % MOD
        
        inner_sum = 0
        for k in range(N):
            weight = (fact[k] * fact[N - 1 - k]) % MOD
            inner_sum = (inner_sum + weight * B[k]) % MOD
        
        term = (S[d] * inner_sum) % MOD
        total_sum = (total_sum + term) % MOD
    
    print(total_sum)

solve()