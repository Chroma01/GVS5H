import sys

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    K = int(input_data[0])
    S = input_data[1]
    T = input_data[2]
    
    # Optimization: iterate over the shorter string to minimize band width iterations
    if len(S) > len(T):
        S, T = T, S
        
    n, m = len(S), len(T)
    
    # If the length difference is greater than K, it's impossible to match within K operations
    if abs(n - m) > K:
        print("No")
        return

    INF = K + 2
    # dp[j] stores the edit distance between S[0..i-1] and T[0..j]
    # Initialize for i=0: distance is just j (insertions)
    dp = list(range(m + 1))
    new_dp = [0] * (m + 1)
    
    for i in range(1, n + 1):
        # We only need to compute dp[j] where |i - j| <= K
        # This restricts j to [max(1, i-K), min(m, i+K)]
        start_j = max(1, i - K)
        end_j = min(m, i + K)
        
        # Handle j=0 separately to avoid index issues with T[j-1]
        if i <= K:
            new_dp[0] = i
        else:
            new_dp[0] = INF
            
        if start_j <= end_j:
            # prev_diag stores dp[j-1] from the previous row (i-1)
            prev_diag = dp[start_j - 1]
            
            for j in range(start_j, end_j + 1):
                temp = dp[j]  # Save dp[j] from previous row for next iteration's diagonal
                cost = 0 if S[i-1] == T[j-1] else 1
                
                # dp[j] is from previous row (delete from S)
                # new_dp[j-1] is from current row (insert into S)
                # prev_diag is dp[j-1] from previous row (match/replace)
                v1 = dp[j] + 1
                v2 = new_dp[j-1] + 1
                v3 = prev_diag + cost
                
                if v1 < v2:
                    new_dp[j] = v1 if v1 < v3 else v3
                else:
                    new_dp[j] = v2 if v2 < v3 else v3
                    
                prev_diag = temp
            
        # Swap arrays for next iteration. new_dp becomes the old dp array for reuse.
        dp, new_dp = new_dp, dp
        
    if dp[m] <= K:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()