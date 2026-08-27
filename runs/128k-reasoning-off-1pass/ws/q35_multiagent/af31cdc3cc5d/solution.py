import sys

def solve():
    # Increase recursion depth just in case, though we will use iterative DP
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
        
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    # DP[i][0]: Max score for prefix A[0...i] where A[i] is available (not removed)
    # DP[i][1]: Max score for prefix A[0...i] where A[i] is removed (paired)
    
    # Initialize DP table
    # We use -1e18 for negative infinity to represent invalid states
    NEG_INF = -10**18
    
    # dp0[i] corresponds to DP[i][0]
    # dp1[i] corresponds to DP[i][1]
    
    dp0 = [NEG_INF] * N
    dp1 = [NEG_INF] * N
    
    # Base cases
    # For i=0: A[0] is available, score 0. A[0] cannot be removed.
    dp0[0] = 0
    dp1[0] = NEG_INF
    
    if N > 1:
        # For i=1:
        # dp0[1]: A[1] is available. A[0] could be available or removed.
        # If A[0] available: score 0.
        # If A[0] removed: impossible (cannot remove single element).
        # So dp0[1] = max(dp0[0], dp1[0]) = max(0, NEG_INF) = 0
        dp0[1] = max(dp0[0], dp1[0])
        
        # dp1[1]: A[1] is removed. Must be paired with A[0].
        # Score = dp0[-1] + |A[1]-A[0]|. dp0[-1] is 0 (empty prefix).
        dp1[1] = 0 + abs(A[1] - A[0])
        
    for i in range(2, N):
        # Transition for dp0[i]: A[i] is available
        # This means A[i] is not paired with A[i-1].
        # A[i-1] could have been available or removed.
        # In either case, the max score is the max of the previous states.
        dp0[i] = max(dp0[i-1], dp1[i-1])
        
        # Transition for dp1[i]: A[i] is removed
        # This means A[i] is paired with A[i-1].
        # The score is the max score for prefix i-2 plus |A[i] - A[i-1]|.
        # Prefix i-2 can end with A[i-2] available or removed.
        prev_max = max(dp0[i-2], dp1[i-2])
        if prev_max != NEG_INF:
            dp1[i] = prev_max + abs(A[i] - A[i-1])
        else:
            dp1[i] = NEG_INF
            
    # Final answer
    if N % 2 == 0:
        # All elements must be removed, so A[N-1] must be removed.
        ans = dp1[N-1]
    else:
        # One element remains. It could be A[N-1] (available) or some earlier element (A[N-1] removed).
        ans = max(dp0[N-1], dp1[N-1])
        
    print(ans)

if __name__ == '__main__':
    solve()