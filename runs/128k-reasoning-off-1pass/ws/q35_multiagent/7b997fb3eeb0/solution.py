import sys

def solve():
    # Increase recursion depth just in case, though not needed here
    sys.setrecursionlimit(2000)
    
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
        
    results = []
    
    for _ in range(Q):
        L = int(next(iterator))
        R = int(next(iterator))
        
        # Convert 1-based indexing to 0-based
        l_idx = L - 1
        r_idx = R - 1
        
        # The subarray is A[l_idx ... r_idx]
        # Split point
        mid_idx = (l_idx + r_idx) // 2
        
        # Left part: A[l_idx ... mid_idx]
        # Right part: A[mid_idx+1 ... r_idx]
        
        len_left = mid_idx - l_idx + 1
        len_right = r_idx - mid_idx
        
        max_k = min(len_left, len_right)
        
        if max_k == 0:
            results.append("0")
            continue
            
        # We want to find the largest K in [0, max_k] such that
        # for all i in [0, K-1], A[mid_idx + 1 + i] >= 2 * A[l_idx + i]
        # This is equivalent to finding the first i in [0, max_k-1] where
        # A[mid_idx + 1 + i] < 2 * A[l_idx + i].
        # Let this first failure index be i_fail. Then K = i_fail.
        # If no failure, K = max_k.
        
        # Binary search for the first failure index in range [0, max_k]
        low = 0
        high = max_k
        
        while low < high:
            mid_bs = (low + high) // 2
            # Check if index mid_bs is a failure
            # Left element: A[l_idx + mid_bs]
            # Right element: A[mid_idx + 1 + mid_bs]
            left_val = A[l_idx + mid_bs]
            right_val = A[mid_idx + 1 + mid_bs]
            
            if right_val < 2 * left_val:
                # This index fails, so the first failure is at or before mid_bs
                high = mid_bs
            else:
                # This index is valid, so the first failure is after mid_bs
                low = mid_bs + 1
                
        # low is now the first failure index, or max_k if no failure
        results.append(str(low))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()