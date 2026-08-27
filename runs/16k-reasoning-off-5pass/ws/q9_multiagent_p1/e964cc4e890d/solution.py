import sys

# Increase recursion depth just in case
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    
    MOD = 998244353
    
    # Precompute factorials
    fact = [1] * (N + 1)
    for i in range(2, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    # Precompute inverse factorials for combinations
    inv = [1] * (N + 1)
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    # Identify segments where prefix balance is 0
    # We scan S and track balance (W=+1, B=-1)
    # A segment ends at index i if balance becomes 0.
    # We only care about segments strictly between 0 and 2N.
    # The last index 2N is always 0.
    
    balance = 0
    segments = [] # List of sizes n_j (number of W in each segment)
    current_start = 0
    
    for i in range(2 * N):
        if S[i] == 'W':
            balance += 1
        else:
            balance -= 1
        
        if balance == 0:
            # Segment from current_start to i (inclusive)
            # Length is i - current_start + 1
            # Number of W (and B) in this segment is (i - current_start + 1) // 2
            seg_len = i - current_start + 1
            n_j = seg_len // 2
            if n_j > 0:
                segments.append(n_j)
            current_start = i + 1
            
    # If no segments found (impossible since total W=N, B=N), handle gracefully
    if not segments:
        print(0)
        return

    # Separate segments into those with size 1 and those with size > 1
    ones = []
    others = []
    
    for x in segments:
        if x == 1:
            ones.append(x)
        else:
            others.append(x)
            
    num_ones = len(ones)
    sum_others = sum(others)
    limit_k = N - sum_others
    
    # Initialize dp with the contribution of 'ones'
    # The polynomial for ones is (1 - x)^num_ones
    # Coefficient of x^k is C(num_ones, k) * (-1)^k
    current_dp = [0] * (limit_k + 1)
    
    for k in range(limit_k + 1):
        if k <= num_ones:
            val = nCr_mod(num_ones, k)
            if k % 2 == 1:
                val = (MOD - val) % MOD
            current_dp[k] = val
        else:
            current_dp[k] = 0
            
    # Convolve with 'others' using knapsack-like DP
    # For each x in others, the term is (1 - x! * x^x)
    # Update: dp[k] = dp[k] - dp[k-x] * x!
    
    for x in others:
        term = fact[x]
        # Update dp in reverse to avoid using updated values from current item
        for k in range(limit_k, x - 1, -1):
            val = (current_dp[k-x] * term) % MOD
            current_dp[k] = (current_dp[k] - val + MOD) % MOD
            
    # Final answer calculation
    ans = 0
    for k in range(limit_k + 1):
        # Term: current_dp[k] * (N - k)!
        ways = (current_dp[k] * fact[N - k]) % MOD
        ans = (ans + ways) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()