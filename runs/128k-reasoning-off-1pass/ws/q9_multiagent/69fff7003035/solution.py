import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

MOD = 998244353
G = 3

def power(a, b):
    res = 1
    a %= MOD
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        b //= 2
    return res

def inv(n):
    return power(n, MOD - 2)

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
        wlen = power(G, (MOD - 1) // length)
        if invert:
            wlen = inv(wlen)
        for i in range(0, n, length):
            w = 1
            for k in range(length // 2):
                u = a[i + k]
                v = (a[i + k + length // 2] * w) % MOD
                a[i + k] = (u + v) % MOD
                a[i + k + length // 2] = (u - v) % MOD
                w = (w * wlen) % MOD
        length <<= 1
    
    if invert:
        n_inv = inv(n)
        for i in range(n):
            a[i] = (a[i] * n_inv) % MOD

def multiply(a, b):
    if not a or not b:
        return []
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = (fa[i] * fb[i]) % MOD
    ntt(fa, True)
    return fa[:len(a) + len(b) - 1]

def poly_pow(base, exp):
    res = [1]
    while exp > 0:
        if exp % 2 == 1:
            res = multiply(res, base)
        base = multiply(base, base)
        exp //= 2
    return res

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])

    counts = {}
    sum_vals_by_len = {}
    total_sum = 0
    
    for x in range(1, N + 1):
        s = str(x)
        l = len(s)
        counts[l] = counts.get(l, 0) + 1
        total_sum = (total_sum + x) % MOD
        if l not in sum_vals_by_len:
            sum_vals_by_len[l] = 0
        sum_vals_by_len[l] = (sum_vals_by_len[l] + x) % MOD

    fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = (fact[i-1] * i) % MOD

    polys = []
    for l in sorted(counts.keys()):
        count = counts[l]
        base_poly = [1, (power(10, l)) % MOD]
        term = poly_pow(base_poly, count)
        polys.append(term)
    
    Q = [1]
    for p in polys:
        Q = multiply(Q, p)
    
    A = Q
    
    distinct_lengths = sorted(sum_vals_by_len.keys())
    B = [0] * N
    
    for l in distinct_lengths:
        count_l = counts[l]
        sum_l = sum_vals_by_len[l]
        val_l = power(10, l)
        
        # We need to convolve A with the sequence g[t] = (-1)^t * (10^l)^t
        # The sequence length needed is N (since we access up to index N-1 in B)
        g_len = N
        g = [0] * g_len
        term = 1
        neg_val = (MOD - val_l) % MOD
        for t in range(g_len):
            g[t] = term
            term = (term * neg_val) % MOD
            
        conv = multiply(g, A)
        
        factor = (val_l * sum_l) % MOD
        for k in range(1, N):
            if k-1 < len(conv):
                term_val = conv[k-1]
                B[k] = (B[k] + factor * term_val) % MOD

    ans = 0
    total_sum_val = total_sum
    
    for k in range(N):
        term_A = (total_sum_val * A[k]) % MOD
        term_B = B[k]
        diff = (term_A - term_B + MOD) % MOD
        
        count_perms = (fact[N - k] * fact[k]) % MOD
        
        contribution = (count_perms * diff) % MOD
        ans = (ans + contribution) % MOD
        
    print(ans)

if __name__ == '__main__':
    main()