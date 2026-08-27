import sys

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        Q = int(next(iterator))
    except StopIteration:
        return

    # Precompute a sparse table for Range Minimum Query (RMQ)
    # We want to check if for a fixed K, 2*A[L+i] <= A[L+K+i] for all 0 <= i < K.
    # This is equivalent to A[L+K+i] - 2*A[L+i] >= 0 for all i.
    # Let B[i] = A[i] - 2*A[i-K]. This depends on K, so we can't precompute B.
    
    # Alternative approach: Binary search on K.
    # For a fixed K, we need to check if min_{0<=i<K} (A[L+K+i] - 2*A[L+i]) >= 0.
    # This is still hard because the term depends on K.
    
    # However, note that the condition 2*A[L+i] <= A[L+K+i] for all i in [0, K-1]
    # is equivalent to: for all j in [L+K, L+2K-1], A[j] >= 2*A[j-K].
    # Let's define a new array C where C[j] = A[j] - 2*A[j-K]. We need min(C[L+K...L+2K-1]) >= 0.
    # This still depends on K.
    
    # Let's use the property that the answer is the largest K such that
    # the greedy two-pointer would find K pairs.
    # The greedy two-pointer for a range [L, R] with split at M = L + (R-L+1)//2:
    # left starts at L, right starts at M.
    # If 2*A[left] <= A[right], pair, left++, right++.
    # Else, right++.
    
    # To speed this up, we can use a Segment Tree or Sparse Table to skip 'right' pointers.
    # Specifically, if 2*A[left] > A[right], we need to find the smallest right' > right such that A[right'] >= 2*A[left].
    # Since A is sorted, we can use binary search (bisect) to find the next valid right.
    # This reduces the number of iterations in the inner loop.
    
    # Precompute nothing for A, but use bisect for jumps.
    import bisect
    
    results = []
    
    for _ in range(Q):
        try:
            L = int(next(iterator))
            R = int(next(iterator))
        except StopIteration:
            break
            
        l_idx = L - 1
        r_idx = R - 1
        
        length = r_idx - l_idx + 1
        max_k = length // 2
        
        if max_k == 0:
            results.append("0")
            continue
            
        # Two-pointer greedy with binary search jumps
        left = l_idx
        # Start right pointer at the middle of the range
        right = l_idx + (length + 1) // 2
        count = 0
        
        first_half_end = l_idx + length // 2
        
        # We can only form pairs if left < first_half_end and right <= r_idx
        while left < first_half_end and right <= r_idx:
            target = 2 * A[left]
            # Find the smallest index >= right such that A[index] >= target
            # Since A is sorted, we can use bisect_left
            next_right = bisect.bisect_left(A, target, right, r_idx + 1)
            
            if next_right <= r_idx:
                # We found a valid right
                count += 1
                left += 1
                right = next_right + 1
            else:
                # No valid right found for this left, and since A is sorted, no valid right for any subsequent left either
                break
                
        results.append(str(count))

    sys.stdout.write('\n'.join(results) + '\n')

solve()