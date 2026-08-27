import sys
from collections import defaultdict

# Set recursion limit just in case, though we use iterative DP
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

    # Precompute primes up to 1000
    MAX_VAL = 1000
    primes = []
    is_prime = [True] * (MAX_VAL + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, MAX_VAL + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, MAX_VAL + 1, i):
                is_prime[j] = False

    # Function to get prime factorization exponents for a number
    def get_exponents(n, primes):
        exps = {}
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                count = 0
                while n % p == 0:
                    count += 1
                    n //= p
                exps[p] = count
        if n > 1:
            exps[n] = 1
        return exps

    # For each prime, we need to compute the sum of p^(sum e_j) for valid sequences
    # where min(e_j) = 0.
    # We process each prime independently.
    
    # Collect all primes that appear in any A_i
    primes_in_A = set()
    for x in A:
        if x > 1:
            # Factorize x to find primes
            temp = x
            for p in primes:
                if p * p > temp:
                    break
                if temp % p == 0:
                    primes_in_A.add(p)
                    while temp % p == 0:
                        temp //= p
            if temp > 1:
                primes_in_A.add(temp)
    
    # If A is empty or all 1s, the only good sequence is all 1s (score 1)
    # But N >= 2, so A has at least 1 element.
    
    total_ans = 1

    # Precompute powers of primes and their inverses for speed?
    # Max exponent sum is roughly N * log2(1000) ~ 10000.
    # We can compute powers on the fly or precompute.
    
    for p in primes_in_A:
        # Get d_i = v_p(A_i) for all i
        d = []
        for x in A:
            count = 0
            temp = x
            while temp % p == 0:
                count += 1
                temp //= p
            d.append(count)
        
        # DP state: dp[v] = {min_val: weight}
        # v is the current relative exponent r_i (with r_1 = 0)
        # min_val is the minimum r_j seen so far
        # weight is p^(sum_{j=1}^i r_j)
        
        # Initial state: at i=1, r_1 = 0, min_1 = 0, sum_1 = 0, weight = p^0 = 1
        # We use a dictionary for the current layer to handle sparsity
        # Key: current_v, Value: {min_val: weight}
        
        current_dp = defaultdict(dict)
        current_dp[0] = {0: 1}
        
        for i in range(N - 1):
            step = d[i]
            next_dp = defaultdict(dict)
            
            # Precompute p^step and p^(-step) mod MOD
            p_step = pow(p, step, MOD)
            p_neg_step = pow(p_step, MOD - 2, MOD)
            
            for v, min_map in current_dp.items():
                for m, w in min_map.items():
                    # Transition 1: r_{i+1} = v + step
                    v1 = v + step
                    m1 = m if m < v1 else v1
                    w1 = (w * p_step) % MOD
                    
                    if v1 in next_dp:
                        if m1 in next_dp[v1]:
                            next_dp[v1][m1] = (next_dp[v1][m1] + w1) % MOD
                        else:
                            next_dp[v1][m1] = w1
                    else:
                        next_dp[v1] = {m1: w1}
                        
                    # Transition 2: r_{i+1} = v - step
                    v2 = v - step
                    m2 = m if m < v2 else v2
                    w2 = (w * p_neg_step) % MOD
                    
                    if v2 in next_dp:
                        if m2 in next_dp[v2]:
                            next_dp[v2][m2] = (next_dp[v2][m2] + w2) % MOD
                        else:
                            next_dp[v2][m2] = w2
                    else:
                        next_dp[v2] = {m2: w2}
            
            current_dp = next_dp
        
        # Sum up contributions
        # For each final state (v, m) with weight W, the term is W * p^(-N * m)
        p_neg_N = pow(p, -N, MOD) # This might not work directly with negative exponent in pow for some versions, use inverse
        
        # Better: p^(-N*m) = (p^(-N))^m
        p_inv = pow(p, MOD - 2, MOD)
        p_inv_N = pow(p_inv, N, MOD)
        
        prime_sum = 0
        for v, min_map in current_dp.items():
            for m, w in min_map.items():
                # Term: w * p^(-N * m)
                # p^(-N * m) = (p^(-N))^m
                factor = pow(p_inv_N, m, MOD)
                term = (w * factor) % MOD
                prime_sum = (prime_sum + term) % MOD
        
        total_ans = (total_ans * prime_sum) % MOD

    # If there are no primes in A (all A_i = 1), the answer is 1.
    # The loop above won't execute, total_ans remains 1.
    # However, we must ensure that if A_i=1, the logic holds.
    # If all A_i=1, then d_i=0 for all primes.
    # The only good sequence is S_i = 1 for all i. Score 1.
    
    print(total_ans)

solve()