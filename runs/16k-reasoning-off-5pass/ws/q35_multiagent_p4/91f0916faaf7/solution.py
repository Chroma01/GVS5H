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

    # Factorize all A_i to find relevant primes and their exponents
    # We need to process each prime independently.
    # Map: prime -> list of exponents a_i for i=1..N-1
    prime_exponents = defaultdict(list)
    
    # Precompute primes up to 1000
    MAX_A = 1000
    primes = []
    is_prime = [True] * (MAX_A + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, MAX_A + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, MAX_A + 1, i):
                is_prime[j] = False

    # For each A_i, factorize and record exponents for each prime
    # A has length N-1
    for val in A:
        temp = val
        for p in primes:
            if p * p > temp:
                break
            if temp % p == 0:
                count = 0
                while temp % p == 0:
                    count += 1
                    temp //= p
                prime_exponents[p].append(count)
        if temp > 1:
            # temp is a prime > sqrt(1000) ~ 31.6
            # It could be up to 1000
            prime_exponents[temp].append(1)
            
    # If A_i=1, it contributes 0 to all primes, which is handled by not adding to dict.
    # We need to ensure that for primes not in prime_exponents, the exponent list is effectively all zeros.
    # But we only iterate over primes that appear. Primes not appearing have all a_i=0.
    # For such primes, the only valid sequence is e_i=0 for all i (since min=0 and diffs=0).
    # Score contribution is p^0 = 1. So they don't affect the product.
    
    total_ans = 1
    
    # Precompute powers of primes modulo MOD for efficiency?
    # Actually, we compute p^k on the fly or precompute small powers.
    # Since exponents can be large, we use pow(p, k, MOD).
    
    for p, exps in prime_exponents.items():
        # exps is a list of length N-1
        # DP state: dictionary mapping (min_delta, current_delta) -> sum_of_weights
        # weight for a path is p^(sum of deltas so far)
        # Initial state: at index 1 (before any transitions), delta_1 = 0, min_delta = 0, sum_deltas = 0.
        # Weight = p^0 = 1.
        
        # dp[(m, d)] = sum of p^(sum_{k=1}^i delta_k)
        dp = defaultdict(int)
        dp[(0, 0)] = 1
        
        for a_i in exps:
            new_dp = defaultdict(int)
            
            # If a_i is 0, delta doesn't change, min doesn't change (since d'=d)
            # But we still multiply weight by p^d.
            
            # To optimize, we iterate over current states
            for (m, d), weight in dp.items():
                # Option 1: delta increases by a_i
                d1 = d + a_i
                m1 = m if m < d1 else d1 # min(m, d1)
                
                # Weight update: multiply by p^d1
                # We need p^d1 mod MOD. Note d1 can be negative? 
                # No, d1 is an integer exponent. But wait, delta can be negative.
                # p^d1 where d1 is negative? 
                # In the formula, the term is p^(sum delta). 
                # The transition adds d1 to the sum of deltas.
                # So we multiply the accumulated weight by p^d1.
                # If d1 is negative, we need modular inverse.
                
                # Calculate p^d1 mod MOD
                if d1 >= 0:
                    term1 = pow(p, d1, MOD)
                else:
                    term1 = pow(p, -d1, MOD)
                    term1 = pow(term1, MOD - 2, MOD)
                
                new_weight1 = (weight * term1) % MOD
                new_dp[(m1, d1)] = (new_dp[(m1, d1)] + new_weight1) % MOD
                
                # Option 2: delta decreases by a_i
                d2 = d - a_i
                m2 = m if m < d2 else d2
                
                if d2 >= 0:
                    term2 = pow(p, d2, MOD)
                else:
                    term2 = pow(p, -d2, MOD)
                    term2 = pow(term2, MOD - 2, MOD)
                    
                new_weight2 = (weight * term2) % MOD
                new_dp[(m2, d2)] = (new_dp[(m2, d2)] + new_weight2) % MOD
                
            dp = new_dp
            
        # After processing all N-1 transitions, we have states for index N.
        # For each state (m, d), the total exponent of p in the score is:
        # E = -N * m + d
        # The contribution is p^E.
        # The value stored in dp[(m,d)] is sum of p^(sum_{k=1}^N delta_k).
        # Let S = sum_{k=1}^N delta_k. Note that d is delta_N.
        # Wait, the DP state stores sum of weights.
        # The weight for a specific path is p^(sum_{k=1}^N delta_k).
        # The final exponent for the score is -N*m + sum_{k=1}^N delta_k.
        # So we need to multiply the stored weight by p^(-N*m).
        
        prime_ans = 0
        for (m, d), weight in dp.items():
            # Exponent part from min: -N * m
            # We need to multiply weight by p^(-N*m)
            exp_min = -N * m
            if exp_min >= 0:
                factor = pow(p, exp_min, MOD)
            else:
                factor = pow(p, -exp_min, MOD)
                factor = pow(factor, MOD - 2, MOD)
            
            term = (weight * factor) % MOD
            prime_ans = (prime_ans + term) % MOD
            
        total_ans = (total_ans * prime_ans) % MOD

    print(total_ans)

solve()