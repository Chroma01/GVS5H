import sys
import bisect

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
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
            l = int(next(iterator))
            r = int(next(iterator))
            queries.append((l, r))
    except StopIteration:
        return

    # Segment Tree to manage available indices
    # We need to find the smallest available index in a range [L, R]
    # Initially, all indices 0 to N-1 are available.
    # When an index is used (paired), we mark it as unavailable (set to infinity).
    
    # Size of the segment tree
    size = 1
    while size < N + 2:
        size *= 2
    
    # Tree array. Initialize with N+1 (infinity)
    # Leaves will be at indices [size, size + N + 1]
    tree = [N + 1] * (2 * size)
    
    # Initialize leaves: tree[size + i] = i for i in 0..N-1
    # Indices N and N+1 remain N+1
    for i in range(N):
        tree[size + i] = i
    
    # Build the tree
    for i in range(size - 1, 0, -1):
        tree[i] = min(tree[2 * i], tree[2 * i + 1])
        
    def update(pos, val):
        """Update the value at position pos to val."""
        idx = size + pos
        tree[idx] = val
        idx //= 2
        while idx > 0:
            tree[idx] = min(tree[2 * idx], tree[2 * idx + 1])
            idx //= 2
            
    def query_min(l, r):
        """Query the minimum value in range [l, r]."""
        if l > r:
            return N + 1
        l += size
        r += size
        res = N + 1
        while l <= r:
            if l % 2 == 1:
                if tree[l] < res:
                    res = tree[l]
                l += 1
            if r % 2 == 0:
                if tree[r] < res:
                    res = tree[r]
                r -= 1
            l //= 2
            r //= 2
        return res

    results = []
    
    for l, r in queries:
        # Convert 1-based indexing to 0-based
        L = l - 1
        R = r - 1
        
        ans = 0
        curr_l = L
        
        # Greedy strategy:
        # Iterate through potential "top" elements starting from L.
        # For each top A[curr_l], find the smallest available "bottom" A[curr_r]
        # such that A[curr_r] >= 2 * A[curr_l] and curr_r > curr_l.
        # If found, pair them and mark curr_r as used.
        # If not found (or no valid bottom exists in the range), stop.
        
        while curr_l <= R:
            val_l = A[curr_l]
            needed = 2 * val_l
            
            # Find the first index k in [curr_l + 1, R] such that A[k] >= needed
            # bisect_left returns the first index where A[idx] >= needed
            # We restrict the search range to [curr_l + 1, R + 1] for the hi argument
            # Note: bisect_left on the whole array A with lo=curr_l+1 works correctly
            # because A is sorted.
            
            k = bisect.bisect_left(A, needed, lo=curr_l + 1, hi=R + 1)
            
            if k > R:
                # No element in the range satisfies the condition
                break
            
            # Find the smallest available index in [k, R]
            avail_idx = query_min(k, R)
            
            if avail_idx > R:
                # No available index found in the valid range
                break
            
            # Pair (curr_l, avail_idx)
            ans += 1
            # Mark avail_idx as used
            update(avail_idx, N + 1)
            
            # Move to the next potential top
            curr_l += 1
            
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()