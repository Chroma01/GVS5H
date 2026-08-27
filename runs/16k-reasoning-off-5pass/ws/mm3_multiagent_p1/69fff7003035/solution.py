import sys

MOD = 998244353
PRIMITIVE_ROOT = 3

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
        wlen = pow(PRIMITIVE_ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:len(a) + len(b) - 1]

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    N = int(input_data)
    
    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    invfact = [1] * (N + 1)
    invfact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        invfact[i-1] = invfact[i] * i % MOD
    
    total_sum = N * (N + 1) // 2 % MOD
    
    # Compute digit groups: c[d] = count, S[d] = sum
    c = [0] * 7
    S = [0] * 7
    for d in range(1, 7):
        lo = 10 ** (d - 1)
        hi = min(N, 10 ** d - 1)
        if lo > hi:
            continue
        cnt = hi - lo + 1
        c[d] = cnt
        s = (lo + hi) * cnt // 2
        S[d] = s % MOD
    
    # Weights w_d = 10^d mod MOD
    w = [0] * 7
    for d in range(1, 7):
        w[d] = pow(10, d, MOD)
    
    # Compute E polynomial: product of (1 + w[d] t)^{c[d]}
    poly = [1]
    for d in range(1, 7):
        if c[d] == 0:
            continue
        # Build polynomial for this d: coefficient k is C(c[d], k) * w[d]^k
        cd = c[d]
        F = [0] * (cd + 1)
        pow_w = 1
        for k in range(cd + 1):
            # C(cd, k) = fact[cd] * invfact[k] * invfact[cd-k]
            F[k] = fact[cd] * invfact[k] % MOD * invfact[cd - k] % MOD * pow_w % MOD
            pow_w = pow_w * w[d] % MOD
        poly = convolution(poly, F)
        if len(poly) > N + 1:
            poly = poly[:N + 1]
    # Ensure length N+1
    if len(poly) < N + 1:
        poly += [0] * (N + 1 - len(poly))
    E = poly
    
    # Compute A[m] for m = 0..N-1
    # Precompute powers of w[d] for each d
    pow_wd = [[0] * (N + 1) for _ in range(7)]
    for d in range(1, 7):
        if c[d] == 0:
            continue
        pow_wd[d][0] = 1
        for m in range(1, N + 1):
            pow_wd[d][m] = pow_wd[d][m-1] * w[d] % MOD
    
    A = [0] * N
    for m in range(N):
        val = 0
        for d in range(1, 7):
            if c[d] == 0:
                continue
            # term = S[d] * w[d] * (w[d])^m = S[d] * w[d]^{m+1}
            term = S[d] * w[d] % MOD * pow_wd[d][m] % MOD
            val = (val + term) % MOD
        A[m] = val
    
    # B[m] = (-1)^m * A[m]
    B = [0] * N
    for m in range(N):
        if m % 2 == 0:
            B[m] = A[m]
        else:
            B[m] = (MOD - A[m]) % MOD
    
    # Convolve B and E to get C, then T[k] = C[k-1] for k>=1
    C = convolution(B, E)
    T = [0] * (N + 1)
    for k in range(1, N + 1):
        if k - 1 < len(C):
            T[k] = C[k-1]
        else:
            T[k] = 0
    
    # Compute S_k = total_sum * E[k] - T[k] for k=0..N-1
    S_arr = [0] * N
    for k in range(N):
        S_arr[k] = (total_sum * E[k] - T[k]) % MOD
    
    # Compute invC(N-1, k) for k=0..N-1
    invC = [0] * N
    inv_fact_N_1 = invfact[N-1] if N >= 1 else 1
    for k in range(N):
        invC[k] = inv_fact_N_1 * fact[k] % MOD * fact[N-1-k] % MOD
    
    # Compute sum_val = Σ S[k] * invC[k]
    sum_val = 0
    for k in range(N):
        sum_val = (sum_val + S_arr[k] * invC[k]) % MOD
    
    ans = fact[N-1] * sum_val % MOD
    print(ans)

if __name__ == "__main__":
    solve()