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

    # Precompute primes up to 1000
    primes = []
    is_prime = [True] * 1001
    for i in range(2, 1001):
        if is_prime[i]:
            primes.append(i)
            for j in range(i*i, 1001, i):
                is_prime[j] = False
    
    # Identify which primes are relevant (divide at least one A_i)
    relevant_primes = set()
    for x in A:
        temp = x
        for p in primes:
            if p * p > temp:
                break
            if temp % p == 0:
                relevant_primes.add(p)
                while temp % p == 0:
                    temp //= p
        if temp > 1:
            relevant_primes.add(temp)
            
    # Precompute transitions for each prime
    # prime_transitions[p][i] will be a list of possible x values for A[i]
    prime_transitions = {p: [] for p in relevant_primes}
    
    for i in range(N - 1):
        val = A[i]
        # Factorize val
        temp = val
        factors = {}
        for p in primes:
            if p * p > temp:
                break
            if temp % p == 0:
                cnt = 0
                while temp % p == 0:
                    cnt += 1
                    temp //= p
                factors[p] = cnt
        if temp > 1:
            factors[temp] = 1
            
        # For each relevant prime p, find possible x = v_p(Q) - v_p(P)
        # If p divides val with exponent k, then x can be k or -k.
        # If p does not divide val, x is 0.
        
        for p in relevant_primes:
            if p in factors:
                k = factors[p]
                prime_transitions[p].append([k, -k])
            else:
                prime_transitions[p].append([0])

    total_score = 1
    
    # DP for each prime
    for p in relevant_primes:
        # Determine range
        max_exp = 0
        for x in A:
            temp = x
            while temp % p == 0:
                max_exp += 1
                temp //= p
        # Max sum is (N-1) * max_exp
        limit = (N - 1) * max_exp
        offset = limit + 100
        
        # Initialize DP
        size = 2 * limit + 200
        dp = [0] * size
        dp[offset] = 1
        
        # Precompute powers of p is not strictly necessary if we use pow(p, exp, MOD)
        # but we need to handle negative exponents via modulo arithmetic.
        # We will compute term % (MOD-1) and use pow(p, term_mod, MOD).
        
        MOD_EXP = MOD - 1
        
        # Use a list of active states to optimize
        active_states = [offset]
        
        for i in range(N - 1):
            next_dp = [0] * size
            next_active = set()
            
            trans = prime_transitions[p][i]
            
            for s in active_states:
                if dp[s] == 0:
                    continue
                val = dp[s]
                
                for x in trans:
                    s_prime = s + x
                    if s_prime < 0 or s_prime >= size:
                        continue
                    
                    # Calculate term
                    # Linear part: (N - (i+1)) * x
                    # Count part: N * I(s_prime < 0)
                    
                    term = (N - 1 - i) * x
                    if s_prime < 0:
                        term += N
                    
                    # Compute factor
                    term_mod = term % (MOD_EXP)
                    factor = pow(p, term_mod, MOD)
                    
                    new_val = (val * factor) % MOD
                    next_dp[s_prime] = (next_dp[s_prime] + new_val) % MOD
                    next_active.add(s_prime)
            
            dp = next_dp
            active_states = list(next_active)
            
        # Sum up the results
        total_score = (total_score + sum(dp)) % MOD

    print(total_score)

if __name__ == '__main__':
    solve()