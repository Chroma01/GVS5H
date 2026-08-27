import sys

# Increase recursion depth just in case, though we are using iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

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
    # because each operation changes length by at most 1.
    if abs(n - m) > K:
        print("No")
        return

    # Band DP approach
    # We only compute the DP table within a band of width 2*K + 1 around the main diagonal.
    # dp[j] will store the edit distance between S[0...i] and T[0...j].
    # We maintain the current row and the previous row.
    
    INF = K + 1
    
    # Base case: i = 0 (S is empty)
    # dist("", T[0...j]) = j
    # We only need to store j such that |0 - j| <= K => 0 <= j <= K
    # Also bounded by m.
    prev_offset = 0
    prev_end = min(m, K)
    prev = list(range(prev_end + 1))
    
    # Iterate through each character of S
    for i in range(n):
        # We are computing row i+1 (after processing S[i])
        new_i = i + 1
        
        # Determine the range of j (indices of T) we need to compute for row new_i
        # Condition: |new_i - j| <= K  =>  new_i - K <= j <= new_i + K
        # Also 0 <= j <= m
        new_offset = max(0, new_i - K)
        new_end = min(m, new_i + K)
        new_len = new_end - new_offset + 1
        
        curr = [INF] * new_len
        
        # Previous row offset
        prev_offset = max(0, i - K)
        
        # Compute values for the current row
        for k in range(new_len):
            j = new_offset + k
            
            # Initialize cost with infinity
            cost = INF
            
            # Option 1: Delete S[i] (transition from dp[i][j])
            # Corresponds to prev[j]
            # Valid if j is within the range of the previous row
            if j >= prev_offset:
                val = prev[j - prev_offset]
                if val < cost:
                    cost = val + 1
            
            # Option 2: Insert T[j-1] (transition from dp[i+1][j-1])
            # Corresponds to curr[j-1]
            # Valid if j-1 >= new_offset => k >= 1
            if k >= 1:
                val = curr[k-1]
                if val < cost:
                    cost = val + 1
            
            # Option 3: Replace (transition from dp[i][j-1])
            # Corresponds to prev[j-1]
            # Valid if j-1 >= prev_offset
            if j - 1 >= prev_offset:
                val = prev[j - 1 - prev_offset]
                add = 0 if S[i] == T[j-1] else 1
                if val + add < cost:
                    cost = val + add
            
            # Cap the cost at INF to prevent overflow and prune
            curr[k] = cost if cost <= K else INF
        
        prev = curr
        
        # Optimization: If the minimum value in the current band exceeds K,
        # it's impossible to reach T within K operations.
        if min(prev) > K:
            print("No")
            return

    # After processing all characters of S, we are at row n.
    # We need the value for T[m] (index m).
    final_offset = max(0, n - K)
    
    # Check if m is within the computed range
    if m < final_offset:
        # This implies m < n - K => n - m > K, which was caught at the start.
        print("No")
    else:
        idx = m - final_offset
        if idx < len(prev):
            if prev[idx] <= K:
                print("Yes")
            else:
                print("No")
        else:
            # This implies m > n + K, caught at the start.
            print("No")

if __name__ == '__main__':
    solve()