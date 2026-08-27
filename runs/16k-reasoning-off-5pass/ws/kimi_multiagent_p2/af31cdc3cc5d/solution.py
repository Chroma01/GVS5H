import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    
    # dp[i][j] = max score for subarray a[i..j] (inclusive), 0-indexed
    # Only valid when (j-i+1) is even (can be completely removed)
    dp = [[0] * n for _ in range(n)]
    
    # Fill by increasing length
    for length in range(2, n + 1, 2):  # only even lengths
        for i in range(n - length + 1):
            j = i + length - 1
            # Pair i with some k in (i+1..j), where (k-i-1) is even
            # Then [i+1..k-1] must be completely removable, and [k+1..j] must be completely removable
            best = 0
            # k must be such that k-i-1 is even, so k and i have same parity
            # Also (j-k) must be even, so j and k have same parity
            # Since length is even, i and j have opposite parity, so k exists
            for k in range(i + 1, j + 1, 2):  # step 2 to maintain parity
                left = dp[i+1][k-1] if k-1 >= i+1 else 0
                right = dp[k+1][j] if k+1 <= j else 0
                val = abs(a[i] - a[k]) + left + right
                if val > best:
                    best = val
            dp[i][j] = best
    
    # If n is even, answer is dp[0][n-1]
    # If n is odd, we need to leave one element, so answer is max over leaving each element
    if n % 2 == 0:
        print(dp[0][n-1])
    else:
        # For odd n, try leaving each element i, then we need to remove [0..i-1] and [i+1..n-1]
        # Both must have even length, which they do since n is odd.
        ans = 0
        for i in range(n):
            left = dp[0][i-1] if i > 0 else 0
            right = dp[i+1][n-1] if i < n-1 else 0
            total = left + right
            if total > ans:
                ans = total
        print(ans)

main()