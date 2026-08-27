import sys
from bisect import bisect_right

def solve():
    # Increase recursion depth just in case, though we don't use recursion
    sys.setrecursionlimit(200005)
    
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        Q = int(next(iterator))
    except StopIteration:
        return

    A = []
    for _ in range(N):
        A.append(int(next(iterator)))
        
    queries = []
    for i in range(Q):
        R = int(next(iterator))
        X = int(next(iterator))
        queries.append((R, X, i))
        
    # Coordinate compression for values in A
    unique_A = sorted(list(set(A)))
    val_to_idx = {val: i + 1 for i, val in enumerate(unique_A)}
    m = len(unique_A)
    
    # Fenwick Tree (BIT) for Range Maximum Query
    # bit[i] stores the max LIS length ending at a value with compressed index <= i
    bit = [0] * (m + 1)
    
    def update(idx, value):
        """Update the BIT at index idx with value (max operation)."""
        while idx <= m:
            if value > bit[idx]:
                bit[idx] = value
            idx += idx & (-idx)
            
    def query(idx):
        """Query the maximum value in the BIT from index 1 to idx."""
        res = 0
        while idx > 0:
            if bit[idx] > res:
                res = bit[idx]
            idx -= idx & (-idx)
        return res

    # Sort queries by R_i
    queries.sort(key=lambda x: x[0])
    
    answers = [0] * Q
    
    # Process elements and queries
    query_idx = 0
    num_queries = len(queries)
    
    for i in range(1, N + 1):
        val = A[i-1]
        compressed_val = val_to_idx[val]
        
        # Calculate LIS length ending at this element
        # We need the max LIS length ending at a value strictly less than val
        # So we query up to compressed_val - 1
        prev_max = query(compressed_val - 1)
        current_lis = prev_max + 1
        
        # Update the BIT with the new LIS length ending at val
        update(compressed_val, current_lis)
        
        # Answer all queries with R_i == i
        while query_idx < num_queries and queries[query_idx][0] == i:
            R, X, original_idx = queries[query_idx]
            
            # Find the largest compressed index corresponding to a value <= X
            # unique_A is sorted. We want the rightmost value <= X.
            # bisect_right returns the insertion point after all elements <= X.
            # So the index in unique_A is bisect_right(...) - 1.
            # The compressed index is that index + 1.
            
            pos = bisect_right(unique_A, X)
            if pos == 0:
                # No element <= X exists in the entire array A
                # But the problem guarantees X >= min(A[1..R]), so this shouldn't happen
                # unless the min is not in the prefix? No, min is over the prefix.
                # If pos == 0, it means X < min(unique_A), which contradicts the guarantee.
                ans = 0
            else:
                # The compressed index for the largest value <= X is pos
                # because unique_A[0] -> 1, ..., unique_A[pos-1] -> pos
                ans = query(pos)
                
            answers[original_idx] = ans
            query_idx += 1
            
    for ans in answers:
        print(ans)

solve()