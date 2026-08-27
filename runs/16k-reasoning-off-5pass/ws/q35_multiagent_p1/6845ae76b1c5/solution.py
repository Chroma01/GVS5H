import sys
from bisect import bisect_right

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    N = int(next(iterator))
    A = [int(next(iterator)) for _ in range(N)]
    B = [int(next(iterator)) for _ in range(N)]
    K = int(next(iterator))
    
    queries = []
    for _ in range(K):
        X = int(next(iterator))
        Y = int(next(iterator))
        queries.append((X, Y))
    
    # Sort A and B to enable efficient prefix sum calculations
    A.sort()
    B.sort()
    
    # Precompute prefix sums for sorted A and sorted B
    # prefix_A[i] = sum of A[0]...A[i-1]
    prefix_A = [0] * (N + 1)
    for i in range(N):
        prefix_A[i+1] = prefix_A[i] + A[i]
        
    prefix_B = [0] * (N + 1)
    for i in range(N):
        prefix_B[i+1] = prefix_B[i] + B[i]
        
    results = []
    
    for X, Y in queries:
        # We need to compute sum_{i=0}^{X-1} sum_{j=0}^{Y-1} |A[i] - B[j]|
        # A_part = A[0:X], B_part = B[0:Y]
        # Since A and B are sorted, A_part and B_part are sorted.
        
        # Use two-pointer approach
        # For each A[i], find how many B[j] <= A[i]
        # Let pos be the number of elements in B[0:Y] that are <= A[i]
        # Then sum for A[i] is:
        #   A[i] * pos - sum(B[0:pos]) + sum(B[pos:Y]) - A[i] * (Y - pos)
        #   = A[i] * (2*pos - Y) + (prefix_B[Y] - 2*prefix_B[pos])
        
        total_sum = 0
        pos = 0  # pointer in B for elements <= A[i]
        
        # Iterate through A[0:X]
        for i in range(X):
            val = A[i]
            # Advance pos while B[pos] <= val and pos < Y
            while pos < Y and B[pos] <= val:
                pos += 1
            
            # Now pos is the count of elements in B[0:Y] that are <= val
            # sum of B[0:pos] is prefix_B[pos]
            # sum of B[pos:Y] is prefix_B[Y] - prefix_B[pos]
            
            term1 = val * pos
            term2 = prefix_B[pos]
            term3 = prefix_B[Y] - prefix_B[pos]
            term4 = val * (Y - pos)
            
            total_sum += term1 - term2 + term3 - term4
            
        results.append(total_sum)
        
    for res in results:
        print(res)

solve()