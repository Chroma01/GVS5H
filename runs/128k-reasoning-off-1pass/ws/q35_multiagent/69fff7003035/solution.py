import sys

# Set recursion limit just in case, though we use iterative DP
sys.setrecursionlimit(200005)

def solve():
    # Read N from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    
    MOD = 998244353
    
    # 1. Count numbers by digit length and sum them
    # Max digits for N <= 2*10^5 is 6 (since 200000 has 6 digits)
    # cnt[L] = number of integers in [1, N] with L digits
    # sum_val[L] = sum of integers in [1, N] with L digits
    
    cnt = [0] * 7
    sum_val = [0] * 7
    
    # Helper to process a range [start, end]
    def process_range(start, end):
        if start > end:
            return
        # Count
        c = end - start + 1
        # Sum of arithmetic progression: (start + end) * count / 2
        s = (start + end) * c // 2
        return c, s

    # Determine ranges for each digit length
    # 1-digit: 1-9
    # 2-digits: 10-99
    # ...
    # 6-digits: 100000-200000 (bounded by N)
    
    for L in range(1, 7):
        start = 10**(L-1)
        end = min(N, 10**L - 1)
        if start <= N:
            c, s = process_range(start, end)
            cnt[L] = c
            sum_val[L] = s % MOD
            
    # 2. Precompute factorials and inverse factorials for combinations
    MAX_N = N + 1
    fact = [1] * MAX_N
    inv_fact = [1] * MAX_N
    
    for i in range(1, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv_fact[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for i in range(MAX_N-2, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i+1)) % MOD
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % MOD
        return (num * den) % MOD

    # 3. Precompute powers of 10
    # We need powers up to total digits, which is at most 6 * N
    # But actually, the max suffix length is total digits - 1.
    # Total digits T = sum(L * cnt[L])
    T = sum(L * cnt[L] for L in range(1, 7))
    pow10 = [1] * (T + 1)
    curr = 1
    for i in range(1, T + 1):
        curr = (curr * 10) % MOD
        pow10[i] = curr
        
    # 4. Compute C_d for each digit length d present
    # C_d = sum_{k=0}^{N-1} k! * (N-1-k)! * W_k
    # where W_k is the sum of 10^{len(S)} for all subsets S of size k from M'
    # M' is the multiset of lengths of all numbers except one of length d.
    
    # We will compute W_k using DP.
    # Groups of identical lengths: only lengths 1 to 6 have non-zero counts.
    # For a fixed d, we create a temporary count array.
    
    # To optimize, we can compute the DP for the full set M, and then "remove" one item of length d?
    # Removing from subset sum DP is tricky because the weights depend on the subset size.
    # However, since there are only 6 groups, we can just run the DP 6 times (or fewer if some counts are 0).
    # This is O(6 * N * 6) = O(N), which is fine.
    
    # Let's define a function to compute W_k for a given count array
    def compute_W_for_counts(counts, total_items):
        # counts: dict or list mapping length -> count
        # We only care about lengths that have count > 0
        # DP state: dp[j] = sum of 10^{total length} for subsets of size j
        # Initialize dp[0] = 1, others 0
        dp = [0] * (total_items + 1)
        dp[0] = 1
        
        current_max_size = 0
        
        # Iterate over each distinct length L present in the counts
        # We need to process groups. The groups are defined by the lengths L where counts[L] > 0.
        # Sort lengths to ensure deterministic order, though not strictly necessary.
        lengths_with_items = [L for L in range(1, 7) if counts[L] > 0]
        
        for L in lengths_with_items:
            C = counts[L]
            if C == 0:
                continue
            
            # We need to update dp array.
            # new_dp[j] = sum_{t=0}^{min(C, j)} dp[j-t] * nCr(C, t) * 10^{t*L}
            # We iterate backwards to use a single array or create a new one.
            # Creating a new array is safer and clearer.
            new_dp = [0] * (total_items + 1)
            
            # Optimization: The max size we can reach increases by C each time.
            # But we can just iterate up to current_max_size + C.
            next_max_size = current_max_size + C
            
            # Precompute binomial coefficients for this group size C
            # nCr(C, t) for t in 0..C
            binoms = [nCr_mod(C, t) for t in range(C + 1)]
            
            # Precompute powers 10^{t*L}
            pow10_L = [pow(10, t * L, MOD) for t in range(C + 1)]
            
            for j in range(current_max_size, -1, -1):
                if dp[j] == 0:
                    continue
                val = dp[j]
                # Try taking t items from this group
                # t can range from 0 to C, but j+t <= total_items
                max_t = min(C, total_items - j)
                
                for t in range(max_t + 1):
                    if t == 0:
                        new_dp[j] = (new_dp[j] + val) % MOD
                    else:
                        term = (val * binoms[t]) % MOD
                        term = (term * pow10_L[t]) % MOD
                        new_dp[j + t] = (new_dp[j + t] + term) % MOD
            
            dp = new_dp
            current_max_size = next_max_size
            
        return dp

    # Precompute factorials for the final sum formula
    # We need k! * (N-1-k)!
    # Let's precompute an array F where F[k] = k! * (N-1-k)!
    # Note: N-1 can be up to 2*10^5 - 1
    
    N_minus_1 = N - 1
    if N_minus_1 < 0:
        # N=0 case, though constraints say N>=1
        print(0)
        return
        
    F = [0] * (N) # Indices 0 to N-1
    for k in range(N):
        # k! * (N-1-k)!
        term1 = fact[k]
        term2 = fact[N_minus_1 - k]
        F[k] = (term1 * term2) % MOD
        
    total_sum = 0
    
    # For each digit length d that exists
    for d in range(1, 7):
        if cnt[d] == 0:
            continue
            
        # Create temporary counts for M' (remove one instance of length d)
        temp_cnt = cnt[:] # Copy list
        temp_cnt[d] -= 1
        
        # Compute W_k for this M'
        # Total items in M' is N-1
        W = compute_W_for_counts(temp_cnt, N_minus_1)
        
        # Compute C_d = sum_{k=0}^{N-1} F[k] * W[k]
        C_d = 0
        for k in range(N):
            if W[k] == 0:
                continue
            term = (F[k] * W[k]) % MOD
            C_d = (C_d + term) % MOD
            
        # Add contribution of all numbers with length d
        # Contribution = sum_val[d] * C_d
        if sum_val[d] > 0:
            contrib = (sum_val[d] * C_d) % MOD
            total_sum = (total_sum + contrib) % MOD
            
    print(total_sum)

solve()