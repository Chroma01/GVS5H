import sys
from bisect import bisect_right

def solve():
    # Increase recursion depth just in case, though we use iterative segment tree
    sys.setrecursionlimit(200000)
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
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
        
    # Coordinate compression for values in A
    # We need to map values to ranks for the segment tree
    unique_vals = sorted(list(set(A)))
    val_to_rank = {val: i + 1 for i, val in enumerate(unique_vals)}
    max_rank = len(unique_vals)
    
    # Segment tree for range maximum query
    # Size should be power of 2 for simplicity, or just 2*max_rank
    size = 1
    while size <= max_rank:
        size *= 2
        
    tree = [0] * (2 * size)
    
    def update(pos, value):
        """Update the value at pos (1-indexed rank) with max(current, value)"""
        idx = pos + size - 1
        if tree[idx] >= value:
            return
        tree[idx] = value
        idx //= 2
        while idx > 0:
            new_val = max(tree[2 * idx], tree[2 * idx + 1])
            if tree[idx] == new_val:
                break
            tree[idx] = new_val
            idx //= 1
            
    def query(l, r):
        """Query max in range [l, r] (1-indexed ranks)"""
        if l > r:
            return 0
        # Clamp to valid range
        if l < 1:
            l = 1
        if r > max_rank:
            r = max_rank
        if l > r:
            return 0
            
        l += size - 1
        r += size - 1
        res = 0
        while l <= r:
            if l % 2 == 1:
                if tree[l] > res:
                    res = tree[l]
                l += 1
            if r % 2 == 0:
                if tree[r] > res:
                    res = tree[r]
                r -= 1
            l //= 2
            r //= 2
        return res

    # Group queries by R
    queries_by_r = [[] for _ in range(N + 1)]
    for R, X, idx in queries:
        queries_by_r[R].append((X, idx))
        
    answers = [0] * Q
    
    # Process elements one by one
    for i in range(N):
        val = A[i]
        rank = val_to_rank[val]
        
        # Find the longest increasing subsequence ending with a value < val
        # This corresponds to query in range [1, rank - 1]
        prev_len = query(1, rank - 1)
        new_len = prev_len + 1
        
        # Update the segment tree at position 'rank' with new_len
        update(rank, new_len)
        
        # Answer all queries with R = i + 1
        for X, q_idx in queries_by_r[i + 1]:
            # We need max LIS length with values <= X
            # Find the largest rank such that unique_vals[rank-1] <= X
            # bisect_right returns insertion point, so index-1 is the last element <= X
            # unique_vals is 0-indexed, ranks are 1-indexed
            # bisect_right returns k such that all unique_vals[:k] <= X
            # So the rank corresponding to the largest value <= X is k
            k = bisect_right(unique_vals, X)
            if k == 0:
                ans = 0
            else:
                ans = query(1, k)
            answers[q_idx] = ans
            
    for ans in answers:
        print(ans)

solve()