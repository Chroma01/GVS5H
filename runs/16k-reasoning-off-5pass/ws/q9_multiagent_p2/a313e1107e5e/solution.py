import sys
import bisect

# Increase recursion depth just in case, though we will use iterative approaches
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
            R = int(next(iterator))
            X = int(next(iterator))
            queries.append((R, X, i))
            
    except StopIteration:
        return

    # Coordinate Compression
    # We need to map values of A to ranks.
    # The BIT will be built over the ranks of values present in A.
    # For a query with X, we need the rank of the largest value in A that is <= X.
    
    # Collect all unique values from A
    sorted_unique_A = sorted(list(set(A)))
    val_to_rank = {val: i + 1 for i, val in enumerate(sorted_unique_A)}
    num_unique = len(sorted_unique_A)
    
    # Prepare queries for offline processing
    # Sort queries by R (prefix length)
    queries.sort(key=lambda x: x[0])
    
    # Fenwick Tree (Binary Indexed Tree) for Range Maximum Query
    # bit[i] stores the max LIS length for values with rank corresponding to the range covered by i
    bit = [0] * (num_unique + 1)
    
    def update(idx, val):
        """Update the value at idx with val (maximize)."""
        while idx <= num_unique:
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

    results = [0] * Q
    current_r = 0
    
    # Process queries in increasing order of R
    for R, X, original_idx in queries:
        # Advance current_r to R
        while current_r < R:
            val = A[current_r]
            rank = val_to_rank[val]
            
            # Calculate LIS ending at this value
            # We need max LIS ending at any value < val
            # Since we are using ranks, we query for rank - 1
            prev_max = query(rank - 1)
            new_len = prev_max + 1
            
            # Update the BIT at this rank
            update(rank, new_len)
            
            current_r += 1
            
        # Answer the query
        # We need the max LIS length using values <= X
        # Find the rank of the largest value in A that is <= X
        # We can use bisect_right on sorted_unique_A to find the insertion point
        # The index returned is the count of elements <= X.
        # Since ranks are 1-based and correspond to indices in sorted_unique_A (0-based),
        # if bisect returns k, it means there are k elements <= X.
        # These elements have ranks 1 to k.
        
        idx_in_sorted = bisect.bisect_right(sorted_unique_A, X)
        
        if idx_in_sorted == 0:
            # No element in A is <= X
            results[original_idx] = 0
        else:
            # Query max in range [1, idx_in_sorted]
            results[original_idx] = query(idx_in_sorted)
            
    # Print results in original order
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()