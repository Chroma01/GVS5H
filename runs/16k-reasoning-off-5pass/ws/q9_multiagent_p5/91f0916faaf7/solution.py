import sys

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N - 1):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    MOD = 998244353

    # Factorize all A_i to find relevant primes and their exponents
    # We need a map: prime -> list of exponents for each step
    prime_exponents = {}
    
    # Collect all numbers to factorize
    numbers_to_factor = A
    
    # Precompute primes up to 1000
    MAX_VAL = 1000
    primes = []
    is_prime = [True] * (MAX_VAL + 1)
    for i in range(2, MAX_VAL + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, MAX_VAL + 1, i):
                is_prime[j] = False
    
    # Factorize each A_i
    for x in numbers_to_factor:
        temp = x
        for p in primes:
            if p * p > temp:
                break
            if temp % p == 0:
                cnt = 0
                while temp % p == 0:
                    cnt += 1
                    temp //= p
                if p not in prime_exponents:
                    prime_exponents[p] = []
                prime_exponents[p].append(cnt)
        if temp > 1:
            if temp not in prime_exponents:
                prime_exponents[temp] = []
            prime_exponents[temp].append(1)

    total_score = 1

    # Process each prime
    for p, exponents in prime_exponents.items():
        # exponents[i] is the step size k_i for step i (from S_i to S_{i+1})
        # We have N-1 steps, so exponents has length N-1
        
        # If all exponents are 0, the contribution is 1 (since min(e)=0 implies e_i=0 for all i)
        if all(e == 0 for e in exponents):
            continue
        
        # We need to compute G(0) = sum_{h>=0} dp[N][h]
        # where dp[i][h] = p^h * x[i][h]
        # x[i][h] satisfies: x[i][h] = p^{-k} * x[i-1][h-k] + p^k * x[i-1][h+k]
        # Base case: x[0][h] = 1 for all h >= 0.
        # We compute x[i][h] for h up to LIMIT = N * max(k).
        # For h > LIMIT, x[i][h] = C^i where C = p^{-k} + p^k.
        
        k_list = exponents
        max_k = max(k_list)
        LIMIT = N * max_k
        
        # Precompute powers of p
        # We need up to LIMIT + max_k + 1 for the tail calculation
        limit_pow = LIMIT + max_k + 2
        pow_p = [1] * limit_pow
        curr = 1
        for i in range(1, limit_pow):
            curr = (curr * p) % MOD
            pow_p[i] = curr
            
        # Precompute powers of C
        # C = p^{-k} + p^k. Note: k varies per step, so we need to handle this carefully.
        # Actually, the recurrence for x[i][h] depends on the specific k_i at step i.
        # So C is not constant across steps.
        # My previous derivation assumed constant k. Here k changes.
        # So we cannot use a single C for the tail.
        # However, for h > LIMIT, the path cannot touch 0.
        # So for h > LIMIT, the recurrence is homogeneous: x[i][h] = p^{-k_i} x[i-1][h-k_i] + p^{k_i} x[i-1][h+k_i].
        # Since h > LIMIT >= N * max_k, both h-k_i and h+k_i are > LIMIT (assuming LIMIT is large enough).
        # Actually, if h > LIMIT, then h - k_i > LIMIT - max_k. This might be <= LIMIT.
        # So the "tail" logic is more complex if k varies.
        # But we can simply extend the DP array to be large enough such that for h > LIMIT,
        # the values are determined by the homogeneous recurrence.
        # Let's set LIMIT = N * max_k.
        # If h > LIMIT, then h - k_i > LIMIT - max_k.
        # If we set the array size to LIMIT + max_k + 1, then for h in [LIMIT+1, ...],
        # h - k_i might be in the array or not.
        # To be safe, let's just compute the DP for h up to LIMIT + max_k.
        # And for the tail, we assume the homogeneous behavior.
        # But since k varies, the homogeneous solution is not simply C^i.
        # It is a product of terms.
        # Let's re-evaluate the tail.
        # If h is very large, the boundary at 0 is never touched.
        # So x[i][h] = (product_{j=1}^i (p^{-k_j} + p^{k_j})) * x[0][h].
        # Since x[0][h] = 1, x[i][h] = Product_{j=1}^i (p^{-k_j} + p^{k_j}).
        # Let ProdC[i] = Product_{j=1}^i (p^{-k_j} + p^{k_j}).
        # Then for h > LIMIT, x[i][h] = ProdC[i].
        # This is valid if h - k_j > 0 for all j <= i.
        # If we choose LIMIT = N * max_k, then for h > LIMIT, h - k_j > N*max_k - max_k >= 0.
        # So the condition holds.
        # So we can compute ProdC array.
        
        # Precompute ProdC
        prod_c = [1] * (N + 1)
        current_prod = 1
        for i in range(N - 1):
            k = k_list[i]
            pk = pow_p[k]
            inv_pk = pow(pk, MOD - 2, MOD)
            term = (inv_pk + pk) % MOD
            current_prod = (current_prod * term) % MOD
            prod_c[i+1] = current_prod
        
        # DP for x
        # x[h] stores x[i][h]
        # We need to handle the boundary for h+k > LIMIT.
        # If h+k > LIMIT, x[i-1][h+k] = prod_c[i-1].
        # But we need to be careful: prod_c[i-1] is valid only if h+k > LIMIT.
        # Let's set the array size to LIMIT + max_k + 1.
        # Then for h in 0..LIMIT, h+k can be up to LIMIT + max_k.
        # If h+k > LIMIT, we use prod_c[i-1].
        # Wait, if h+k > LIMIT, is it guaranteed that x[i-1][h+k] = prod_c[i-1]?
        # Yes, because h+k > LIMIT >= N*max_k >= (i-1)*max_k.
        # So h+k - k_j > 0 for all j <= i-1.
        
        # Array size
        array_size = LIMIT + max_k + 1
        x = [1] * array_size
        
        # Precompute prod_c for access
        # prod_c[i] corresponds to step i (after i steps)
        
        for i in range(1, N):
            new_x = [0] * array_size
            k = k_list[i-1]
            inv_pk = pow(pow_p[k], MOD - 2, MOD)
            pk = pow_p[k]
            C_prev = prod_c[i-1]
            
            # We can optimize the loop
            # For h in 0..LIMIT:
            #   term1 = x[h-k] if h>=k else 0
            #   term2 = x[h+k] if h+k < array_size else C_prev
            #   new_x[h] = term1 * inv_pk + term2 * pk
            
            # To speed up, we can iterate h
            for h in range(array_size):
                val = 0
                if h >= k:
                    val += x[h-k]
                if h + k < array_size:
                    val += x[h+k]
                else:
                    val += C_prev
                
                # new_x[h] = val * inv_pk + val * pk? No.
                # We need to multiply the terms separately.
                # But wait, if h+k >= array_size, we use C_prev.
                # If h+k < array_size, we use x[h+k].
                # The logic above combines them into 'val'.
                # But we need to multiply x[h-k] by inv_pk and x[h+k] by pk.
                
                term1 = 0
                if h >= k:
                    term1 = x[h-k]
                term2 = 0
                if h + k < array_size:
                    term2 = x[h+k]
                else:
                    term2 = C_prev
                
                new_x[h] = (term1 * inv_pk + term2 * pk) % MOD
            x = new_x
            
        # Sum
        # We need sum_{h=0}^{infinity} p^h * x[N][h]
        # We computed x up to array_size - 1.
        # For h >= array_size, x[N][h] = prod_c[N].
        # So sum = sum_{h=0}^{array_size-1} p^h * x[N][h] + sum_{h=array_size}^inf p^h * prod_c[N]
        # Tail = prod_c[N] * sum_{h=array_size}^inf p^h = prod_c[N] * p^{array_size} / (1-p)
        
        total_sum = 0
        for h in range(array_size):
            total_sum = (total_sum + pow_p[h] * x[h]) % MOD
            
        tail = (prod_c[N] * pow_p[array_size]) % MOD
        inv_1_minus_p = pow(1 - p, MOD - 2, MOD)
        tail = (tail * inv_1_minus_p) % MOD
        
        Y = (total_sum + tail) % MOD
        X = (Y * (1 - pow(p, N, MOD))) % MOD
        X = (X + MOD) % MOD
        
        total_score = (total_score * X) % MOD

    print(total_score)

if __name__ == '__main__':
    solve()