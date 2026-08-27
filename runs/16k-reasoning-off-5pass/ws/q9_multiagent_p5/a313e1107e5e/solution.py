import sys
import bisect

# Increase recursion depth just in case, though we use iterative BIT
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        queries = []
        for i in range(Q):
            r = int(next(iterator))
            x = int(next(iterator))
            queries.append((r, x, i))
            
    except StopIteration:
        return

    # Coordinate Compression
    # We collect all unique values from A to map them to ranks [1, M]
    # This is necessary because A_i can be up to 10^9
    sorted_A = sorted(list(set(A)))
    val_map = {val: i + 1 for i, val in enumerate(sorted_A)}
    M = len(sorted_A)
    
    # Prepare queries for offline processing
    # Sort queries by R (the prefix length) in ascending order
    queries.sort(key=lambda q: q[0])
    
    # Fenwick Tree (Binary Indexed Tree) for Range Maximum Query
    # Supports: update(index, value) -> max(current, value)
    #          query(index) -> max in range [1, index]
    # Size is M + 1 because ranks are 1-based
    bit = [0] * (M + 1)
    
    def update(idx, val):
        """Update the BIT at idx with val, keeping the maximum."""
        while idx <= M:
            if val > bit[idx]:
                bit[idx] = val
            idx += idx & (-idx)
            
    def query(idx):
        """Query the maximum value in range [1, idx]."""
        res = 0
        while idx > 0:
            if bit[idx] > res:
                res = bit[idx]
            idx -= idx & (-idx)
        return res

    # Process
    results = [0] * Q
    current_r = 0
    
    # We iterate through the sorted queries.
    # For each query (r, x, original_idx), we advance current_r to r.
    # As we advance, we process elements A[0]...A[r-1] and update the BIT.
    # Note: r is 1-based index from input. A has indices 0 to N-1.
    # We need to process elements A[0]...A[r-1] (total r elements).
    
    for r, x, original_idx in queries:
        # Advance current_r to r
        while current_r < r:
            val = A[current_r]
            # Find compressed index for val
            # Since val is guaranteed to be in sorted_A (as it comes from A), we can use val_map
            c_idx = val_map[val]
            
            # Calculate LIS ending at this value
            # We need max length of increasing subsequence ending with value < val
            # In compressed space, this is query(c_idx - 1)
            prev_len = query(c_idx - 1)
            new_len = prev_len + 1
            
            # Update BIT at c_idx with new_len
            update(c_idx, new_len)
            
            current_r += 1
            
        # Now answer the query for X
        # We need max value in BIT for all compressed indices corresponding to values <= X
        # Find the largest value in sorted_A that is <= X
        # We can use bisect_right to find the insertion point
        
        idx_limit = bisect.bisect_right(sorted_A, x)
        
        # idx_limit is the count of elements <= x in sorted_A.
        # The compressed indices are 1-based, so we query up to idx_limit.
        if idx_limit > 0:
            ans = query(idx_limit)
        else:
            ans = 0
            
        results[original_idx] = ans

    # Print results in original order
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()