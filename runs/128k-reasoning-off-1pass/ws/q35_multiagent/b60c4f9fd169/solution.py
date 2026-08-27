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
    
    # If the length difference is already greater than K, it's impossible
    # because we need at least |n-m| insertions/deletions.
    if abs(n - m) > K:
        print("No")
        return
    
    # We use a 1D DP array to save space.
    # dp[j] will store the edit distance between S[0:i] and T[0:j]
    # We iterate i from 0 to n.
    
    # Initialize dp array for i=0 (empty S)
    # dp[j] = j (need j insertions to form T[0:j] from empty string)
    # But we cap values at K+1 to avoid overflow and unnecessary computation
    INF = K + 1
    dp = [j if j <= K else INF for j in range(m + 1)]
    
    for i in range(1, n + 1):
        # Create a new row for the current i
        new_dp = [INF] * (m + 1)
        
        # The range of j we need to consider is [max(0, i-K), min(m, i+K)]
        # Because if |i-j| > K, the edit distance will be > K.
        start_j = max(0, i - K)
        end_j = min(m, i + K)
        
        # Handle the first element of the row (j=0) if it's in range
        if start_j == 0:
            new_dp[0] = i
            if new_dp[0] > K:
                new_dp[0] = INF
        
        # Fill the band
        for j in range(start_j, end_j + 1):
            if i == 1 and j == 0:
                # Already handled above
                continue
                
            cost = 0 if S[i-1] == T[j-1] else 1
            
            # new_dp[j] = min(
            #     new_dp[j-1] + 1,      # Insertion (into S to match T[j])
            #     dp[j] + 1,            # Deletion from S
            #     dp[j-1] + cost        # Substitution/Match
            # )
            
            # We can compute these values carefully
            val_ins = new_dp[j-1] + 1 if j > 0 else INF
            val_del = dp[j] + 1
            val_sub = dp[j-1] + cost if j > 0 else INF
            
            min_val = val_ins
            if val_del < min_val:
                min_val = val_del
            if val_sub < min_val:
                min_val = val_sub
                
            if min_val > K:
                new_dp[j] = INF
            else:
                new_dp[j] = min_val
                
        dp = new_dp
        
        # Early termination: if all values in the current row are > K, we can stop
        # Since we capped at INF, we can check if the minimum in the relevant band is INF
        # But checking the whole row is O(m) which is too slow.
        # Instead, we can just let it run. The band is small.
        # However, we can check if the minimum value in the computed band is > K.
        # Since we only compute a band of size at most 2K+1, this check is cheap.
        if all(v == INF for v in dp[start_j:end_j+1]):
            print("No")
            return

    # The answer is dp[m]
    if dp[m] <= K:
        print("Yes")
    else:
        print("No")

solve()