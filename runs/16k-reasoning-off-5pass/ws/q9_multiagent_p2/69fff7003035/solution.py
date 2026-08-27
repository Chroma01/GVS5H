import sys

# Increase recursion depth just in case, though not strictly needed for this iterative solution
sys.setrecursionlimit(200005)

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

def inv(n, m=MOD):
    return power(n, m - 2, m)

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
    while n < len(a) + len(b):
        n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = (fa[i] * fb[i]) % MOD
    ntt(fa, True)
    return fa[:len(a) + len(b) - 1]

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    # Count lengths and sum of values for each length
    # Lengths can be 1 to 6 for N <= 200,000
    cnt = [0] * 7
    sum_vals = [0] * 7
    
    for i in range(1, N + 1):
        s = str(i)
        l = len(s)
        cnt[l] += 1
        sum_vals[l] = (sum_vals[l] + i) % MOD
        
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = (fact[i - 1] * i) % MOD
        
    # Precompute powers of 10
    pow10 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow10[i] = (pow10[i - 1] * 10) % MOD
        
    # Construct polynomials for each length group
    # Poly_l(x) = sum_{i=0}^{cnt[l]} C(cnt[l], i) * (10^l)^i * x^i
    polys = []
    for l in range(1, 7):
        c = cnt[l]
        if c == 0:
            continue
        # Coefficients for (1 + x * 10^l)^c
        # We need binomial coefficients C(c, i)
        
        # Construct the list of coefficients
        # degree is c
        poly = [0] * (c + 1)
        base = pow10[l]
        
        # Compute C(c, i) * base^i
        # C(c, 0) = 1
        # C(c, i) = C(c, i-1) * (c - i + 1) / i
        
        curr_comb = 1
        curr_pow = 1
        
        poly[0] = 1
        
        for i in range(1, c + 1):
            # Update combination: C(c, i) = C(c, i-1) * (c - i + 1) * inv(i)
            curr_comb = (curr_comb * (c - i + 1)) % MOD
            curr_comb = (curr_comb * inv(i)) % MOD
            
            curr_pow = (curr_pow * base) % MOD
            
            term = (curr_comb * curr_pow) % MOD
            poly[i] = term
            
        polys.append(poly)
        
    # Multiply all polynomials
    # Start with [1]
    current_poly = [1]
    for p in polys:
        current_poly = multiply(current_poly, p)
        
    # current_poly[j] is A_j = sum_s C(j, s) * 10^s
    # We need to compute:
    # S1 = sum_{j=0}^{N-1} A_j * j! * (N-j-1)!
    # S2(L) = 10^L * sum_{j=0}^{N-2} A_j * (j+1)! * (N-j-2)!
    
    # Note: current_poly has length N+1 (indices 0 to N)
    
    S1 = 0
    for j in range(N): # j goes from 0 to N-1
        # term: A_j * j! * (N-1-j)!
        term = (current_poly[j] * fact[j]) % MOD
        term = (term * fact[N - 1 - j]) % MOD
        S1 = (S1 + term) % MOD
        
    # Precompute S2 contributions for each length L
    # S2(L) = 10^L * sum_{j=0}^{N-2} A_j * (j+1)! * (N-j-2)!
    # Let's compute the inner sum part first: SumInner = sum_{j=0}^{N-2} A_j * (j+1)! * (N-j-2)!
    # Then S2(L) = 10^L * SumInner
    
    SumInner = 0
    # j ranges from 0 to N-2
    # If N=1, range is empty (0 to -1), sum is 0.
    limit = N - 2
    if limit >= 0:
        for j in range(limit + 1):
            # term: A_j * (j+1)! * (N-j-2)!
            term = (current_poly[j] * fact[j + 1]) % MOD
            term = (term * fact[N - j - 2]) % MOD
            SumInner = (SumInner + term) % MOD
            
    # Now compute final answer
    ans = 0
    for l in range(1, 7):
        if cnt[l] == 0:
            continue
            
        # Contribution of numbers with length l
        # SumVal[l] * (S1 - 10^l * SumInner)
        term = (S1 - (pow10[l] * SumInner) % MOD) % MOD
        contribution = (sum_vals[l] * term) % MOD
        ans = (ans + contribution) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()