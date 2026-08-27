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
    
    # If the length difference is already greater than K, it's impossible
    if abs(n - m) > K:
        print("No")
        return
    
    # We use a banded DP approach.
    # dp[i][j] = minimum edit distance between S[:i] and T[:j]
    # We only compute for j in [max(0, i-K), min(m, i+K)]
    # To save space, we use two rows: prev_row and curr_row
    
    # We'll use a dictionary or an array with offset for the band.
    # Since the band width is at most 2*K+1, we can use an array of size 2*K+2 for each row.
    # Let's map j to an index in the array: idx = j - (i - K)
    # The valid j range for row i is [max(0, i-K), min(m, i+K)]
    # The offset for row i is max(0, i-K)
    
    # However, a simpler way with fixed size arrays:
    # For each i, we compute values for j from max(0, i-K) to min(m, i+K).
    # We can store these in a list/array where index corresponds to j.
    # But since j varies, let's use a dictionary for the previous row and build the current row.
    # Or better, use two arrays of size m+1, but only iterate the band.
    # Given m can be 500,000, allocating two arrays of size 500,001 is fine (about 4MB each).
    
    # Let's use two arrays: dp_prev and dp_curr of size m+1
    # Initialize dp_prev for i=0
    # dp_prev[j] = j for j in [0, min(m, K)] because for i=0, j can be at most K (since |0-j|<=K)
    # Actually, for i=0, j ranges from 0 to min(m, K). But we need to be careful:
    # The band condition is |i - j| <= K. For i=0, j in [0, K].
    
    # Initialize previous row
    # We only need to store values for j in the band. But for simplicity and speed,
    # let's allocate full arrays and only iterate the band.
    
    INF = K + 2
    
    dp_prev = [INF] * (m + 1)
    dp_curr = [INF] * (m + 1)
    
    # Base case: i = 0
    # dp[0][j] = j, but capped at INF
    for j in range(min(m, K) + 1):
        dp_prev[j] = j
        
    # For i from 1 to n
    for i in range(1, n + 1):
        # Determine the range of j for this i
        # j must satisfy: |i - j| <= K  =>  i - K <= j <= i + K
        # Also 0 <= j <= m
        j_start = max(0, i - K)
        j_end = min(m, i + K)
        
        # Initialize the current row's band with INF
        # We only need to set the band, but for safety, let's just compute the band
        # and leave others as INF (they won't be accessed if we're careful)
        
        # For j in the band, compute dp_curr[j]
        for j in range(j_start, j_end + 1):
            if S[i-1] == T[j-1]:
                # If characters match, no operation needed for this position
                # dp[i][j] = dp[i-1][j-1]
                # We need to access dp_prev[j-1]. Note: j-1 might be out of the previous band?
                # But if j is in [i-K, i+K], then j-1 is in [i-K-1, i+K-1].
                # The previous row i-1 had band [i-1-K, i-1+K] = [i-K-1, i+K-1].
                # So j-1 is always in the previous band. Good.
                val = dp_prev[j-1]
            else:
                # dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                # dp[i-1][j]: previous row, same j. j is in [i-K, i+K].
                #   Previous band: [i-K-1, i+K-1]. j is in this range? 
                #   j >= i-K >= i-K-1, and j <= i+K. But i+K might be > i+K-1.
                #   So if j == i+K, then j is NOT in the previous band (since prev band ends at i+K-1).
                #   In that case, dp_prev[j] should be INF (or we didn't compute it).
                #   Let's ensure we handle this.
                
                # dp[i][j-1]: current row, previous j. j-1 is in [i-K-1, i+K-1].
                #   If j-1 < j_start_prev for row i? No, we're computing in order.
                #   But j-1 might be outside the current band if j = j_start.
                #   If j = j_start, then j-1 = i-K-1. The current band starts at i-K.
                #   So dp_curr[j-1] would be INF (not computed). This is correct because
                #   transforming S[:i] to T[:i-K-1] requires at least K+1 deletions, so > K.
                
                # dp[i-1][j-1]: previous row, j-1. As argued, j-1 is in previous band.
                
                v1 = dp_prev[j] if j <= i + K - 1 else INF
                v2 = dp_curr[j-1] if j-1 >= j_start else INF
                v3 = dp_prev[j-1]
                
                val = 1 + min(v1, v2, v3)
            
            if val > INF:
                val = INF
            dp_curr[j] = val
            
        # Copy current row to previous row for next iteration
        # We only need to copy the band, but for simplicity, we can swap references
        # and re-allocate or just copy the relevant part.
        # To avoid O(m) copy, we can just swap references and re-allocate the new row.
        # But we need to ensure the new row has INF in the right places.
        # Let's just swap and then set the new row's band to INF before next use?
        # Actually, we can just swap and then in the next iteration, we overwrite the band.
        # But we must ensure that values outside the band are not used.
        # Since we only access dp_prev[j], dp_prev[j-1], dp_curr[j-1] within the band,
        # and we set dp_curr[j] for j in the band, it should be fine.
        # However, dp_prev might have old values outside the new band.
        # But we only access dp_prev[j] for j in the current band, which was in the previous band.
        # So it's safe.
        
        dp_prev, dp_curr = dp_curr, dp_prev
        
    # After the loop, dp_prev holds the values for i = n
    # We want dp[n][m]
    result = dp_prev[m]
    
    if result <= K:
        print("Yes")
    else:
        print("No")

solve()