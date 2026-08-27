import sys

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

    # Basic necessary condition: if the length difference is more than K,
    # we need at least |n - m| insertions/deletions, which is > K.
    if abs(n - m) > K:
        print("No")
        return

    # We use a banded DP approach.
    # dp[j] will store the edit distance for S[:i] and T[:j+1]
    # We only need to compute values where |i - (j+1)| <= K, i.e., |i - 1 - j| <= K
    # For row i (1-indexed, corresponding to S[0..i-1]), the valid j range (0-indexed for T)
    # is from max(0, i - 1 - K) to min(m - 1, i - 1 + K).
    # Let's use 0-indexed i for S length: i from 0 to n.
    # dp[j] corresponds to edit distance between S[:i] and T[:j+1].
    
    # Initialize dp array for i=0 (S is empty)
    # dp[j] = j (need j insertions to form T[:j+1] from empty string)
    # But we only care about j in range [0, min(m-1, K)] because if j > K, dp[j] = j > K.
    # Actually, let's just use a full array but restrict computation.
    # Since K is small, we can use a list of size m+1, but only update the band.
    
    # dp[j] = edit distance between S[:i] and T[:j]
    # Base case: i=0, dp[j] = j
    dp = list(range(m + 1))
    
    # Iterate over each character of S
    for i in range(1, n + 1):
        # Determine the valid range for j in the current row
        # We need |i - j| <= K => j >= i - K and j <= i + K
        # Also 0 <= j <= m
        j_start = max(0, i - K)
        j_end = min(m, i + K)
        
        # For j < j_start, dp[j] = i - j > K (since i - j > K), so we can ignore.
        # For j > j_end, dp[j] = j - i > K (since j - i > K), so we can ignore.
        
        # We need to compute new_dp for j in [j_start, j_end]
        # new_dp[j] depends on:
        # - delete: dp[j] + 1 (delete S[i-1])
        # - insert: new_dp[j-1] + 1 (insert T[j-1])
        # - replace/match: dp[j-1] + (0 if S[i-1] == T[j-1] else 1)
        
        # Handle boundary: new_dp[0] = i (delete all i characters of S)
        # But new_dp[0] is only valid if 0 is in [j_start, j_end]
        
        new_dp = [0] * (m + 1)
        
        # Set values outside the band to infinity (or a value > K)
        # We'll just compute the band and check min at the end.
        
        # Compute new_dp[j] for j in [j_start, j_end]
        for j in range(j_start, j_end + 1):
            if j == 0:
                new_dp[j] = i
            else:
                # delete: dp[j] + 1
                val_delete = dp[j] + 1
                # insert: new_dp[j-1] + 1
                val_insert = new_dp[j-1] + 1
                # replace/match: dp[j-1] + cost
                cost = 0 if S[i-1] == T[j-1] else 1
                val_replace = dp[j-1] + cost
                
                new_dp[j] = min(val_delete, val_insert, val_replace)
        
        # Check if all valid values in the current row exceed K
        # We only need to check the band [j_start, j_end]
        min_val = min(new_dp[j_start:j_end+1])
        if min_val > K:
            print("No")
            return
            
        dp = new_dp

    # After processing all characters of S, check if dp[m] <= K
    if dp[m] <= K:
        print("Yes")
    else:
        print("No")

solve()