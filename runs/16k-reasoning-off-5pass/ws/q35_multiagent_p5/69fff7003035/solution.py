import sys

# Set recursion limit just in case, though we'll use iterative NTT
sys.setrecursionlimit(200000)

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    MOD = 998244353
    G = 3
    
    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    inv_fact = [1] * (N + 1)
    
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD
        
    def inverse(n):
        return pow(n, MOD - 2, MOD)

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
                
        length = 2
        while length <= n:
            w_len = pow(G, (MOD - 1) // length, MOD)
            if invert:
                w_len = inverse(w_len)
            
            for i in range(0, n, length):
                w = 1
                for j in range(i, i + length // 2):
                    u = a[j]
                    v = (a[j + length // 2] * w) % MOD
                    a[j] = (u + v) % MOD
                    a[j + length // 2] = (u - v + MOD) % MOD
                    w = (w * w_len) % MOD
            length <<= 1
            
        if invert:
            n_inv = inverse(n)
            for i in range(n):
                a[i] = (a[i] * n_inv) % MOD

    def multiply(poly1, poly2):
        n = 1
        while n < len(poly1) + len(poly2) - 1:
            n <<= 1
            
        a = poly1 + [0] * (n - len(poly1))
        b = poly2 + [0] * (n - len(poly2))
        
        ntt(a, False)
        ntt(b, False)
        
        for i in range(n):
            a[i] = (a[i] * b[i]) % MOD
            
        ntt(a, True)
        
        return a[:len(poly1) + len(poly2) - 1]

    # Count numbers with each length
    # Lengths are from 1 to len(str(N))
    len_counts = {}
    for k in range(1, N + 1):
        l = len(str(k))
        len_counts[l] = len_counts.get(l, 0) + 1
        
    # Sum of numbers with each length
    len_sum = {}
    for k in range(1, N + 1):
        l = len(str(k))
        if l not in len_sum:
            len_sum[l] = 0
        len_sum[l] = (len_sum[l] + k) % MOD
        
    # Compute polynomial P(y) = Product_{d} (1 + y * 10^d)^{Count_d}
    # Start with polynomial [1]
    P = [1]
    
    for d, count in len_counts.items():
        base_poly = [1, pow(10, d, MOD)]
        # Compute base_poly^count using binary exponentiation
        result = [1]
        base = base_poly
        
        exp = count
        while exp > 0:
            if exp % 2 == 1:
                result = multiply(result, base)
                # Truncate to degree N to keep size manageable
                if len(result) > N + 1:
                    result = result[:N+1]
            base = multiply(base, base)
            if len(base) > N + 1:
                base = base[:N+1]
            exp //= 1
            
        P = multiply(P, result)
        if len(P) > N + 1:
            P = P[:N+1]
            
    # P now has coefficients C_m for m=0 to N (or less)
    # Ensure P has length N+1
    while len(P) <= N:
        P.append(0)
        
    # For each distinct length d, compute Q_d(y) such that Q_d(y) * (1 + y * 10^d) = P(y)
    # Coefficients q_m satisfy: q_m + 10^d * q_{m-1} = C_m
    # So q_m = C_m - 10^d * q_{m-1}
    
    total_answer = 0
    
    for d in len_counts:
        pow10d = pow(10, d, MOD)
        
        # Compute coefficients of Q_d(y)
        Q = [0] * (N + 1)
        q_prev = 0
        for m in range(N + 1):
            C_m = P[m] if m < len(P) else 0
            q_curr = (C_m - pow10d * q_prev) % MOD
            Q[m] = q_curr
            q_prev = q_curr
            
        # Compute S_d = sum_{m=0}^{N-1} (N-1-m)! * m! * q_m
        # Note: The suffix size is m, so the number of elements after k is m.
        # The number of elements before k is (N-1) - m.
        # The weight is ((N-1-m)! * m!)
        # We sum for m from 0 to N-1 (since suffix can have 0 to N-1 elements)
        
        S_d = 0
        for m in range(N): # m from 0 to N-1
            # weight = (N-1-m)! * m!
            weight = (fact[N-1-m] * fact[m]) % MOD
            term = (weight * Q[m]) % MOD
            S_d = (S_d + term) % MOD
            
        # Add contribution: S_d * (sum of k with length d)
        contribution = (S_d * len_sum[d]) % MOD
        total_answer = (total_answer + contribution) % MOD
        
    print(total_answer)

solve()