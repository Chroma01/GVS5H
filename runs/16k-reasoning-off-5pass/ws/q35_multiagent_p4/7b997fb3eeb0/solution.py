import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
        
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            L = int(next(iterator))
            R = int(next(iterator))
            queries.append((L, R))
    except StopIteration:
        return

    # Precompute nothing, use binary search for each query
    # A is 0-indexed in our list, but queries are 1-indexed.
    # Subarray for query (L, R) is A[L-1 : R]
    
    results = []
    
    for L, R in queries:
        # Subarray indices in 0-based: start = L-1, end = R-1
        # Length of subarray
        length = R - L + 1
        if length < 2:
            results.append(0)
            continue
            
        # Binary search for the maximum K
        # K can range from 0 to length // 2
        low = 0
        high = length // 2
        ans = 0
        
        while low <= high:
            mid = (low + high) // 2
            if mid == 0:
                # 0 pairs is always possible
                ans = max(ans, mid)
                low = mid + 1
                continue
            
            # Check if mid pairs can be formed
            # We need to pair A[L-1 + i] with A[R-1 - mid + i] for i in 0..mid-1
            # Condition: A[L-1 + i] <= A[R-1 - mid + i] / 2
            # i.e., 2 * A[L-1 + i] <= A[R-1 - mid + i]
            
            possible = True
            # The first part of the subarray: indices L-1 to L-1+mid-1
            # The second part of the subarray: indices R-mid to R-1
            # We pair index (L-1+i) with (R-mid+i)
            
            start_first = L - 1
            start_second = R - mid
            
            # Check all mid pairs
            for i in range(mid):
                if 2 * A[start_first + i] > A[start_second + i]:
                    possible = False
                    break
            
            if possible:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        results.append(ans)
        
    # Print all results
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()