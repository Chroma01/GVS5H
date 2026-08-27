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

    # If N=1, the problem says A has length N-1, so A is empty.
    # But constraints say N >= 2.
    # If N=2, A has 1 element.

    # Step 1: Factorize all A_i to find relevant primes and their exponents.
    # We need to group exponents by prime.
    # prime_exponents[p] will be a list of exponents of p in A_1, A_2, ..., A_{N-1}
    prime_exponents = defaultdict(list)
    
    # Precompute primes up to 1000 for factorization
    limit = 1000
    primes = []
    is_prime = [True] * (limit + 1)
    for i in range(2, limit + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

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
            prime_exponents[temp].append(0) # It appeared in one A_i, but we need to align with N-1 elements
            # Wait, if temp > 1, it's a prime factor of val.
            # We need to ensure the list has length N-1.
            # The defaultdict(list) approach above only appends when found.
            # We need to pad with 0s.
            pass

    # Re-factorize properly to ensure all lists have length N-1
    prime_exponents = defaultdict(lambda: [0] * (N - 1))
    
    for idx, val in enumerate(A):
        temp = val
        for p in primes:
            if p * p > temp:
                break
            if temp % p == 0:
                count = 0
                while temp % p == 0:
                    count += 1
                    temp //= p
                prime_exponents[p][idx] = count
        if temp > 1:
            prime_exponents[temp][idx] = temp # Wait, temp is the prime itself, count is 1.
            # Correction:
            prime_exponents[temp][idx] = 1

    # Get all relevant primes
    relevant_primes = list(prime_exponents.keys())

    total_ans = 1

    # Step 2: For each prime, compute the sum of scores contribution
    for p in relevant_primes:
        k = prime_exponents[p] # List of length N-1
        
        # DP state: map from (current_min_offset, current_offset) to sum of p^{sum_offsets}
        # Initial state: at i=1 (first element), offset is 0, min is 0.
        # dp[(min_off, curr_off)] = sum_val
        dp = defaultdict(int)
        dp[(0, 0)] = 1
        
        # Precompute powers of p modulo MOD for efficiency
        # We might need negative powers? No, we work in modular arithmetic.
        # But offsets can be negative. p^offset mod MOD requires modular inverse if offset < 0.
        # However, the final formula is p^{-N * min + sum}.
        # We can compute everything in integers? No, numbers are huge.
        # We must work in Z_p.
        # p^(-x) mod MOD = pow(p, MOD-1-x, MOD) ? No, pow(p, -x, MOD) works in Python 3.8+
        
        # Let's verify Python version support. Usually competitive envs support pow(a, b, m) with negative b if a and m coprime.
        # Yes, it computes modular inverse.
        
        for i in range(N - 1):
            ki = k[i]
            new_dp = defaultdict(int)
            
            # Iterate over current states
            for (min_off, curr_off), val in dp.items():
                # Option 1: next_off = curr_off + ki
                next_off_1 = curr_off + ki
                new_min_1 = min(min_off, next_off_1)
                # Multiply by p^{next_off_1}
                term1 = (val * pow(p, next_off_1, MOD)) % MOD
                new_dp[(new_min_1, next_off_1)] = (new_dp[(new_min_1, next_off_1)] + term1) % MOD
                
                # Option 2: next_off = curr_off - ki
                next_off_2 = curr_off - ki
                new_min_2 = min(min_off, next_off_2)
                # Multiply by p^{next_off_2}
                term2 = (val * pow(p, next_off_2, MOD)) % MOD
                new_dp[(new_min_2, next_off_2)] = (new_dp[(new_min_2, next_off_2)] + term2) % MOD
            
            dp = new_dp

        # After processing all N-1 steps, we have states for offsets relative to e_1.
        # For each state (min_off, curr_off), the actual sequence of exponents is determined by e_1 = -min_off.
        # The total exponent sum is sum_offsets + N * e_1 = sum_offsets - N * min_off.
        # The value stored in dp[(min_off, curr_off)] is sum of p^{sum_offsets} for paths ending at (min_off, curr_off).
        # So we multiply by p^{-N * min_off}.
        
        prime_sum = 0
        for (min_off, curr_off), val in dp.items():
            # exponent = -N * min_off
            # We need val * p^{-N * min_off}
            # Note: min_off <= 0. So -N * min_off >= 0.
            # Let exp = -N * min_off.
            exp = -N * min_off
            term = (val * pow(p, exp, MOD)) % MOD
            prime_sum = (prime_sum + term) % MOD
            
        total_ans = (total_ans * prime_sum) % MOD

    print(total_ans)

solve()