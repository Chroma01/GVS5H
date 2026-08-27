import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    K = int(input_data[0])
    S = input_data[1]
    T = input_data[2]
    
    n = len(S)
    m = len(T)
    
    # If the length difference is greater than K, it's impossible
    if abs(n - m) > K:
        print("No")
        return
    
    # We'll use a banded DP approach.
    # dp[j] will store the edit distance between S[0..i-1] and T[0..j-1]
    # We only need to track j values where |i - j| <= K
    
    # Initialize the previous row (for i=0)
    # For i=0, dp[0][j] = j, but we only care about j where j <= K
    # We'll use a dictionary or an array with offset for the band
    
    # Let's use an array with offset. For row i, valid j ranges from max(0, i-K) to min(m, i+K)
    # We can use a fixed-size array of size 2*K+1 for each row, with offset
    
    # prev_dp[j_offset] corresponds to j = i - K + j_offset, but we need to be careful with bounds
    
    # Actually, let's use a simpler approach: for each i, compute the current row's values
    # for j in range(max(0, i-K), min(m+1, i+K+1))
    
    # We'll store the previous row as a dictionary or list with known indices
    
    # Initialize for i=0
    # dp[0][j] = j for j in 0..min(m, K)
    prev = {}
    for j in range(min(m, K) + 1):
        prev[j] = j
    
    for i in range(1, n + 1):
        curr = {}
        # For current row i, j ranges from max(0, i-K) to min(m, i+K)
        j_start = max(0, i - K)
        j_end = min(m, i + K)
        
        for j in range(j_start, j_end + 1):
            if j == 0:
                # dp[i][0] = i
                curr[j] = i
            else:
                # Get values from previous row
                # dp[i-1][j] = prev.get(j, infinity)
                # dp[i][j-1] = curr.get(j-1, infinity)
                # dp[i-1][j-1] = prev.get(j-1, infinity)
                
                val_prev = prev.get(j, K + 1)  # If not in prev, it's > K
                val_left = curr.get(j - 1, K + 1)
                val_diag = prev.get(j - 1, K + 1)
                
                if S[i - 1] == T[j - 1]:
                    curr[j] = val_diag
                else:
                    curr[j] = 1 + min(val_diag, val_prev, val_left)
        
        # Prune: only keep values <= K for the next iteration
        # Also, for the next row i+1, we need j values where |(i+1) - j| <= K, i.e., j >= i+1-K and j <= i+1+K
        # So we can filter curr to only keep j in [max(0, i+1-K), min(m, i+1+K)]
        next_j_start = max(0, i + 1 - K)
        next_j_end = min(m, i + 1 + K)
        
        prev = {}
        for j in range(next_j_start, next_j_end + 1):
            if j in curr and curr[j] <= K:
                prev[j] = curr[j]
        
        # If prev is empty, it means no valid states, so distance > K
        if not prev:
            print("No")
            return
    
    # Check if dp[n][m] <= K
    if m in prev and prev[m] <= K:
        print("Yes")
    else:
        print("No")

solve()