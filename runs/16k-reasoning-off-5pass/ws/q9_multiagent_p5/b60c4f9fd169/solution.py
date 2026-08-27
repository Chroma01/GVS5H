import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse inputs
    iterator = iter(input_data)
    try:
        K = int(next(iterator))
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    n = len(S)
    m = len(T)

    # If the absolute difference in lengths is greater than K, it's impossible
    # because we need at least abs(n - m) insertions/deletions.
    if abs(n - m) > K:
        print("No")
        return

    # We use a band optimization for Levenshtein distance.
    # We only compute DP states where |i - j| <= K.
    # Since K is small (<= 20), this reduces complexity from O(N*M) to O(K * min(N, M)).
    
    INF = K + 1
    offset = K
    size = 2 * K + 2
    
    # prev[j] stores the edit distance between S[0...i-1] and T[0...j-1]
    # We initialize for i=0 (empty S).
    # dp[0][j] = j (insert j characters)
    prev = [INF] * size
    
    # Fill initial row (i=0)
    # We only need to fill up to j=K because for i=0, j > K implies |0-j| > K.
    # However, to be safe with array bounds and logic, we fill the valid band for i=0.
    # Band for i=0 is [0-K, 0+K] -> [0, K] (since j>=0).
    for j in range(K + 1):
        prev[j + offset] = j
        
    # Iterate through each character of S (i from 0 to n-1)
    for i in range(n):
        curr = [INF] * size
        
        # Base case for the current row: distance to empty T prefix is i
        # This corresponds to j=0. If 0 is in range [i-K, i+K], set it.
        # Condition: |i - 0| <= K  =>  i <= K
        if i <= K:
            curr[offset] = i
        
        # Determine the range of j to compute for this row i
        # We need j such that |i - j| <= K  =>  i - K <= j <= i + K
        # Also 0 <= j <= m
        start_j = max(0, i - K)
        end_j = min(m, i + K)
        
        # We iterate j from start_j to end_j
        for j in range(start_j, end_j + 1):
            idx = j + offset
            idx_prev = j - 1 + offset
            
            # Calculate costs
            # 1. Deletion from S (move from prev[j]) -> dp[i-1][j] + 1
            cost_del = prev[idx] + 1
            
            # 2. Insertion into S (move from curr[j-1]) -> dp[i][j-1] + 1
            # If j == 0, this is invalid (handled by base case above)
            # If j > 0, we check if j-1 is within the computed band for current row i.
            # The band for row i starts at start_j. If j == start_j, then j-1 < start_j,
            # meaning dp[i][j-1] is outside the band (cost > K), so treat as INF.
            if j == 0:
                cost_ins = INF
            elif j > start_j:
                cost_ins = curr[idx - 1] + 1
            else:
                cost_ins = INF
            
            # 3. Replacement (move from prev[j-1]) -> dp[i-1][j-1] + (1 if S[i] != T[j] else 0)
            # If j == 0, this is invalid.
            if j == 0:
                cost_rep = INF
            else:
                # Check if prev[j-1] is valid.
                # For row i-1, the band was [i-1-K, i-1+K].
                # We are accessing j-1. We need |(i-1) - (j-1)| <= K => |i-j| <= K.
                # Since we are in the loop where |i-j| <= K, prev[j-1] should be valid
                # provided it was computed in the previous step.
                # However, if j-1 was outside the band of row i-1, prev[j-1] would be INF.
                # This is consistent.
                cost_rep = prev[idx_prev] + (1 if S[i] != T[j] else 0)
            
            curr[idx] = min(cost_del, cost_ins, cost_rep)
            
            # Clamp to INF if it exceeds K to keep numbers small and logic clean
            if curr[idx] > K:
                curr[idx] = INF
        
        # Update prev for the next iteration
        prev = curr

    # After processing all of S, the answer is in prev[m + offset]
    # We already checked abs(n-m) <= K at the start, so m should be within the band of row n-1.
    ans = prev[m + offset]
    
    if ans <= K:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()