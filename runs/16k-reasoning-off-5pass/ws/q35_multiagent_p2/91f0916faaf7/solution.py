import sys

# Set recursion depth just in case, though we use iterative DP
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

    # Function to get prime factorization of a number
    def get_factorization(n):
        factors = {}
        for p in primes:
            if p * p > n:
                break
            if n % p == 0:
                count = 0
                while n % p == 0:
                    count += 1
                    n //= p
                factors[p] = count
        if n > 1:
            factors[n] = 1
        return factors

    # Identify all primes involved in the input A
    prime_counts = {} # prime -> list of exponents a_i
    for x in A:
        factors = get_factorization(x)
        for p, exp in factors.items():
            if p not in prime_counts:
                prime_counts[p] = []
            prime_counts[p].append(exp)
            
    # For primes not in prime_counts, all a_i are 0.
    # If all a_i are 0, the only good sequence for that prime is e_i = 0 for all i.
    # Contribution is p^0 = 1. So we can ignore primes not in prime_counts.
    
    total_ans = 1
    
    # Precompute powers of p for DP
    # We need p^v for v up to M = sum(a_i)
    
    for p, exponents in prime_counts.items():
        # exponents is the list [a_1, a_2, ..., a_{N-1}]
        # N is the length of S, so there are N-1 constraints.
        
        M = sum(exponents)
        
        # We need to compute Total(M) and Total(M-1)
        # Total(K) is the sum of p^{sum e_i} for sequences e_1...e_N
        # such that |e_i - e_{i+1}| = a_i and 0 <= e_i <= K.
        
        def compute_total(K):
            if K < 0:
                return 0
            
            # DP[i][v] stores the sum of p^{sum_{j=1}^i e_j} for valid prefixes ending at e_i = v
            # We only need the previous row, so we can optimize space, but N=1000, M=10000 is small enough for 2D or 1D with careful updates.
            # Let's use 1D array for current row.
            
            # Current DP state: dp[v] = sum of scores for prefixes ending at value v
            # Initialize for i=1 (first element e_1)
            # e_1 can be any value in [0, K]
            # Score contribution for e_1 is p^{e_1}
            
            dp = [0] * (K + 1)
            p_pow = 1
            for v in range(K + 1):
                dp[v] = p_pow
                p_pow = (p_pow * p) % MOD
                
            # Iterate through constraints
            for a in exponents:
                new_dp = [0] * (K + 1)
                # For each current value v, it can come from v-a or v+a
                # new_dp[v] = p^v * (dp[v-a] if v>=a else 0 + dp[v+a] if v+a<=K else 0)
                
                # We can iterate v from 0 to K
                # To optimize, notice that p^v is a factor.
                
                # Precompute p^v for this step? No, we can just multiply.
                
                for v in range(K + 1):
                    val = 0
                    # From v - a
                    if v >= a:
                        val = (val + dp[v - a]) % MOD
                    # From v + a
                    if v + a <= K:
                        val = (val + dp[v + a]) % MOD
                    
                    if val > 0:
                        new_dp[v] = (val * p_pow) % MOD # Wait, p_pow here is p^v? No.
                        # We need p^v. Let's compute it inside or precompute.
                
                # Let's redo the inner loop to correctly apply p^v
                # Recompute p^v on the fly or precompute
                curr_p_pow = 1
                for v in range(K + 1):
                    val = 0
                    if v >= a:
                        val = (val + dp[v - a]) % MOD
                    if v + a <= K:
                        val = (val + dp[v + a]) % MOD
                    
                    if val > 0:
                        new_dp[v] = (val * curr_p_pow) % MOD
                    
                    curr_p_pow = (curr_p_pow * p) % MOD
                
                dp = new_dp

            return sum(dp) % MOD

        total_M = compute_total(M)
        total_M_minus_1 = compute_total(M - 1)
        
        # Ans_p = Total(M) - p^N * Total(M-1)
        p_N = pow(p, N, MOD)
        ans_p = (total_M - p_N * total_M_minus_1) % MOD
        
        total_ans = (total_ans * ans_p) % MOD

    print(total_ans)

solve()