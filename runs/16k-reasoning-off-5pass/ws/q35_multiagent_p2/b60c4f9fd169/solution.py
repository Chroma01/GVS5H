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
    
    # We'll use a DP approach with a band around the diagonal.
    # dp[j] will store the edit distance for S[0:i] and T[0:j]
    # We only compute for j in [max(0, i-K), min(m, i+K)]
    
    # Initialize the previous row (for i=0)
    # For i=0, dp[0][j] = j for j in [0, min(m, K)]
    # We'll use a dictionary or a list with offset indexing
    
    # Let's use a list for the current and previous rows.
    # The valid j range for row i is [max(0, i-K), min(m, i+K)]
    # We can use an offset: index = j - (i - K) to map to a fixed-size array of size 2K+1
    
    # Actually, let's use a simpler approach: two lists, prev_dp and curr_dp
    # prev_dp[j] corresponds to dp[i-1][j]
    # curr_dp[j] corresponds to dp[i][j]
    # But we only store values for j in the valid band.
    
    # Let's define a function to get the value from prev_dp for a given j
    # We'll store prev_dp as a dictionary or a list with offset.
    
    # Given K is small (<=20), we can use a list of size 2*K+1 for each row.
    # The offset for row i is: base_j = max(0, i - K)
    # The index in our small array for j is: j - base_j
    
    # Initialize prev_dp for i=0
    # For i=0, valid j: [0, min(m, K)]
    # dp[0][j] = j
    
    # We'll use a list `prev` where prev[idx] corresponds to j = base_j + idx
    # For i=0, base_j = 0, so prev[idx] = idx for idx in [0, min(m, K)]
    
    # Let's use a more straightforward implementation with two arrays of size 2*K+2
    
    # prev_dp will store values for the previous row i-1
    # curr_dp will store values for the current row i
    
    # The valid j range for row i is [max(0, i-K), min(m, i+K)]
    # Let's define a helper to get the index in our small array
    
    # Initialize prev_dp for i=0
    # base_j for i=0 is max(0, 0-K) = 0
    # We need to store j from 0 to min(m, K)
    
    # Let's use a list of size 2*K+1 for each row, indexed by j - (i-K)
    # But i-K can be negative, so we use max(0, i-K) as base
    
    # Actually, let's just use a dictionary for simplicity, since the number of entries per row is small (at most 2K+1)
    
    prev_dp = {}
    
    # Initialize for i=0
    for j in range(min(m, K) + 1):
        prev_dp[j] = j
    
    for i in range(1, n + 1):
        curr_dp = {}
        # Valid j range for this i: [max(0, i-K), min(m, i+K)]
        low_j = max(0, i - K)
        high_j = min(m, i + K)
        
        for j in range(low_j, high_j + 1):
            if S[i-1] == T[j-1]:
                # If characters match, cost is same as diagonal
                if (i-1, j-1) in prev_dp:
                    curr_dp[j] = prev_dp[j-1]
                else:
                    # This should not happen if our band is correct, but handle it
                    curr_dp[j] = K + 1  # Mark as too large
            else:
                # Cost is 1 + min(delete, insert, replace)
                # delete: dp[i-1][j] -> prev_dp[j]
                # insert: dp[i][j-1] -> curr_dp[j-1]
                # replace: dp[i-1][j-1] -> prev_dp[j-1]
                
                val_delete = prev_dp.get(j, K + 1)
                val_insert = curr_dp.get(j-1, K + 1)
                val_replace = prev_dp.get(j-1, K + 1)
                
                curr_dp[j] = 1 + min(val_delete, val_insert, val_replace)
        
        # Prune: only keep values <= K in prev_dp for next iteration
        # Actually, we can just replace prev_dp with curr_dp
        prev_dp = curr_dp
        
        # Early termination: if all values in prev_dp are > K, then it's impossible
        if all(v > K for v in prev_dp.values()):
            print("No")
            return
    
    # After processing all characters of S, check if dp[n][m] <= K
    if m in prev_dp and prev_dp[m] <= K:
        print("Yes")
    else:
        print("No")

solve()