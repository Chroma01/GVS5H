import sys

# Increase recursion depth to handle deep recursion in segment tree if necessary
sys.setrecursionlimit(300000)

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

    # Precompute prefix distinct counts
    # prefix_distinct[i] = number of distinct elements in A[0...i-1] (0-based slice of length i)
    # This corresponds to the problem statement A[1...i] in 1-based indexing
    prefix_distinct = [0] * (N + 1)
    seen = set()
    for i in range(N):
        seen.add(A[i])
        prefix_distinct[i+1] = len(seen)

    # Precompute suffix distinct counts
    # suffix_distinct[i] = number of distinct elements in A[i...N-1]
    suffix_distinct = [0] * (N + 1)
    seen = set()
    for i in range(N - 1, -1, -1):
        seen.add(A[i])
        suffix_distinct[i] = len(seen)

    # Segment Tree for Range Add, Range Max
    # We need to support:
    # 1. Point initialization (or range set)
    # 2. Range Add
    # 3. Range Max Query
    # Indices used in the tree will correspond to k (start of middle segment)
    # k ranges from 1 to N-1. We map k -> k-1 (0 to N-2) for 0-based tree indexing.
    
    size = 1
    while size <= N:
        size *= 2
    
    tree = [0] * (2 * size)
    lazy = [0] * (2 * size)
    
    def push(node):
        if lazy[node] != 0:
            tree[2*node] += lazy[node]
            lazy[2*node] += lazy[node]
            tree[2*node+1] += lazy[node]
            lazy[2*node+1] += lazy[node]
            lazy[node] = 0

    def update_range(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            tree[node] += val
            lazy[node] += val
            return
        
        push(node)
        mid = (start + end) // 2
        update_range(2*node, start, mid, l, r, val)
        update_range(2*node+1, mid+1, end, l, r, val)
        tree[node] = max(tree[2*node], tree[2*node+1])

    def query_range(node, start, end, l, r):
        if l > end or r < start:
            return -float('inf')
        if l <= start and end <= r:
            return tree[node]
        
        push(node)
        mid = (start + end) // 2
        p1 = query_range(2*node, start, mid, l, r)
        p2 = query_range(2*node+1, mid+1, end, l, r)
        return max(p1, p2)

    # Initialize the segment tree with prefix_distinct values
    # We want tree[k-1] to store prefix_distinct[k] initially.
    # This represents the state where the middle segment is effectively "empty" or just starting.
    # However, the logic relies on the fact that when we move from j to j+1, 
    # we add 1 to the range of k where A[j] is new.
    # To make the first query (j=2) work correctly, we need the tree to represent
    # prefix_distinct[k] + distinct(A[k...1]) for j=2.
    # distinct(A[k...1]) is 1 if k=1 (since A[1] is the only element) and 0 otherwise?
    # Actually, let's stick to the invariant: tree[k] stores prefix_distinct[k+1] + distinct(A[k+1...j-1]).
    # At start (before loop), we consider a virtual j=1. Middle is A[k+1...0] which is empty.
    # So tree[k] = prefix_distinct[k+1].
    # We map k (1-based start of middle) to index k-1 in tree.
    for k in range(1, N):
        update_range(1, 0, size-1, k-1, k-1, prefix_distinct[k])
        
    ans = 0
    
    # last_pos[x] stores the last index (0-based) where value x appeared
    last_pos = [-1] * (N + 1)
    
    # Iterate j from 2 to N-1 (0-based index for start of right segment)
    # j corresponds to the split point where the right segment starts at A[j]
    # The middle segment ends at A[j-1].
    # Valid k (start of middle) are 1 to j-1.
    for j in range(2, N):
        # Query max in range [1, j-1] for k
        # Map to tree indices [0, j-2]
        if j-1 >= 1:
            res = query_range(1, 0, size-1, 0, j-2)
            if res != -float('inf'):
                # Total distinct = (distinct in Left + distinct in Middle) + distinct in Right
                # res = prefix_distinct[k] + distinct(A[k...j-1])
                # suffix_distinct[j] = distinct(A[j...N-1])
                total = res + suffix_distinct[j]
                if total > ans:
                    ans = total
        
        # Prepare for next iteration (j+1)
        # We need to update the values in the tree to reflect the addition of A[j] to the potential middle segment
        # The value g(k) = prefix_distinct[k] + distinct(A[k...j-1])
        # becomes g'(k) = prefix_distinct[k] + distinct(A[k...j])
        # distinct(A[k...j]) = distinct(A[k...j-1]) + 1 if A[j] is new in A[k...j-1]
        # A[j] is new in A[k...j-1] if and only if the last occurrence of A[j] before j is < k
        # i.e., last_pos[A[j]] < k
        
        val = A[j]
        idx = last_pos[val]
        
        # We need to add 1 to g(k) for all k such that k > idx
        # Range of k is [idx + 1, j] (since for the next step j+1, k can go up to j)
        # Map to tree indices [idx, j-1]
        
        L = idx + 1
        if L < 1: L = 1
        R = j
        
        if L <= R:
            update_range(1, 0, size-1, L-1, R-1, 1)
        
        # Update last_pos for the current element
        last_pos[val] = j

    print(ans)

if __name__ == '__main__':
    solve()