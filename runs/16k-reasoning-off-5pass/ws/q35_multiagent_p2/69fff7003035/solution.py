import sys

def solve():
    # Read input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    MOD = 998244353
    
    # Precompute factorials and inverse factorials if needed, 
    # but we only need factorials for W_j = j! * (N-1-j)!
    # Precompute factorials up to N
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Precompute powers of 10
    pow10 = [1] * (N + 1)
    curr = 1
    for i in range(1, N + 1):
        curr = (curr * 10) % MOD
        pow10[i] = curr
        
    # Count numbers by digit length and sum their values
    # Max digits for N <= 2*10^5 is 6
    max_len = len(str(N))
    
    count_by_len = [0] * (max_len + 1)
    sum_val_by_len = [0] * (max_len + 1)
    
    for k in range(1, N + 1):
        s = str(k)
        l = len(s)
        count_by_len[l] += 1
        sum_val_by_len[l] = (sum_val_by_len[l] + k) % MOD
        
    # Compute DP_full[j]: sum of 10^(sum of lengths of subset) for all subsets of size j from ALL numbers 1..N
    # DP[j] represents the sum of 10^(total length) for subsets of size j
    # Initialize DP[0] = 1 (empty subset has length sum 0, 10^0 = 1)
    dp_full = [0] * (N) # We need indices 0 to N-1
    dp_full[0] = 1
    
    # We process each number k from 1 to N.
    # To optimize, we process by length groups.
    # For each length L, there are count_by_len[L] numbers.
    # Each number with length L contributes a factor of (1 + x * 10^L) to the generating function.
    # So we multiply the current DP array by (1 + x * 10^L) count_by_len[L] times.
    # This can be done efficiently.
    
    # Let's do it iteratively for each length group
    # dp[j] currently holds the sum for subsets of size j from processed numbers
    for L in range(1, max_len + 1):
        c = count_by_len[L]
        if c == 0:
            continue
        val = pow10[L]
        
        # We need to multiply the polynomial by (1 + val * x)^c
        # This is equivalent to applying the update c times:
        # new_dp[j] = dp[j] + dp[j-1] * val
        # Doing this c times naively is O(N*c), which might be O(N^2) if c is large.
        # However, we can use the fact that (1 + val*x)^c can be computed via binomial expansion or just loop.
        # Since sum of c over all L is N, and each update is O(N), total time is O(N^2) in worst case?
        # No, the inner loop runs N times for each number? No.
        # If we process one number at a time, it's O(N^2).
        # We need a faster way to apply (1 + val*x)^c.
        
        # Actually, we can just loop c times. The total number of updates is N.
        # Each update is a convolution-like step: dp[j] += dp[j-1] * val.
        # This is O(N) per number. Total O(N^2). This is too slow for N=2*10^5.
        
        # Optimization:
        # We can compute the effect of multiplying by (1 + val*x)^c using binomial coefficients?
        # Or we can just note that we only need to do this once per length group.
        # But the standard DP update for one item is:
        # for j from current_max down to 1: dp[j] = (dp[j] + dp[j-1]*val) % MOD
        # If we do this c times, it's O(c*N). Sum of c*N over all groups is N*N = O(N^2).
        
        # We need a better way.
        # Let's use the property that we only have a few distinct lengths (at most 6).
        # But the counts can be large.
        # We can use binary exponentiation for polynomials? No, degree is N.
        
        # Alternative:
        # The generating function is Product_{L} (1 + 10^L x)^{C_L}.
        # We can compute this product using divide and conquer or just simple iteration if we are careful.
        # But wait, the degree is N. Multiplying two polynomials of degree D takes O(D^2) or O(D log D).
        # Here we have factors (1 + 10^L x).
        # We can group identical factors.
        # (1 + v x)^c.
        # We can compute this using the binomial theorem:
        # (1 + v x)^c = sum_{k=0}^c binom(c, k) v^k x^k.
        # Then we convolve this with the current DP.
        # Convolution of size N with size c takes O(N*c). Still potentially O(N^2).
        
        # However, note that c can be up to N.
        # But there are only 6 lengths.
        # Let's try to optimize the DP update.
        # Actually, for N=2*10^5, O(N^2) is TLE.
        
        # Let's re-evaluate.
        # We need DP_full[j] for j=0..N-1.
        # DP_full is the coefficient of x^j in Product_{k=1}^N (1 + 10^{len(k)} x).
        # This is equivalent to Product_{L=1}^6 (1 + 10^L x)^{C_L}.
        # We can compute this product by multiplying polynomials.
        # Since there are only 6 factors, we can multiply them one by one.
        # Multiplying a polynomial of degree D by (1 + v x)^c.
        # (1 + v x)^c has degree c.
        # If we multiply a polynomial of degree D by a polynomial of degree c, the result has degree D+c.
        # The cost is O(D*c).
        # If we do this sequentially:
        # Start with P(x) = 1 (degree 0).
        # Multiply by (1 + 10^1 x)^{C_1}. Cost O(0 * C_1) = 0? No, result degree C_1.
        # Then multiply by (1 + 10^2 x)^{C_2}. Cost O(C_1 * C_2).
        # Total cost sum_{i<j} C_i C_j. This is roughly (Sum C_i)^2 / 2 = N^2 / 2. Still O(N^2).
        
        # Is there an O(N) or O(N log N) way?
        # Yes, using FFT/NTT for polynomial multiplication.
        # But implementing NTT in Python for competitive programming is complex and might be slow due to overhead.
        # However, N=2*10^5 is small enough for O(N log N) NTT in C++, but in Python?
        # Maybe the constraints allow O(N^2) if the constant is small? No, 4*10^10 ops is too much.
        
        # Let's look at the structure again.
        # We need DP_L[j] for each length L.
        # DP_L is derived from DP_full by removing one item of length L.
        # DP_full[j] = DP_L[j] + DP_L[j-1] * 10^L.
        # So DP_L[j] = DP_full[j] - DP_L[j-1] * 10^L.
        # This allows computing DP_L from DP_full in O(N).
        # So the bottleneck is computing DP_full.
        
        # Can we compute DP_full in O(N)?
        # DP_full[j] is the sum of 10^(sum of lengths) for subsets of size j.
        # This is the coefficient of x^j in Product_{k=1}^N (1 + 10^{len(k)} x).
        # Let G(x) = Product_{L=1}^6 (1 + 10^L x)^{C_L}.
        # We can compute the logarithm of G(x) and then exponentiate?
        # log(G(x)) = sum_{L} C_L log(1 + 10^L x) = sum_{L} C_L sum_{m=1}^\infty (-1)^{m-1} (10^L x)^m / m
        # = sum_{m=1}^\infty (-1)^{m-1} x^m / m sum_{L} C_L 10^{L m}
        # Let S_m = sum_{L} C_L 10^{L m}.
        # Then log(G(x)) = sum_{m=1}^N (-1)^{m-1} S_m / m x^m.
        # Then G(x) = exp(log(G(x))).
        # We can compute the coefficients of log(G(x)) in O(N) (since we only need up to x^N).
        # Then we can compute the exponential of a polynomial in O(N log N) using Newton's method / NTT.
        # In Python, implementing NTT is feasible.
        
        # Steps for O(N log N):
        # 1. Compute S_m for m=1..N. S_m = sum_{L=1}^6 C_L * (10^L)^m.
        #    This is O(N * 6) = O(N).
        # 2. Compute log_G[x^m] = (-1)^{m-1} * S_m * inv(m) % MOD.
        # 3. Compute G(x) = exp(log_G(x)) using polynomial exponentiation.
        #    This requires NTT.
        
        # Given the complexity of implementing NTT in Python within a single script and potential TLE due to Python's slowness,
        # let's check if there's a simpler O(N) DP.
        # The standard DP for knapsack-like problems is O(N * max_weight). Here max_weight is N.
        # But the "weights" are 10^L, which are large, but we only care about the count j.
        # The state is just j.
        # The transition is dp[j] += dp[j-1] * 10^L.
        # This is O(N) per item. Total O(N^2).
        
        # Wait, is there a combinatorial formula?
        # DP_full[j] = sum_{k_1 + ... + k_6 = j} (Product_{L} binom(C_L, k_L) * (10^L)^{k_L})
        # This is a sum over compositions.
        # This doesn't simplify easily.
        
        # Let's try the NTT approach. It's the most robust for O(N log N).
        # We need a modular NTT for MOD = 998244353.
        # 998244353 = 119 * 2^23 + 1. Primitive root is 3.
        
        # Implement NTT
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

        def poly_mul(a, b):
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

        def poly_inv(a, n):
            # Compute inverse of polynomial a modulo x^n
            if a[0] == 0:
                raise ValueError("Polynomial must have non-zero constant term")
            res = [pow(a[0], MOD - 2, MOD)]
            cur_len = 1
            while cur_len < n:
                cur_len <<= 1
                # res = res * (2 - a * res) mod x^cur_len
                # Truncate a and res to cur_len
                a_trunc = a[:cur_len] if len(a) >= cur_len else a + [0]*(cur_len - len(a))
                res_trunc = res + [0]*(cur_len - len(res))
                
                # Compute a * res
                prod = poly_mul(a_trunc, res_trunc)
                # 2 - prod
                sub = [(-prod[i]) % MOD for i in range(len(prod))]
                sub[0] = (2 + sub[0]) % MOD
                sub = sub[:cur_len]
                
                res = poly_mul(res, sub)
                res = res[:cur_len]
            return res[:n]

        def poly_log(a, n):
            # Compute log(a) mod x^n
            # a[0] must be 1
            if a[0] != 1:
                raise ValueError("Polynomial must have constant term 1")
            # log(a) = integral(a'/a)
            # a' is derivative
            da = [0] * n
            for i in range(1, n):
                da[i-1] = (i * a[i]) % MOD
            da[n-1] = 0 # Truncate to degree n-1
            
            inv_a = poly_inv(a, n)
            prod = poly_mul(da, inv_a)
            # Integrate
            res = [0] * n
            inv = [pow(i, MOD - 2, MOD) for i in range(1, n)]
            for i in range(n-1):
                res[i+1] = (prod[i] * inv[i]) % MOD
            return res

        def poly_exp(a, n):
            # Compute exp(a) mod x^n
            # a[0] must be 0
            if a[0] != 0:
                raise ValueError("Polynomial must have constant term 0")
            res = [1]
            cur_len = 1
            while cur_len < n:
                cur_len <<= 1
                # res = res * (1 + a - log(res)) mod x^cur_len
                # log(res)
                log_res = poly_log(res, cur_len)
                # a - log_res
                a_trunc = a[:cur_len] if len(a) >= cur_len else a + [0]*(cur_len - len(a))
                diff = [0] * cur_len
                for i in range(cur_len):
                    val = a_trunc[i] - log_res[i]
                    diff[i] = val % MOD
                diff[0] = (diff[0] + 1) % MOD
                
                res = poly_mul(res, diff)
                res = res[:cur_len]
            return res[:n]

        # Compute S_m
        S = [0] * (N + 1)
        for m in range(1, N + 1):
            val = 0
            for L in range(1, max_len + 1):
                if count_by_len[L] > 0:
                    term = (count_by_len[L] * pow10[L * m % N]) % MOD # pow10 index can be large, mod N? No, 10^(Lm) mod MOD
                    # pow10 array is up to N. L*m can be > N.
                    # We need 10^(L*m) % MOD.
                    # pow(10, L*m, MOD)
                    term = (count_by_len[L] * pow(10, L * m, MOD)) % MOD
                    val = (val + term) % MOD
            S[m] = val
            
        # Compute log_G
        log_G = [0] * N
        for m in range(1, N):
            sign = 1 if (m - 1) % 2 == 0 else -1
            term = (S[m] * pow(m, MOD - 2, MOD)) % MOD
            if sign == -1:
                term = (-term) % MOD
            log_G[m-1] = term # log_G is degree N-1, so N coefficients? No, log_G has N coefficients for x^0..x^{N-1}
            # log_G[0] is 0 since m starts at 1.
            
        # Compute G = exp(log_G)
        G = poly_exp(log_G, N)
        
        # G[j] is DP_full[j]
        dp_full = G
        
        # Now compute the answer
        ans = 0
        
        # Precompute W_j = j! * (N-1-j)!
        W = [0] * N
        for j in range(N):
            W[j] = (fact[j] * fact[N - 1 - j]) % MOD
            
        for L in range(1, max_len + 1):
            if count_by_len[L] == 0:
                continue
            
            # Compute DP_L from DP_full
            # DP_L[j] = DP_full[j] - DP_L[j-1] * 10^L
            dp_L = [0] * N
            dp_L[0] = dp_full[0] # dp_full[0] is 1, dp_L[0] is 1
            
            val_L = pow10[L]
            for j in range(1, N):
                dp_L[j] = (dp_full[j] - dp_L[j-1] * val_L) % MOD
                
            # Compute Term_L = sum_{j=0}^{N-1} W[j] * dp_L[j]
            term_L = 0
            for j in range(N):
                term_L = (term_L + W[j] * dp_L[j]) % MOD
                
            # Add to answer
            contrib = (sum_val_by_len[L] * term_L) % MOD
            ans = (ans + contrib) % MOD
            
        print(ans)

solve()