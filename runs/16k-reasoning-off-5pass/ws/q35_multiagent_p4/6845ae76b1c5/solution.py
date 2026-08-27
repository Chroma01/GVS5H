import sys
from bisect import bisect_right

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    N = int(next(iterator))
    A = [int(next(iterator)) for _ in range(N)]
    B = [int(next(iterator)) for _ in range(N)]
    K = int(next(iterator))
    
    queries = []
    for _ in range(K):
        X = int(next(iterator))
        Y = int(next(iterator))
        queries.append((X, Y))
    
    # Sort A and B
    A.sort()
    B.sort()
    
    # Precompute prefix sums for A and B
    # prefix_A[i] = sum of A[0] to A[i-1]
    prefix_A = [0] * (N + 1)
    for i in range(N):
        prefix_A[i + 1] = prefix_A[i] + A[i]
        
    prefix_B = [0] * (N + 1)
    for i in range(N):
        prefix_B[i + 1] = prefix_B[i] + B[i]
    
    results = []
    
    for X_k, Y_k in queries:
        # We need to compute sum_{i=0}^{X_k-1} sum_{j=0}^{Y_k-1} |A[i] - B[j]|
        # Using two pointers on sorted A[0..X_k-1] and B[0..Y_k-1]
        
        # For each A[i], find how many B[j] <= A[i] in B[0..Y_k-1]
        # Let idx = bisect_right(B, A[i], 0, Y_k)
        # Then for A[i]:
        #   count_le = idx, sum_le = prefix_B[idx]
        #   count_gt = Y_k - idx, sum_gt = prefix_B[Y_k] - prefix_B[idx]
        #   contribution = count_le * A[i] - sum_le + sum_gt - count_gt * A[i]
        
        # To optimize, we can iterate over the smaller array and binary search on the larger
        # But let's use two pointers for O(X_k + Y_k) per query
        
        # Two pointer approach:
        # i for A, j for B
        # We want to compute sum |A[i] - B[j]| for i in [0, X_k-1], j in [0, Y_k-1]
        
        # Alternative: For each A[i], use bisect to find split in B[0..Y_k-1]
        # This is O(X_k log Y_k) per query. Let's try this first as it's easier to implement efficiently.
        
        total = 0
        sum_B_all = prefix_B[Y_k]
        
        for i in range(X_k):
            a_val = A[i]
            # Find how many B[j] <= a_val in B[0..Y_k-1]
            idx = bisect_right(B, a_val, 0, Y_k)
            
            count_le = idx
            sum_le = prefix_B[idx]
            count_gt = Y_k - idx
            sum_gt = sum_B_all - sum_le
            
            total += count_le * a_val - sum_le + sum_gt - count_gt * a_val
            
        results.append(total)
    
    for res in results:
        print(res)

solve()