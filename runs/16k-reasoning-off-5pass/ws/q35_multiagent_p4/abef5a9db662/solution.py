import sys

# Increase recursion depth just in case, though we'll use iterative or careful recursive
sys.setrecursionlimit(2000000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    # Max initial rating is 500,000. We need to support indices 1 to 500,000.
    MAX_X = 500000
    
    # We will use a Segment Tree with Lazy Propagation.
    # The segment tree covers the range [1, MAX_X].
    # Each leaf i stores the current rating if the initial rating was i.
    # Initially, leaf i stores i.
    # We need to support:
    # 1. Range Add: Add v to all leaves in [l, r].
    # 2. Find First Index >= val: Find smallest i such that tree[i] >= val.
    # 3. Find Last Index <= val: Find largest i such that tree[i] <= val.
    
    # Size of segment tree array: 4 * MAX_X is sufficient.
    size = 4 * (MAX_X + 1)
    tree_min = [0] * size
    tree_max = [0] * size
    lazy = [0] * size

    # Build the tree
    # Leaves are at indices corresponding to the range.
    # We'll use a standard recursive build.
    
    def build(node, start, end):
        if start == end:
            tree_min[node] = start
            tree_max[node] = start
        else:
            mid = (start + end) // 2
            left_node = 2 * node
            right_node = 2 * node + 1
            build(left_node, start, mid)
            build(right_node, mid + 1, end)
            tree_min[node] = min(tree_min[left_node], tree_min[right_node])
            tree_max[node] = max(tree_max[left_node], tree_max[right_node])

    build(1, 1, MAX_X)

    def push(node):
        if lazy[node] != 0:
            lz = lazy[node]
            left_node = 2 * node
            right_node = 2 * node + 1
            
            lazy[left_node] += lz
            tree_min[left_node] += lz
            tree_max[left_node] += lz
            
            lazy[right_node] += lz
            tree_min[right_node] += lz
            tree_max[right_node] += lz
            
            lazy[node] = 0

    def update_range(node, start, end, l, r, val):
        if l > end or r < start:
            return
        if l <= start and end <= r:
            tree_min[node] += val
            tree_max[node] += val
            lazy[node] += val
            return
        
        push(node)
        mid = (start + end) // 2
        left_node = 2 * node
        right_node = 2 * node + 1
        update_range(left_node, start, mid, l, r, val)
        update_range(right_node, mid + 1, end, l, r, val)
        
        tree_min[node] = min(tree_min[left_node], tree_min[right_node])
        tree_max[node] = max(tree_max[left_node], tree_max[right_node])

    # Find the smallest index i in [1, MAX_X] such that tree[i] >= val
    # Since the function is non-decreasing, we can descend the tree.
    def find_first_ge(node, start, end, val):
        # If the max value in this range is less than val, no solution here
        if tree_max[node] < val:
            return -1
        
        if start == end:
            return start
        
        push(node)
        mid = (start + end) // 2
        left_node = 2 * node
        right_node = 2 * node + 1
        
        # Check left child first
        if tree_max[left_node] >= val:
            res = find_first_ge(left_node, start, mid, val)
            if res != -1:
                return res
        
        # If not found in left, check right
        return find_first_ge(right_node, mid + 1, end, val)

    # Find the largest index i in [1, MAX_X] such that tree[i] <= val
    def find_last_le(node, start, end, val):
        # If the min value in this range is greater than val, no solution here
        if tree_min[node] > val:
            return -1
        
        if start == end:
            return start
        
        push(node)
        mid = (start + end) // 2
        left_node = 2 * node
        right_node = 2 * node + 1
        
        # Check right child first to find the largest index
        if tree_min[right_node] <= val:
            res = find_last_le(right_node, mid + 1, end, val)
            if res != -1:
                return res
        
        # If not found in right, check left
        return find_last_le(left_node, start, mid, val)

    # Process contests
    for _ in range(N):
        L = int(next(iterator))
        R = int(next(iterator))
        
        # Find range [A, B] of initial ratings X such that current_rating(X) is in [L, R]
        # i.e., L <= tree[X] <= R
        
        # Find first X where tree[X] >= L
        A = find_first_ge(1, 1, MAX_X, L)
        
        # Find last X where tree[X] <= R
        B = find_last_le(1, 1, MAX_X, R)
        
        if A != -1 and B != -1 and A <= B:
            update_range(1, 1, MAX_X, A, B, 1)

    # Process queries
    try:
        Q_str = next(iterator)
        Q = int(Q_str)
    except StopIteration:
        Q = 0
        
    results = []
    for _ in range(Q):
        X = int(next(iterator))
        # Query the value at leaf X
        # We can implement a point query or just use the tree structure
        # Since we have lazy propagation, we need to push down to get the correct value.
        # Alternatively, we can write a query function.
        
        # Let's write a simple point query
        def query_point(node, start, end, idx):
            if start == end:
                return tree_min[node] # tree_min == tree_max == value at leaf
            
            push(node)
            mid = (start + end) // 2
            left_node = 2 * node
            right_node = 2 * node + 1
            
            if idx <= mid:
                return query_point(left_node, start, mid, idx)
            else:
                return query_point(right_node, mid + 1, end, idx)
        
        ans = query_point(1, 1, MAX_X, X)
        results.append(str(ans))
        
    sys.stdout.write('\n'.join(results) + '\n')

solve()