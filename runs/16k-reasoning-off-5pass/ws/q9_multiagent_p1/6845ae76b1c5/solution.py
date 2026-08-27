import sys
from bisect import bisect_right

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        K = int(next(iterator))
        queries = []
        for _ in range(K):
            x = int(next(iterator))
            y = int(next(iterator))
            queries.append((x, y))
    except StopIteration:
        return

    # Sort A and B
    A.sort()
    B.sort()
    
    # Precompute prefix sums for A and B
    # prefA[i] stores sum of A[0]...A[i-1]
    prefA = [0] * (N + 1)
    for i in range(N):
        prefA[i+1] = prefA[i] + A[i]
        
    prefB = [0] * (N + 1)
    for i in range(N):
        prefB[i+1] = prefB[i] + B[i]
        
    # Precompute v[j] = number of elements in A strictly less than B[j]
    # This corresponds to bisect_right(A, B[j])
    # Since B is sorted, v will be non-decreasing.
    v = [0] * N
    for j in range(N):
        v[j] = bisect_right(A, B[j])
        
    # Precompute prefix sums over the array v to answer queries in O(1) after finding split point
    # We need:
    # 1. Sum of prefA[v[j]] for j in range
    # 2. Sum of B[j] * v[j] for j in range
    # 3. Sum of B[j] for j in range (for the count term)
    
    pref_v_prefA = [0] * (N + 1)
    pref_v_B_times_v = [0] * (N + 1)
    
    for j in range(N):
        # Term 1: prefA[v[j]]
        term1 = prefA[v[j]]
        pref_v_prefA[j+1] = pref_v_prefA[j] + term1
        
        # Term 2: B[j] * v[j]
        term2 = B[j] * v[j]
        pref_v_B_times_v[j+1] = pref_v_B_times_v[j] + term2

    # Process queries
    results = []
    for x, y in queries:
        # We need to sum over j from 0 to y-1 (indices in B)
        # We need to find split point k such that for j < k, v[j] < x, and for j >= k, v[j] >= x.
        # Since v is sorted, we can find the first index in v (0-based) where v[idx] >= x.
        # bisect_right(v, x-1) finds the first element > x-1, which is >= x.
        pos = bisect_right(v, x-1)
        
        # The valid indices j where v[j] < x are [0, pos-1].
        # However, we are restricted to indices < y.
        # So the range of j where v[j] < x is [0, min(pos, y) - 1].
        k = min(pos, y)
        
        # We need to compute:
        # Sum1 = sum_{j=0}^{y-1} prefA[v[j]]
        # Split into [0, k-1] and [k, y-1]
        # Part 1: sum_{j=0}^{k-1} prefA[v[j]] = pref_v_prefA[k]
        # Part 2: sum_{j=k}^{y-1} prefA[v[j]] = (y - k) * prefA[x] 
        #         (because for j >= k, v[j] >= x, so min(v[j], x) = x)
        
        sum_prefA_v = pref_v_prefA[k] + (y - k) * prefA[x]
        
        # Sum2 = sum_{j=0}^{y-1} B[j] * max(0, x - v[j])
        # Split into [0, k-1] and [k, y-1]
        # For j >= k, v[j] >= x, so max(0, x - v[j]) = 0.
        # For j < k, max(0, x - v[j]) = x - v[j].
        # So Sum2 = sum_{j=0}^{k-1} B[j] * (x - v[j])
        #         = x * sum_{j=0}^{k-1} B[j] - sum_{j=0}^{k-1} B[j]*v[j]
        #         = x * prefB[k] - pref_v_B_times_v[k]
        
        sum_B_times_v = x * prefB[k] - pref_v_B_times_v[k]
        
        # Total Sum formula derived:
        # Total = Y * S_{A, X} + X * S_{B, Y} - 2 * (sum_{j=1}^Y S_{A, min(v_j, X)} + sum_{j=1}^Y B_j * max(0, X - v_j))
        # Note: In 0-based indexing for sums, S_{A, X} corresponds to prefA[x]
        
        term1 = y * prefA[x]
        term2 = x * prefB[y]
        term3 = -2 * sum_prefA_v
        term4 = -2 * sum_B_times_v
        
        ans = term1 + term2 + term3 + term4
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()