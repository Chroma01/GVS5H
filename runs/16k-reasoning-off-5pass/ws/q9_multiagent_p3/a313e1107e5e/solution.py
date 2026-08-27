import sys
from bisect import bisect_right

# Increase recursion depth just in case, though we use iterative BIT
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
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
    # We need to map values of A to ranks 1..K
    # We also need to map X values to the largest rank <= X
    
    sorted_unique_A = sorted(list(set(A)))
    rank_map = {val: i + 1 for i, val in enumerate(sorted_unique_A)}
    K = len(sorted_unique_A)
    
    # Prepare queries for offline processing
    # Sort queries by R (prefix length)
    queries.sort(key=lambda x: x[0])
    
    # Fenwick Tree (Binary Indexed Tree) for Range Maximum Query
    # tree[i] stores the max LIS length ending with a value having rank i
    tree = [0] * (K + 1)
    
    def update(idx, val):
        # Update position idx with val (taking max)
        while idx <= K:
            if val > tree[idx]:
                tree[idx] = val
            idx += idx & (-idx)
            
    def query(idx):
        # Query max in range [1, idx]
        res = 0
        while idx > 0:
            if tree[idx] > res:
                res = tree[idx]
            idx -= idx & (-idx)
        return res

    results = [0] * Q
    
    current_R = 0
    query_idx = 0
    
    # Process elements of A one by one
    for i in range(N):
        current_R += 1
        
        val = A[i]
        r = rank_map[val]
        
        # Calculate LIS length ending at current element
        # It is 1 + max(LIS length ending with value < val)
        # Since we use ranks, we query range [1, r-1]
        prev_max = query(r - 1)
        current_len = prev_max + 1
        
        # Update the BIT at position r with current_len
        update(r, current_len)
        
        # Answer all queries that end at current_R
        while query_idx < Q and queries[query_idx][0] == current_R:
            R, X, original_idx = queries[query_idx]
            
            # Find the largest rank in sorted_unique_A that is <= X
            # bisect_right returns the insertion point after elements <= X
            # So the index returned is the count of elements <= X
            # The rank we want is that index (since ranks are 1-based)
            # Example: sorted_unique_A = [2, 4, 5], X = 4
            # bisect_right returns 2 (index of 5). Elements <= 4 are at indices 0, 1.
            # Ranks are 1, 2. We want max over ranks 1..2.
            # So we query at index = bisect_right(...)
            
            limit_rank = bisect_right(sorted_unique_A, X)
            
            # limit_rank is the number of elements <= X, which corresponds exactly to the max rank <= X
            # because ranks are 1-based indices of sorted_unique_A.
            # If limit_rank is 0, it means no element <= X exists (though problem guarantees X >= min)
            
            ans = query(limit_rank)
            results[original_idx] = ans
            
            query_idx += 1
            
    # Print results in original order
    for res in results:
        print(res)

if __name__ == '__main__':
    solve()