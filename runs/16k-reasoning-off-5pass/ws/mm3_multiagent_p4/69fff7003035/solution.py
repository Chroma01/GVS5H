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

def multiply(a, b):
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

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    
    # Compute counts and sums for each digit length
    c = [0] * 7  # index 0 unused
    S = [0] * 7
    for d in range(1, 7):
        start = 10**(d-1)
        end = min(N, 10**d - 1)
        if start > end:
            continue
        count = end - start + 1
        c[d] = count
        # Sum of arithmetic series: count * (start + end) // 2
        S[d] = count * (start + end) // 2 % MOD
    
    # Compute H(z) = product over d of (1 + w_d * z)^{c_d}
    H = [1]
    for d in range(1, 7):
        if c[d] == 0:
            continue
        w = pow(10, d, MOD)
        # Compute polynomial (1 + w*z)^{c_d}
        poly = [0] * (c[d] + 1)
        for j in range(c[d] + 1):
            binom = fact[c[d]] * inv_fact[j] % MOD * inv_fact[c[d]-j] % MOD
            poly[j] = binom * pow(w, j, MOD) % MOD
        H = multiply(H, poly)
        if len(H) > N + 1:
            H = H[:N + 1]
    
    # Compute R(z) = sum_d S[d] * w_d * z/(1 + w_d * z) truncated to degree N-1
    R = [0] * N
    for d in range(1, 7):
        if c[d] == 0:
            continue
        w = pow(10, d, MOD)
        coeff = S[d] * w % MOD
        cur = 1
        for k in range(1, N):
            R[k] = (R[k] + coeff * cur) % MOD
            cur = cur * (-w) % MOD
    
    # Compute Q(z) = H(z) * R(z) truncated to degree N-1
    Q = multiply(H, R)
    if len(Q) > N:
        Q = Q[:N]
    else:
        Q = Q + [0] * (N - len(Q))
    
    # Extract A_k and B_k
    A = H[:N] if len(H) >= N else H + [0] * (N - len(H))
    B = Q
    
    total_sum = N * (N + 1) // 2 % MOD
    
    ans = 0
    for k in range(N):
        term = fact[N - k - 1] * fact[k] % MOD
        val = (total_sum * A[k] - B[k]) % MOD
        ans = (ans + term * val) % MOD
    
    print(ans)

if __name__ == "__main__":
    main()