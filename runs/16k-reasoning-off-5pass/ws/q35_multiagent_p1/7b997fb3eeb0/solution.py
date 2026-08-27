import sys
from bisect import bisect_left

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    A = []
    for _ in range(N):
        A.append(int(next(iterator)))
    
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        L = int(next(iterator))
        R = int(next(iterator))
        queries.append((L, R))
        
    # Convert to 0-indexed
    # A is 0-indexed, so A[i] corresponds to the (i+1)-th mochi
    # Query L, R are 1-indexed, so we use A[L-1:R]
    
    results = []
    
    for L, R in queries:
        # 0-indexed range [l, r]
        l = L - 1
        r = R - 1
        length = r - l + 1
        
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
                
            # Check if mid pairs are possible
            # We need to match A[l], A[l+1], ..., A[l+mid-1]
            # with A[r-mid+1], A[r-mid+2], ..., A[r]
            # such that A[l+i] <= A[r-mid+1+i] / 2 for all 0 <= i < mid
            
            possible = True
            # Check the condition for all i in [0, mid-1]
            # To optimize, we can break early
            for i in range(mid):
                if 2 * A[l + i] > A[r - mid + 1 + i]:
                    possible = False
                    break
            
            if possible:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
                
        results.append(ans)
        
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()