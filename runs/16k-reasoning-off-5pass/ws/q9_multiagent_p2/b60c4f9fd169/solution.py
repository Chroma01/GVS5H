import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    K = int(input_data[0])
    S = input_data[1]
    T = input_data[2]

    n = len(S)
    m = len(T)

    # Fast failure check: if length difference is greater than K, impossible
    # Because each operation changes length by at most 1.
    if abs(n - m) > K:
        print("No")
        return

    # Band-limited DP
    # We only compute states (i, j) where |i - j| <= K
    # dp[j] represents the edit distance for S[0..i-1] and T[0..j-1]
    # We use a dictionary to store only the relevant j's for the current row i.
    
    # Initial state: i = 0 (empty S)
    # dp[j] = j (insert j characters)
    # We only care about j where |0 - j| <= K => j <= K.
    # Also j cannot exceed m.
    
    dp = {}
    limit_j = min(m, K)
    for j in range(limit_j + 1):
        dp[j] = j
        
    # Iterate i from 1 to n
    for i in range(1, n + 1):
        new_dp = {}
        # Range of j for current i: [max(0, i-K), min(m, i+K)]
        # We only need to compute j in this range because if |i-j| > K, 
        # the cost to reach (i, j) is at least |i-j| > K, which is > K.
        # Since we only care if the final answer is <= K, we can prune these states.
        
        start_j = max(0, i - K)
        end_j = min(m, i + K)
        
        # We need to compute new_dp[j] for j in [start_j, end_j]
        # Transitions:
        # 1. Delete from S: dp[i-1][j] + 1  -> dp[j] + 1 (from previous row)
        # 2. Insert into S: dp[i][j-1] + 1  -> new_dp[j-1] + 1 (from current row)
        # 3. Replace: dp[i-1][j-1] + cost -> dp[j-1] + cost (from previous row)
        
        # Note: For the "Insert" operation, we need new_dp[j-1]. 
        # If j-1 < start_j, then j-1 is outside the valid range for the current row i.
        # This implies |i - (j-1)| > K, so the cost to reach (i, j-1) would be > K.
        # Thus, we can treat new_dp[j-1] as infinity if j-1 < start_j.
        
        for j in range(start_j, end_j + 1):
            # Option 1: Delete from S (from dp[j])
            cost_del = float('inf')
            if j in dp:
                cost_del = dp[j] + 1
            
            # Option 2: Insert into S (from new_dp[j-1])
            cost_ins = float('inf')
            if j - 1 >= start_j: 
                if j - 1 in new_dp:
                    cost_ins = new_dp[j - 1] + 1
            
            # Option 3: Replace (from dp[j-1])
            cost_rep = float('inf')
            if j - 1 >= 0:
                if j - 1 in dp:
                    cost_rep = dp[j - 1] + (0 if S[i-1] == T[j-1] else 1)
            
            # Determine minimum cost
            res = min(cost_del, cost_ins, cost_rep)
            new_dp[j] = res
            
        dp = new_dp
        
        # Optimization: If the minimum value in the current band is already > K,
        # we can stop early because the edit distance will only increase or stay same 
        # as we extend the strings (monotonicity property of edit distance).
        # However, strictly speaking, extending S might allow matching later chars, 
        # but the cost to reach state (i, j) is the prefix cost. 
        # If min(dp.values()) > K, then any path extending from here to (n, m) 
        # will have cost >= min(dp.values()) > K.
        if not new_dp:
            break
        if min(new_dp.values()) > K:
            print("No")
            return

    # After loop, check dp[m]
    # Note: m must be in dp because we checked abs(n-m) <= K at the start.
    # If n < m, end_j for i=n is m. If n >= m, end_j is at least m (since i+K >= m).
    # So m is always computed.
    
    if m in dp:
        if dp[m] <= K:
            print("Yes")
        else:
            print("No")
    else:
        # This case should theoretically not be reached given the initial check
        print("No")

if __name__ == '__main__':
    solve()