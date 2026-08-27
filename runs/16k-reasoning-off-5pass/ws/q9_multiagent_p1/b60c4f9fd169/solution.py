import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse inputs
    K = int(input_data[0])
    S = input_data[1]
    T = input_data[2]

    N = len(S)
    M = len(T)

    # If the length difference is greater than K, it's impossible to transform S to T
    # because each operation changes the length by at most 1.
    if abs(N - M) > K:
        print("No")
        return

    # We use a banded DP approach.
    # dp[j] represents the edit distance between S[0..i-1] and T[0..j-1].
    # We only need to maintain a window of size roughly 2*K + 1 around the diagonal.
    # The valid range for j at row i is [i - K, i + K].
    
    # We will use a 1D array to store the current row.
    # To handle the sliding window efficiently, we map the logical index j 
    # to an array index.
    # Let's define the window such that at step i, we compute values for j in [i-K, i+K].
    # We can use an offset to map j to array index.
    # Let's define `dp` array such that `dp[k]` corresponds to `T` index `j = i - K + k`.
    # So `k` ranges from 0 to 2*K.
    # When we move to i+1, the new `j` for the same `k` is `(i+1) - K + k = j + 1`.
    # So the window shifts right by 1.
    
    # Initialize for i=0 (empty prefix of S)
    # j = 0 - K + k => k = j + K.
    # We need j in [0, K] (since j < 0 is invalid, and j > K is outside band for i=0).
    # So k in [K, 2*K].
    # dp[k] = j = k - K.
    
    dp = [0] * (2 * K + 1)
    for k in range(K, 2 * K + 1):
        j = k - K
        if j <= M:
            dp[k] = j
        else:
            dp[k] = j # Just in case, though loop bounds might prevent access

    # Now loop i from 1 to N
    for i in range(1, N + 1):
        new_dp = [0] * (2 * K + 1)
        # Determine valid j range for this i
        # j_min = max(0, i - K)
        # j_max = min(M, i + K)
        # Corresponding k range:
        # k_min = j_min - (i - K)
        # k_max = j_max - (i - K)
        
        j_min = max(0, i - K)
        j_max = min(M, i + K)
        
        k_min = j_min - (i - K)
        k_max = j_max - (i - K)
        
        # We need to compute new_dp[k] for k in [k_min, k_max]
        # new_dp[k] corresponds to T index j = i - K + k
        
        # Pre-calculate character comparison to avoid repeated lookups in inner loop
        char_s = S[i-1]
        
        for k in range(k_min, k_max + 1):
            j = i - K + k
            
            # Option 1: Delete from S (from prev row, same j) -> dp[k+1]
            # In prev row (i-1), index for j is k+1
            val_del = dp[k+1] + 1
            
            # Option 2: Insert into S (from current row, j-1) -> new_dp[k-1]
            # If k-1 < k_min, this corresponds to j-1 < j_min.
            # If j=0, we are at T[0..-1]. The cost is i (delete all S).
            # However, if j=0, k = K-i. If i <= K, k >= 0.
            # If k == k_min, then j = j_min.
            # If j_min == 0, then j=0.
            # In this case, new_dp[k-1] is out of bounds (k-1 < k_min).
            # But we can derive the value: if j=0, cost is i.
            # However, val_del (from dp[i-1][0]) will be i-1 + 1 = i.
            # So val_del covers the case. We can set val_ins to infinity if k-1 < k_min.
            val_ins = float('inf')
            if k > k_min:
                val_ins = new_dp[k-1] + 1
            
            # Option 3: Replace (from prev row, j-1) -> dp[k]
            # cost = 0 if S[i-1] == T[j-1] else 1
            # Note: if j=0, T[j-1] is invalid, but j=0 case is handled by val_del usually.
            # If j > 0:
            cost = 0 if char_s == T[j-1] else 1
            val_rep = dp[k] + cost
            
            new_dp[k] = min(val_del, val_ins, val_rep)
            
            # Optimization: If the value exceeds K, we can cap it at K+1 to prevent overflow
            # and speed up comparisons, though not strictly necessary for correctness.
            if new_dp[k] > K:
                new_dp[k] = K + 1
        
        dp = new_dp
        
        # Early exit optimization: If the minimum value in the current band is > K,
        # we can stop early because the distance will only increase or stay same relative to band.
        # However, checking min() takes O(K), which is fine.
        # But we must be careful: the band might not contain the final answer yet.
        # But if min(dp) > K, then any future state reachable from here will be > K.
        # So we can break.
        # Let's check if min(dp) > K.
        # We only care about the computed part of dp.
        # The computed part is from k_min to k_max.
        # If min(new_dp[k_min : k_max+1]) > K, we can stop.
        # But wait, we need to ensure that the final answer (at i=N, j=M) is reachable.
        # If |N-M| <= K, the final answer is within the band at i=N.
        # If at any point the minimum distance in the band exceeds K, then the final distance will also exceed K.
        # So we can break.
        
        # Check min of the computed range
        current_min = min(dp[k_min : k_max+1])
        if current_min > K:
            print("No")
            return

    # After loop, check the result
    # We need dp[i][j] where i=N, j=M.
    # k = M - (N - K) = M - N + K.
    k_final = M - N + K
    if 0 <= k_final <= 2 * K:
        if dp[k_final] <= K:
            print("Yes")
        else:
            print("No")
    else:
        # Should not happen if |N-M| <= K
        print("No")

if __name__ == '__main__':
    solve()