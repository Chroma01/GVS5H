import sys

# Increase recursion depth just in case
sys.setrecursionlimit(3000)

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

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])

    if N == 1:
        print(1)
        return

    # Precompute powers of 10
    # Numbers 1 to N have lengths from 1 to 6 (since N <= 2*10^5)
    pow10 = [1] * 7
    for k in range(1, 7):
        pow10[k] = (pow10[k-1] * 10) % MOD

    # Calculate lengths and digit sums for each number 1..N
    # We group numbers by their weight w = 10^length
    # distinct_w[w] will store the sum of digits of all numbers with weight w
    # counts[w] will store the number of times weight w appears
    
    counts = {}
    digit_sums_by_w = {}
    
    for i in range(1, N + 1):
        temp = i
        s = 0
        l = 0
        while temp > 0:
            s += temp % 10
            temp //= 10
            l += 1
        
        w = pow10[l]
        digit_sums_by_w[w] = digit_sums_by_w.get(w, 0) + s
        counts[w] = counts.get(w, 0) + 1

    # Precompute factorials for combinations
    fact = [1] * (N + 1)
    inv_fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
    inv_fact[N] = inv(fact[N])
    for i in range(N-1, 1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i+1)) % MOD

    # Helper for NTT
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
                    a[i + k + length // 2] = (u - v + MOD) % MOD
                    w = (w * wlen) % MOD
            length <<= 1
        
        if invert:
            n_inv = inv(n)
            for i in range(n):
                a[i] = (a[i] * n_inv) % MOD

    def multiply(a, b):
        n = len(a)
        m = len(b)
        size = 1
        while size < n + m:
            size <<= 1
        fa = a + [0] * (size - n)
        fb = b + [0] * (size - m)
        ntt(fa, False)
        ntt(fb, False)
        for i in range(size):
            fa[i] = (fa[i] * fb[i]) % MOD
        ntt(fa, True)
        return fa[:n+m-1]

    def build_poly_recursive(items):
        if len(items) == 1:
            return items
        mid = len(items) // 2
        left = build_poly_recursive(items[:mid])
        right = build_poly_recursive(items[mid:])
        return multiply(left, right)

    # Prepare items for D&C
    # Each item is a polynomial (list of coeffs)
    items = []
    for w in counts:
        k = counts[w]
        # Polynomial for (1 + w*z)^k
        # Coeffs: C(k, j) * w^j
        poly = [0] * (k + 1)
        w_pow = 1
        for j in range(k + 1):
            c = (fact[k] * inv_fact[j]) % MOD * inv_fact[k-j] % MOD
            poly[j] = (c * w_pow) % MOD
            w_pow = (w_pow * w) % MOD
        items.append(poly)
    
    # Compute P(z) = product (1 + w*z)^count[w]
    P = build_poly_recursive(items)
    # P has length N+1
    
    # Now compute the answer
    # Total Sum = (N-1)! * sum_{v} (digit_sums_by_w[v] * F(v))
    # F(v) = sum_{k=0}^{N-1} k! * (N-1-k)! * b_k(v)
    # b_k(v) = coeff of z^k in P(z) / (1 + v*z)
    # b_k(v) = P[k] - v * b_{k-1}(v)
    
    total_ans = 0
    
    for w in counts:
        v = w
        k_count = counts[w]
        ds = digit_sums_by_w[w]
        
        # Compute b_k iteratively
        # b_0 = P[0]
        # b_k = P[k] - v * b_{k-1}
        
        b_prev = P[0] # Should be 1
        term_sum = 0
        
        # k=0 term
        # 0! * (N-1)! * b_0
        term = (fact[0] * fact[N-1]) % MOD * b_prev % MOD
        term_sum = (term_sum + term) % MOD
        
        for k in range(1, N):
            # b_k = P[k] - v * b_{k-1}
            b_curr = (P[k] - v * b_prev) % MOD
            if b_curr < 0:
                b_curr += MOD
            
            # term = k! * (N-1-k)! * b_k
            term = (fact[k] * fact[N-1-k]) % MOD * b_curr % MOD
            term_sum = (term_sum + term) % MOD
            
            b_prev = b_curr
            
        contrib = (ds * term_sum) % MOD
        total_ans = (total_ans + contrib) % MOD

    # Final result
    ans = (total_ans * fact[N-1]) % MOD
    print(ans)

if __name__ == '__main__':
    solve()