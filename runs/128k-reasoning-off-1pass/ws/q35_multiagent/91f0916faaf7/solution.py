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

    # Factorize each A_i to get prime exponents
    # We need to process each prime independently
    # Map: prime -> list of exponents for each A_i
    prime_exponents = defaultdict(list)
    
    # Precompute primes up to 1000 for factorization
    # Since A_i <= 1000, we only care about primes <= 1000
    limit = 1000
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    primes = [i for i in range(2, limit + 1) if is_prime[i]]
    
    # For each A_i, factorize and store exponents for each prime
    # We'll create a list of lists: prime_to_exponents[p] = [a_1, a_2, ..., a_{N-1}]
    # Initialize with 0s
    prime_to_exponents = {p: [0] * (N - 1) for p in primes}
    
    for i in range(N - 1):
        val = A[i]
        for p in primes:
            if p * p > val:
                break
            if val % p == 0:
                count = 0
                while val % p == 0:
                    count += 1
                    val //= p
                prime_to_exponents[p][i] = count
        if val > 1:
            # val is a prime > sqrt(1000) or the remaining prime factor
            # Check if it's in our primes list (it should be if <= 1000)
            if val in prime_to_exponents:
                prime_to_exponents[val][i] = 1
            else:
                # This case shouldn't happen given constraints A_i <= 1000
                # But if it did, we'd need to handle it. 
                # Since we iterate primes up to 1000, and val <= 1000, it must be in the list.
                pass

    total_answer = 1

    # For each prime, compute the sum of scores contributed by this prime
    for p, exponents in prime_to_exponents.items():
        # If no A_i has this prime factor, then all a_i = 0.
        # The condition |e_i - e_{i+1}| = 0 implies e_1 = e_2 = ... = e_N.
        # The condition min(e_i) = 0 implies e_i = 0 for all i.
        # The score contribution is p^0 = 1.
        # So if all exponents are 0, the factor is 1.
        if all(a == 0 for a in exponents):
            continue
            
        # DP state: dictionary mapping (d, m) -> sum_p_S
        # d = P_i - m, m = min(P_1, ..., P_i)
        # P_1 = 0, so initially d=0, m=0, sum_P = 0.
        # dp[(d, m)] stores the sum of p^(sum_{j=1}^i P_j) for paths ending in state (d, m)
        
        dp = defaultdict(int)
        dp[(0, 0)] = 1
        
        # Current sum of P_j for the base path? No, we accumulate p^P_j in the transitions.
        # Actually, dp[(d,m)] stores sum of p^(P_1 + ... + P_i).
        # At step i=1, P_1=0, sum=0, p^0=1. Correct.
        
        for i in range(N - 1):
            a_i = exponents[i]
            new_dp = defaultdict(int)
            
            # Precompute powers of p to avoid repeated pow() calls if possible, 
            # but P can be large, so we compute on the fly.
            
            for (d, m), val in dp.items():
                # Current P_i = m + d
                P_curr = m + d
                
                # Option 1: Step Up -> P_next = P_curr + a_i
                P_next_up = P_curr + a_i
                # New min is still m because P_next_up >= P_curr >= m
                d_next_up = P_next_up - m
                m_next_up = m
                
                # Multiply val by p^P_next_up
                term_up = (val * pow(p, P_next_up, MOD)) % MOD
                new_dp[(d_next_up, m_next_up)] = (new_dp[(d_next_up, m_next_up)] + term_up) % MOD
                
                # Option 2: Step Down -> P_next = P_curr - a_i
                P_next_down = P_curr - a_i
                
                if P_next_down >= m:
                    # Min doesn't change
                    d_next_down = P_next_down - m
                    m_next_down = m
                else:
                    # Min changes to P_next_down
                    d_next_down = 0
                    m_next_down = P_next_down
                
                term_down = (val * pow(p, P_next_down, MOD)) % MOD
                new_dp[(d_next_down, m_next_down)] = (new_dp[(d_next_down, m_next_down)] + term_down) % MOD
            
            dp = new_dp

        # After N-1 steps, we have states for P_N.
        # The total exponent for prime p in the score is sum_{j=1}^N e_j.
        # e_j = P_j - min_k P_k.
        # Sum e_j = (Sum P_j) - N * (min_k P_k).
        # We have stored Sum P_j in the DP values (as p^(Sum P_j)).
        # We need to multiply by p^(-N * m) for each state.
        
        prime_sum = 0
        for (d, m), val in dp.items():
            # val is p^(Sum P_j)
            # We need p^(Sum P_j - N * m) = val * p^(-N * m)
            # Since m <= 0, -N * m >= 0.
            exponent = -N * m
            factor = pow(p, exponent, MOD)
            term = (val * factor) % MOD
            prime_sum = (prime_sum + term) % MOD
            
        total_answer = (total_answer * prime_sum) % MOD

    print(total_answer)

if __name__ == '__main__':
    solve()