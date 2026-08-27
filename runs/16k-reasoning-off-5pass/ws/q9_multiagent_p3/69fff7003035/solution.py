import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read N from standard input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    MOD = 998244353
    G = 3 # Primitive root for 998244353

    # Precompute factorials and inverse factorials
    MAX_N = N + 5
    fact = [1] * MAX_N
    finv = [1] * MAX_N

    for i in range(2, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD

    finv[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for i in range(MAX_N-2, 1, -1):
        finv[i] = (finv[i+1] * (i+1)) % MOD

    # Precompute powers of 10
    pow10 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow10[i] = (pow10[i-1] * 10) % MOD

    # Count numbers by length
    cnt = {}
    for i in range(1, N + 1):
        l = len(str(i))
        cnt[l] = cnt.get(l, 0) + 1
    
    # Precompute sum of numbers for each length
    sum_nums_by_len = {}
    for l in cnt:
        start = 10**(l-1)
        end = 10**l - 1
        count = cnt[l]
        # Sum = count * (start + end) // 2
        term = (start + end) % MOD
        total_sum = (count * term) % MOD
        total_sum = (total_sum * pow(2, MOD-2, MOD)) % MOD
        sum_nums_by_len[l] = total_sum

    # NTT Implementation
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
        
        w_len = n
        while w_len > 1:
            w = pow(G, (MOD - 1) // w_len, MOD)
            if invert:
                w = pow(w, MOD - 2, MOD)
            for i in range(0, n, w_len):
                u = 1
                for j in range(w_len // 2):
                    x = a[i+j]
                    y = (a[i+j+w_len//2] * u) % MOD
                    a[i+j] = (x + y) % MOD
                    a[i+j+w_len//2] = (x - y) % MOD
                    u = (u * w) % MOD
            w_len >>= 1
        if invert:
            inv_n = pow(n, MOD - 2, MOD)
            for i in range(n):
                a[i] = (a[i] * inv_n) % MOD

    def multiply(A, B):
        if not A or not B:
            return []
        n = len(A) + len(B) - 1
        size = 1
        while size < n:
            size *= 2
        fa = A + [0] * (size - len(A))
        fb = B + [0] * (size - len(B))
        ntt(fa, False)
        ntt(fb, False)
        for i in range(size):
            fa[i] = (fa[i] * fb[i]) % MOD
        ntt(fa, True)
        return fa[:n]

    def multiply_list(polys):
        if not polys:
            return [1]
        if len(polys) == 1:
            return polys[0]
        mid = len(polys) // 2
        left = multiply_list(polys[:mid])
        right = multiply_list(polys[mid:])
        return multiply(left, right)

    # Generate initial polynomials for P_full
    # P_full(y) = Product over lengths L of (1 + 10^L * y) ^ cnt[L]
    # The coefficient of y^k in (1 + 10^L * y)^c is C(c, k) * (10^L)^k
    polys = []
    for l in cnt:
        c = cnt[l]
        poly = [0] * (c + 1)
        base_val = pow10[l]
        curr = 1
        for i in range(c + 1):
            # C(c, i) * (10^L)^i
            comb = fact[c] * finv[i] % MOD * finv[c-i] % MOD
            val = comb * curr % MOD
            poly[i] = val
            curr = curr * base_val % MOD
        polys.append(poly)
    
    P_full = multiply_list(polys)
    if len(P_full) > N:
        P_full = P_full[:N]
    
    # Precompute G_coeffs for convolution
    # We need to compute Sum_{k} [y^k] P_L(y) * k! * (N-1-k)!
    # This is equivalent to the coefficient of x^(N-1) in (Sum [y^k] P_L(y) * k! * x^k) * (Sum (N-1-j)! * x^j)
    # Let F(x) = Sum [y^k] P_L(y) * k! * x^k
    # Let G(x) = Sum (N-1-j)! * x^j
    # Then Val_L = [x^(N-1)] (F(x) * G(x))
    
    G_coeffs = [0] * N
    for j in range(N):
        G_coeffs[j] = fact[N-1-j]
    
    total_ans = 0
    
    # Process each length L
    for L in cnt:
        c_L = cnt[L]
        
        # B_L coefficients: (-1)^j * 10^(L*j)
        # This corresponds to the series expansion of (1 + 10^L * y)^(-1)
        B_L = [0] * N
        curr_pow = 1
        for j in range(N):
            if j % 2 == 1:
                B_L[j] = (MOD - curr_pow) % MOD
            else:
                B_L[j] = curr_pow
            curr_pow = (curr_pow * pow10[L]) % MOD
        
        # C_L = P_full * B_L
        # We only need up to degree N-1
        size = 1
        while size < len(P_full) + N:
            size *= 2
        fa = P_full + [0] * (size - len(P_full))
        fb = B_L + [0] * (size - N)
        ntt(fa, False)
        ntt(fb, False)
        for i in range(size):
            fa[i] = (fa[i] * fb[i]) % MOD
        ntt(fa, True)
        C_L = fa[:N]
        
        # F_L[k] = C_L[k] * k!
        F_L = [ (C_L[k] * fact[k]) % MOD for k in range(N) ]
        
        # Convolve F_L and G_coeffs
        size = 1
        while size < 2 * N:
            size *= 2
        fa = F_L + [0] * (size - N)
        fb = G_coeffs + [0] * (size - N)
        ntt(fa, False)
        ntt(fb, False)
        for i in range(size):
            fa[i] = (fa[i] * fb[i]) % MOD
        ntt(fa, True)
        
        Val_L = fa[N-1]
        
        term = (c_L * sum_nums_by_len[L]) % MOD
        term = (term * Val_L) % MOD
        total_ans = (total_ans + term) % MOD

    print(total_ans)

if __name__ == '__main__':
    solve()