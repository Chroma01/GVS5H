import sys

# Increase recursion depth to handle deep recursion in Segment Tree if necessary
sys.setrecursionlimit(500000)

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
    except StopIteration:
        return

    # Precompute suffix distinct counts
    # suff[k] = number of distinct integers in A[k...N-1] (0-indexed)
    suff = [0] * N
    seen = set()
    for i in range(N - 1, -1, -1):
        seen.add(A[i])
        suff[i] = len(seen)

    # Precompute next_occurrence
    # next_occ[i] = index of the next occurrence of A[i] after i
    # If no next occurrence, set to N
    next_occ = [N] * N
    last_pos = {}
    for i in range(N - 1, -1, -1):
        val = A[i]
        if val in last_pos:
            next_occ[i] = last_pos[val]
        else:
            next_occ[i] = N
        last_pos[val] = i

    # Precompute prefix distinct counts
    # pref[i] = number of distinct integers in A[0...i-1] (first i elements)
    # pref[0] = 0
    pref = [0] * (N + 1)
    seen = set()
    for i in range(N):
        seen.add(A[i])
        pref[i+1] = len(seen)

    # Segment Tree Implementation (Recursive, Range Update, Range Max)
    # We map split point j (1-based, end of middle segment) to index j-1 in the tree leaves.
    # Valid j are from 2 to N-1. So indices 1 to N-2.
    # Tree size is power of 2 >= N.
    
    size = 1
    while size <= N:
        size *= 2
    
    # Initialize tree with -1 (though we will fill valid range)
    tree = [-1] * (2 * size)
    lazy = [0] * (2 * size)

    def push(v):
        if lazy[v] != 0:
            tree[2*v] += lazy[v]
            lazy[2*v] += lazy[v]
            tree[2*v+1] += lazy[v]
            lazy[2*v+1] += lazy[v]
            lazy[v] = 0

    def update(l, r, val, v, tl, tr):
        if l > r:
            return
        if l == tl and r == tr:
            tree[v] += val
            lazy[v] += val
        else:
            push(v)
            tm = (tl + tr) // 2
            update(l, min(r, tm), 2*v, tl, tm)
            update(max(l, tm+1), r, 2*v+1, tm+1, tr)
            tree[v] = max(tree[2*v], tree[2*v+1])

    def query(l, r, v, tl, tr):
        if l > r:
            return -1
        if l == tl and r == tr:
            return tree[v]
        push(v)
        tm = (tl + tr) // 2
        return max(query(l, min(r, tm), 2*v, tl, tm), 
                   query(max(l, tm+1), r, 2*v+1, tm+1, tr))

    # Initialize the tree for i=1 (first split at index 1, i.e., after A[0])
    # Middle segment starts at index 1 (0-based).
    # We need distinct count of A[1...k] + suff[k+1] for k in [1, N-2].
    # Leaf index k corresponds to split point j = k+1.
    
    vals = [0] * N
    seen_mid = set()
    
    # k=1
    seen_mid.add(A[1])
    vals[1] = len(seen_mid) + suff[2] 
    
    for k in range(2, N-1):
        seen_mid.add(A[k])
        vals[k] = len(seen_mid) + suff[k+1]

    # Fill the segment tree leaves
    # Indices 1 to N-2
    for k in range(1, N-1):
        tree[size + k] = vals[k]
        
    # Build the tree
    for v in range(size - 1, 0, -1):
        tree[v] = max(tree[2*v], tree[2*v+1])

    ans = 0
    
    # Iterate i from 1 to N-2 (1-based index of end of first part)
    # i corresponds to index i-1 in 0-based A.
    # First part: A[0 ... i-1]
    # Middle part starts at i (0-based)
    # We need max over j in [i+1, N-1] (1-based) of (distinct(i+1, j) + suff[j+1])
    # In terms of k (end of middle segment, 0-based): k goes from i to N-2.
    # The range in tree indices is [i, N-2].
    
    for i in range(1, N-1): # i from 1 to N-2
        # Query max in [i, N-2]
        if i <= N-2:
            current_max = query(i, N-2, 1, 0, size-1)
            if current_max != -1:
                total = pref[i] + current_max
                if total > ans:
                    ans = total
        
        # Update for next iteration (i -> i+1)
        # Remove A[i-1] from the middle segment consideration.
        # The middle segment was A[i-1 ... k]. Now it becomes A[i ... k].
        # Distinct count decreases by 1 if A[i-1] does not appear in A[i ... k].
        # i.e., next_occ[i-1] > k.
        # So we decrement values for k in [i, next_occ[i-1]-1].
        
        idx = i - 1
        limit = next_occ[idx] - 1
        # Range to update: [i, limit]
        # We must ensure limit >= i. Also limit < size.
        if limit >= i:
            update(i, min(limit, size-1), -1, 1, 0, size-1)

    print(ans)

if __name__ == '__main__':
    solve()