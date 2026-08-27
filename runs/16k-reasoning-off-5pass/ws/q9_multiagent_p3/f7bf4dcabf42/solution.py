import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(2000)

def solve():
    # Read input from stdin
    try:
        input_data = sys.stdin.read().split()
    except Exception:
        return

    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        S = next(iterator)
    except StopIteration:
        return

    MOD = 998244353

    # Precompute next_occurrence[j][char]
    # next_occurrence[j][c] stores the smallest index p >= j such that S[p] == c
    # If no such p exists, we store N (indicating we cannot extend the prefix of length j with c)
    
    # Initialize with N
    next_occ = [[N] * 26 for _ in range(N + 1)]
    
    # Fill from right to left
    # For j = N, all are N (no characters after N)
    # For j < N, next_occ[j][c] = j if S[j] == c else next_occ[j+1][c]
    
    for j in range(N - 1, -1, -1):
        char_code = ord(S[j]) - ord('a')
        for c in range(26):
            if c == char_code:
                next_occ[j][c] = j
            else:
                next_occ[j][c] = next_occ[j+1][c]
                
    # DP State: dp[i][j] = number of strings of length i such that the longest prefix of S 
    # that is a subsequence of the string has length j.
    # i ranges from 0 to M
    # j ranges from 0 to N
    
    # Initialize
    # dp[0][0] = 1 (empty string has LCS prefix length 0)
    # All others 0
    
    dp = [[0] * (N + 1) for _ in range(M + 1)]
    dp[0][0] = 1
    
    for i in range(M):
        for j in range(N + 1):
            if dp[i][j] == 0:
                continue
            
            count = dp[i][j]
            
            # Try appending each character 'a' through 'z'
            for c in range(26):
                # Find next occurrence of character c in S starting from index j
                p = next_occ[j][c]
                
                if p == N:
                    new_j = j
                else:
                    new_j = p + 1
                
                # new_j is always in [0, N] because if p < N, then p+1 <= N
                dp[i+1][new_j] = (dp[i+1][new_j] + count) % MOD

    # The problem asks for ans_k for k=0 to N.
    # dp[M][j] is the count of strings with LCS length exactly j.
    
    ans = []
    for j in range(N + 1):
        ans.append(str(dp[M][j]))
        
    print(" ".join(ans))

if __name__ == '__main__':
    solve()