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

    # Factorize all A_i to find all primes involved
    MAX_VAL = 1000
    primes = []
    is_prime = [True] * (MAX_VAL + 1)
    for i in range(2, MAX_VAL + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, MAX_VAL + 1, i):
                is_prime[j] = False
    
    # Collect all prime factors and their exponents for each A_i
    prime_factors = {}
    
    for val in A:
        temp = val
        for p in primes:
            if p * p > temp:
                break
            if temp % p == 0:
                cnt = 0
                while temp % p == 0:
                    cnt += 1
                    temp //= p
                if p not in prime_factors:
                    prime_factors[p] = []
                prime_factors[p].append(cnt)
        if temp > 1:
            if temp not in prime_factors:
                prime_factors[temp] = []
            prime_factors[temp].append(1)
            
    # Function to compute the sum of p^(sum x_i) for valid sequences x_i
    # Constraints: x_i + x_{i+1} >= a_i, and (x_i + x_{i+1}) % 2 == a_i % 2
    # We use DP where dp[v] is the sum of p^(sum_{j=1}^i x_j) for sequences ending with x_i = v
    # To handle the global GCD condition (min x_i = 0), we compute:
    # Ans = Total - p^N * Total_shifted
    # where Total is the sum over sequences with x_i + x_{i+1} >= a_i
    # and Total_shifted is the sum over sequences with x_i + x_{i+1} >= max(0, a_i - 2)
    
    def calc_prime_sum(p, exponents):
        n = len(exponents)
        if n == 0:
            return 1
        
        # We need to run the DP twice: once with original constraints, once with shifted constraints
        def run_dp(constraints):
            M = max(constraints) if constraints else 0
            if M == 0:
                # If all constraints are 0, then x_i + x_{i+1} >= 0 is always true.
                # Parity constraint: (x_i + x_{i+1}) % 2 == 0.
                # This means x_i and x_{i+1} have the same parity.
                # So all x_i must have the same parity.
                # Case 1: All even. Sum = sum_{k=0..inf} p^{N*k} = 1/(1-p^N)
                # Case 2: All odd. Sum = sum_{k=0..inf} p^{N*(2k+1)} = p^N/(1-p^{2N})
                # Total = 1/(1-p^N) + p^N/(1-p^{2N}) = (1+p^N)/(1-p^N)
                p_pow_n = pow(p, n, MOD)
                p_pow_2n = pow(p, 2 * n, MOD)
                inv_1p2n = pow((1 - p_pow_n + MOD) % MOD, MOD - 2, MOD)
                inv_1p2n2 = pow((1 - p_pow_2n + MOD) % MOD, MOD - 2, MOD)
                
                term1 = inv_1p2n
                term2 = (p_pow_n * inv_1p2n2) % MOD
                return (term1 + term2) % MOD

            # Precompute powers of p
            # We need p^v for v up to M.
            # Also need geometric series sums.
            
            if p == 1:
                # Should not happen for prime factors
                return 0
                
            inv_p2 = (1 - p * p % MOD + MOD) % MOD
            inv_1p2 = pow(inv_p2, MOD - 2, MOD) # 1/(1-p^2)
            
            # Initialize dp array for v in [0, M]
            # dp[v] = p^v
            dp = [pow(p, v, MOD) for v in range(M + 1)]
            
            # Compute initial S_even, S_odd (infinite sums)
            # S_even = 1/(1-p^2), S_odd = p/(1-p^2)
            S_even = inv_1p2
            S_odd = (p * inv_1p2) % MOD
            
            # Compute T_even, T_odd (tail sums for v > M)
            sum_dp_even = sum(dp[v] for v in range(M + 1) if v % 2 == 0) % MOD
            sum_dp_odd = sum(dp[v] for v in range(M + 1) if v % 2 == 1) % MOD
            
            T_even = (S_even - sum_dp_even + MOD) % MOD
            T_odd = (S_odd - sum_dp_odd + MOD) % MOD
            
            # Function to get sum_{u >= L, u%2==k} dp[u]
            def get_sum_ge(L, k):
                s = 0
                for u in range(L, M + 1):
                    if u % 2 == k:
                        s = (s + dp[u]) % MOD
                start = M + 1 + ((M + 1) % 2 != k)
                term = pow(p, start, MOD)
                tail = (term * inv_1p2) % MOD
                return (s + tail) % MOD

            for i in range(n - 1):
                a = constraints[i]
                new_dp = [0] * (M + 1)
                
                for v in range(M + 1):
                    req_parity = (a - v) % 2
                    min_u = a - v
                    if min_u < 0:
                        min_u = 0
                    
                    total_u = get_sum_ge(min_u, req_parity)
                    term = (pow(p, v, MOD) * total_u) % MOD
                    new_dp[v] = term
                
                dp = new_dp
                
                sum_dp_even = sum(dp[v] for v in range(M + 1) if v % 2 == 0) % MOD
                sum_dp_odd = sum(dp[v] for v in range(M + 1) if v % 2 == 1) % MOD
                
                Prev_S_even = (sum_dp_even + T_even) % MOD
                Prev_S_odd = (sum_dp_odd + T_odd) % MOD
                
                K_even = Prev_S_even if (a % 2 == 0) else Prev_S_odd
                K_odd = Prev_S_even if (a % 2 == 1) else Prev_S_odd
                
                if M % 2 == 0:
                    start_even = M + 2
                else:
                    start_even = M + 1
                
                sum_p_even = pow(p, start_even, MOD) * inv_1p2 % MOD
                T_even = (K_even * sum_p_even) % MOD
                
                if M % 2 == 0:
                    start_odd = M + 1
                else:
                    start_odd = M + 2
                    
                sum_p_odd = pow(p, start_odd, MOD) * inv_1p2 % MOD
                T_odd = (K_odd * sum_p_odd) % MOD
                
                S_even = (sum_dp_even + T_even) % MOD
                S_odd = (sum_dp_odd + T_odd) % MOD
            
            final_sum = (sum(dp) + T_even + T_odd) % MOD
            return final_sum

        # Calculate Total
        total = run_dp(exponents)
        
        # Calculate Total_shifted with constraints max(0, a_i - 2)
        shifted_constraints = [max(0, a - 2) for a in exponents]
        total_shifted = run_dp(shifted_constraints)
        
        # Result for this prime: Total - p^N * Total_shifted
        term = (total - pow(p, n, MOD) * total_shifted) % MOD
        return term

    total_ans = 1
    for p, exponents in prime_factors.items():
        res = calc_prime_sum(p, exponents)
        total_ans = (total_ans * res) % MOD
        
    print(total_ans)

if __name__ == '__main__':
    solve()