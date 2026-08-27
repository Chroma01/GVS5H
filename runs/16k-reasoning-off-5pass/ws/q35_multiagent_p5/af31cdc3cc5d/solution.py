import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    # dp[i][j] = maximum score for subarray a[i..j]
    # We use a 2D array for memoization
    # Initialize with -1 to indicate uncomputed states
    dp = [[-1] * n for _ in range(n)]
    
    def get_dp(i, j):
        if i >= j:
            return 0
        if dp[i][j] != -1:
            return dp[i][j]
        
        # Option 1: Skip a[i] (leave it unpaired in this subarray)
        # This is valid because the subarray might have odd length
        res = get_dp(i + 1, j)
        
        # Option 2: Pair a[i] with a[k] where k = i+1, i+3, ..., j
        # The number of elements between i and k must be even (so k - i is odd)
        for k in range(i + 1, j + 1, 2):
            # Pair a[i] and a[k]
            # Score from this pair: |a[i] - a[k]|
            # Plus score from inner subarray a[i+1..k-1]
            # Plus score from outer subarray a[k+1..j]
            current = abs(a[i] - a[k]) + get_dp(i + 1, k - 1) + get_dp(k + 1, j)
            if current > res:
                res = current
        
        dp[i][j] = res
        return res
    
    result = get_dp(0, n - 1)
    print(result)

if __name__ == '__main__':
    solve()