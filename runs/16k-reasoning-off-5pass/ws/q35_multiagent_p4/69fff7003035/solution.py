import sys

# Set recursion depth just in case, though we won't use deep recursion
sys.setrecursionlimit(2000)

def solve():
    # Read N from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    MOD = 998244353
    
    # Step 1: Count numbers and sum of numbers for each digit length d
    # Digit lengths range from 1 to len(str(N))
    # For a given digit length d, numbers are in [10^(d-1), 10^d - 1]
    # We need to intersect this with [1, N]
    
    max_d = len(str(N))
    
    # cnt[d] = count of numbers with d digits in {1, ..., N}
    # sumx[d] = sum of numbers with d digits in {1, ..., N}
    cnt = [0] * (max_d + 1)
    sumx = [0] * (max_d + 1)
    
    for d in range(1, max_d + 1):
        low = 10**(d-1)
        high = 10**d - 1
        
        # Intersection with [1, N]
        start = max(1, low)
        end = min(N, high)
        
        if start > end:
            continue
            
        count = end - start + 1
        cnt[d] = count
        
        # Sum of arithmetic progression: (start + end) * count / 2
        total_sum = (start + end) * count // 2
        sumx[d] = total_sum % MOD
        
    # Step 2: Build the generating function P(z) = Product_d (1 + 10^d * z)^cnt[d]
    # The degree of P(z) is N.
    # We use NTT for polynomial multiplication.
    
    # Precompute powers of 10 and 10^d mod MOD
    pow10 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow10[i] = (pow10[i-1] * 10) % MOD
        
    pow10_d = {}
    for d in range(1, max_d + 1):
        pow10_d[d] = pow10[d] # 10^d mod MOD
        
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
            w_len = pow(3, (MOD - 1) // length, MOD)
            if invert:
                w_len = pow(w_len, MOD - 2, MOD)
            
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
            n_inv = pow(n, MOD - 2, MOD)
            for i in range(n):
                a[i] = (a[i] * n_inv) % MOD

    def multiply(poly1, poly2):
        # Remove trailing zeros to reduce size
        while len(poly1) > 1 and poly1[-1] == 0:
            poly1.pop()
        while len(poly2) > 1 and poly2[-1] == 0:
            poly2.pop()
            
        n = 1
        while n < len(poly1) + len(poly2) - 1:
            n <<= 1
            
        fa = poly1 + [0] * (n - len(poly1))
        fb = poly2 + [0] * (n - len(poly2))
        
        ntt(fa, False)
        ntt(fb, False)
        
        for i in range(n):
            fa[i] = (fa[i] * fb[i]) % MOD
            
        ntt(fa, True)
        
        # Trim to relevant size (degree N)
        res = fa[:len(poly1) + len(poly2) - 1]
        return res

    # Start with P(z) = [1] (constant polynomial 1)
    P = [1]
    
    for d in range(1, max_d + 1):
        if cnt[d] == 0:
            continue
            
        c = pow10_d[d] # 10^d mod MOD
        k = cnt[d]
        
        # We need to multiply P by (1 + c*z)^k
        # (1 + c*z)^k = sum_{i=0}^k C(k, i) * c^i * z^i
        
        # Compute coefficients of (1 + c*z)^k
        # Coeff of z^i is C(k, i) * c^i
        binom_coeffs = []
        curr_c_pow = 1
        comb = 1
        for i in range(k + 1):
            if i > 0:
                comb = (comb * (k - i + 1)) % MOD
                comb = (comb * pow(i, MOD - 2, MOD)) % MOD
                curr_c_pow = (curr_c_pow * c) % MOD
            term = (comb * curr_c_pow) % MOD
            binom_coeffs.append(term)
            
        # Multiply P by binom_coeffs
        P = multiply(P, binom_coeffs)
        
        # Truncate P to degree N, as we only care about coefficients up to z^N
        if len(P) > N + 1:
            P = P[:N+1]
            
    # P[k] is the coefficient of z^k in the full generating function
    # P has degree at most N.
    
    # Step 3: For each digit length d, compute Q_d(z) = P(z) / (1 + 10^d * z)
    # and accumulate the answer.
    # Answer = sum_{k=0}^{N-1} k! * (N-1-k)! * (sum_{d} sumx[d] * [z^k]Q_d(z))
    
    # Precompute factorials and inverse factorials
    fact = [1] * (N + 1)
    inv_fact = [1] * (N + 1)
    
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD
        
    # Helper to compute Q_d from P
    # P(z) = (1 + c*z) * Q_d(z)
    # p_k = q_k + c * q_{k-1}  =>  q_k = p_k - c * q_{k-1}
    # q_{-1} = 0
    
    total_answer = 0
    
    for d in range(1, max_d + 1):
        if cnt[d] == 0:
            continue
            
        c = pow10_d[d]
        s_x = sumx[d]
        
        if s_x == 0:
            continue
            
        # Compute coefficients of Q_d(z)
        # Q_d has degree len(P)-1, which is at most N
        # We need coefficients up to z^{N-1} for the final sum
        
        q_coeffs = [0] * (len(P))
        q_prev = 0
        
        # We can compute q_k iteratively
        # q_0 = p_0
        # q_k = p_k - c * q_{k-1}
        
        # To avoid creating a new list for each d, we can compute the contribution directly
        # Contribution to answer for this d:
        # sum_{k=0}^{N-1} k! * (N-1-k)! * s_x * q_k
        
        # Let's compute q_k on the fly and add to total_answer
        
        current_q = 0
        for k in range(len(P)):
            p_k = P[k] if k < len(P) else 0
            current_q = (p_k - c * current_q) % MOD
            
            if k < N: # We only need up to z^{N-1} for the suffix length
                # Term: k! * (N-1-k)! * s_x * q_k
                term = (fact[k] * fact[N - 1 - k]) % MOD
                term = (term * s_x) % MOD
                term = (term * current_q) % MOD
                total_answer = (total_answer + term) % MOD
                
    print(total_answer)

solve()