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
            for j in range(i, i + length // 2):
                u = a[j]
                v = a[j + length // 2] * w % MOD
                a[j] = (u + v) % MOD
                a[j + length // 2] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def multiply(a, b, trunc=None):
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
    if trunc is not None:
        return fa[:trunc]
    return fa[:len(a) + len(b) - 1]

def main():
    input_data = sys.stdin.read().split()
    N = int(input_data[0])
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD-2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    
    total_sum = N * (N + 1) // 2 % MOD
    
    # Compute groups by digit length
    groups = []
    l = 1
    while 10**(l-1) <= N:
        start = 10**(l-1)
        end = min(N, 10**l - 1)
        c = end - start + 1
        if c > 0:
            sum_l = (start + end) * c // 2 % MOD
            pow10_l = pow(10, l, MOD)
            groups.append((c, sum_l, pow10_l))
        l += 1
    
    # Build A(t) = prod (1 + t*10^l)^{c_l}
    poly = [1]
    for c, sum_l, pow10_l in groups:
        # Build polynomial for this group: sum_{j=0}^{min(c,N)} C(c,j) * (10^l)^j t^j
        max_j = min(c, N)
        P = [0] * (max_j + 1)
        for j in range(max_j + 1):
            # C(c, j) = fact[c] * inv_fact[j] * inv_fact[c-j]
            P[j] = fact[c] * inv_fact[j] % MOD * inv_fact[c - j] % MOD * pow(pow10_l, j, MOD) % MOD
        poly = multiply(poly, P, trunc=N+1)
    
    A = poly  # length N+1
    
    # Build C(t) = sum_{m=0}^{N-1} c_m t^m where c_m = (-1)^m * sum_l sum_l * 10^l * (10^l)^m
    C = [0] * N
    for c_l, sum_l, pow10_l in groups:
        if c_l == 0:
            continue
        base = sum_l * pow10_l % MOD
        cur = base
        for m in range(N):
            C[m] = (C[m] + cur) % MOD
            cur = cur * pow10_l % MOD
    for m in range(N):
        if m % 2 == 1:
            C[m] = (-C[m]) % MOD
    
    # Multiply A and C to get D(t) = A(t) * C(t)
    D = multiply(A, C, trunc=N)
    
    # Compute the answer
    ans = fact[N-1] * total_sum % MOD
    for k in range(1, N):
        term = fact[k-1] * fact[k] % MOD
        val = total_sum * A[k] % MOD
        val = (val - D[k-1]) % MOD
        ans = (ans + term * val) % MOD
    
    print(ans % MOD)

if __name__ == "__main__":
    main()