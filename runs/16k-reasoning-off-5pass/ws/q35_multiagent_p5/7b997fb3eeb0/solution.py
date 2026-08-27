import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        Q = int(next(iterator))
        
        queries = []
        for _ in range(Q):
            L = int(next(iterator))
            R = int(next(iterator))
            queries.append((L, R))
    except StopIteration:
        return

    # Precompute nothing complex, rely on binary search + linear check with early exit
    # Since A is sorted, for a query (L, R), we want max K such that:
    # A[L+K+i] >= 2 * A[L+i] for all 0 <= i < K
    # Range for K is [0, (R-L+1)//2]
    
    results = []
    
    for L, R in queries:
        # Convert to 0-based index
        l_idx = L - 1
        r_idx = R - 1
        length = r_idx - l_idx + 1
        
        if length < 2:
            results.append(0)
            continue
            
        max_k = length // 2
        
        # Binary search for the largest K
        low = 0
        high = max_k
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                # 0 pairs is always possible
                ans = max(ans, mid)
                low = mid + 1
                continue
                
            # Check if mid pairs are possible
            # We need to check A[l_idx + mid + i] >= 2 * A[l_idx + i] for i in range(mid)
            possible = True
            # Optimization: Check in chunks or just loop. 
            # In Python, a simple loop with early break is often fastest for this pattern.
            for i in range(mid):
                if A[l_idx + mid + i] < 2 * A[l_idx + i]:
                    possible = False
                    break
            
            if possible:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        results.append(ans)

    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()