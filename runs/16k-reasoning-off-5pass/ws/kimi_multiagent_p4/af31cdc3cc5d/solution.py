import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    a = list(map(int, input_data[1:1+n]))
    
    # dp[i] = max score for prefix a[0..i-1]
    # We compute max weight non-crossing matching where matched pairs (i,j) must have j-i odd
    # (so that the number of elements between them is even and can be completely removed)
    # dp[i+1] = max(dp[i], max over valid j of dp[j] + |a[i] - a[j]|)
    # where valid j means j < i and (i - j) is odd (different parity)
    
    dp = [0] * (n + 1)
    
    # Maintain four running maxima:
    # For each parity p (0=even, 1=odd), track:
    #   max_plus[p] = max(dp[j] + a[j]) for j with parity p
    #   max_minus[p] = max(dp[j] - a[j]) for j with parity p
    # This allows O(1) computation of max(dp[j] + |a[i] - a[j]|) over all j of given parity
    
    INF = float('inf')
    max_plus = [-INF, -INF]   # max_plus[parity]
    max_minus = [-INF, -INF]  # max_minus[parity]
    
    for i in range(n):
        # Option 1: skip a[i], carry forward dp[i]
        best = dp[i]
        
        # Option 2: pair a[i] with some previous a[j] where j has different parity
        # If i is even (0-indexed), j must be odd, and vice versa
        p = i & 1
        q = 1 - p  # required parity of j
        
        if max_plus[q] != -INF:
            # |a[i] - a[j]| = max(a[i] - a[j], a[j] - a[i])
            # Case 1: a[i] >= a[j], so |a[i] - a[j]| = a[i] - a[j]
            #   dp[j] + (a[i] - a[j]) = (dp[j] - a[j]) + a[i]
            candidate1 = max_minus[q] + a[i]
            # Case 2: a[j] >= a[i], so |a[i] - a[j]| = a[j] - a[i]
            #   dp[j] + (a[j] - a[i]) = (dp[j] + a[j]) - a[i]
            candidate2 = max_plus[q] - a[i]
            best = max(best, candidate1, candidate2)
        
        dp[i+1] = best
        
        # Update the max structures with current i as potential j for future positions
        if dp[i] + a[i] > max_plus[p]:
            max_plus[p] = dp[i] + a[i]
        if dp[i] - a[i] > max_minus[p]:
            max_minus[p] = dp[i] - a[i]
    
    print(dp[n])

if __name__ == "__main__":
    solve()