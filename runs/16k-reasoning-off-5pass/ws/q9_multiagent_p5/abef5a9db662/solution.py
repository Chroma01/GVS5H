import sys

# Increase recursion depth just in case, though we use iterative approach mostly
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        L = []
        R = []
        for _ in range(N):
            L.append(int(next(iterator)))
            R.append(int(next(iterator)))
        
        Q = int(next(iterator))
        queries = []
        for _ in range(Q):
            queries.append(int(next(iterator)))
    except StopIteration:
        return

    # Maximum possible rating value is 500,000.
    # We need to support indices up to 500,000.
    MAX_VAL = 500005
    # The segment tree will cover indices 1 to MAX_VAL-1.
    # Size of tree array: power of 2 >= MAX_VAL
    size = 1
    while size < MAX_VAL:
        size *= 2
    
    # Tree arrays
    # tree_min[v] stores the minimum value in the range covered by node v
    # tree_max[v] stores the maximum value in the range covered by node v
    # lazy[v] stores the pending addition for node v
    tree_min = [0] * (2 * size)
    tree_max = [0] * (2 * size)
    lazy = [0] * (2 * size)

    # Initialize the tree
    # Leaf nodes correspond to starting ratings 1 to MAX_VAL-1
    # Initially, rating[x] = x
    # Leaf for rating 'i' is at index 'size + i - 1'
    for i in range(1, MAX_VAL):
        tree_min[size + i - 1] = i
        tree_max[size + i - 1] = i
    
    # Build the tree
    for i in range(size - 1, 0, -1):
        tree_min[i] = min(tree_min[2 * i], tree_min[2 * i + 1])
        tree_max[i] = max(tree_max[2 * i], tree_max[2 * i + 1])

    def push(v):
        if lazy[v] != 0:
            lazy[2 * v] += lazy[v]
            lazy[2 * v + 1] += lazy[v]
            tree_min[2 * v] += lazy[v]
            tree_max[2 * v] += lazy[v]
            tree_min[2 * v + 1] += lazy[v]
            tree_max[2 * v + 1] += lazy[v]
            lazy[v] = 0

    def update_range(v, tl, tr, l, r, val):
        if l > r:
            return
        if l == tl and r == tr:
            tree_min[v] += val
            tree_max[v] += val
            lazy[v] += val
        else:
            push(v)
            tm = (tl + tr) // 2
            update_range(2 * v, tl, tm, l, min(r, tm), val)
            update_range(2 * v + 1, tm + 1, tr, max(l, tm + 1), r, val)
            tree_min[v] = min(tree_min[2 * v], tree_min[2 * v + 1])
            tree_max[v] = max(tree_max[2 * v], tree_max[2 * v + 1])

    # Iterative find_first_ge: find smallest index k such that value >= target
    def find_first_ge(target):
        # If the minimum value in the entire tree is less than target, 
        # we might still find a value >= target if the max is >= target.
        # However, since the array is sorted, if min < target, the first occurrence
        # must be somewhere. If min >= target, the first occurrence is at index 1.
        
        # Optimization: if tree_min[1] >= target, then index 1 is the answer.
        if tree_min[1] >= target:
            return 1
        
        # If tree_max[1] < target, no value is >= target.
        if tree_max[1] < target:
            return -1
            
        curr = 1
        t_start = 1
        t_end = size - 1
        
        while t_start != t_end:
            push(curr)
            tm = (t_start + t_end) // 2
            
            # Check left child range [t_start, tm]
            # Intersection with valid range [1, MAX_VAL-1]
            left_end = min(tm, MAX_VAL - 1)
            
            if left_end >= t_start:
                # Check if left child has any value >= target
                if tree_min[2 * curr] >= target:
                    curr = 2 * curr
                    t_end = tm
                else:
                    # Must go right
                    curr = 2 * curr + 1
                    t_start = tm + 1
            else:
                # Left child is completely outside valid range [1, MAX_VAL-1]
                curr = 2 * curr + 1
                t_start = tm + 1
        
        # curr is now a leaf node index in the tree array.
        # The rating value corresponding to this leaf is t_start.
        return t_start

    # Iterative find_last_le: find largest index k such that value <= target
    def find_last_le(target):
        # If max value in valid range <= target, then the last index is MAX_VAL-1.
        # We need to check the max value in [1, MAX_VAL-1].
        # Since the array is sorted, tree_max[1] is the max of [1, size-1].
        # If tree_max[1] <= target, then all valid indices are <= target.
        if tree_max[1] <= target:
            return MAX_VAL - 1
        
        # If min value in valid range > target, no value is <= target.
        if tree_min[1] > target:
            return -1
            
        curr = 1
        t_start = 1
        t_end = size - 1
        
        while t_start != t_end:
            push(curr)
            tm = (t_start + t_end) // 2
            
            # Check right child range [tm+1, t_end]
            # Intersection with valid range [1, MAX_VAL-1]
            right_start = max(tm + 1, 1)
            right_end = min(t_end, MAX_VAL - 1)
            
            if right_start <= right_end:
                # Check if right child has any value <= target
                if tree_max[2 * curr + 1] <= target:
                    curr = 2 * curr + 1
                    t_start = tm + 1
                else:
                    # Must go left
                    curr = 2 * curr
                    t_end = tm
            else:
                # Right child is completely outside valid range
                curr = 2 * curr
                t_end = tm
        
        # curr is now a leaf node index.
        # The rating value is t_start.
        return t_start

    # Process contests
    for i in range(N):
        l_val = L[i]
        r_val = R[i]
        
        # Find range [k, p] such that rating[k] >= l_val and rating[p] <= r_val
        k = find_first_ge(l_val)
        if k == -1:
            continue
        
        p = find_last_le(r_val)
        if p < k:
            continue
        
        # Update range [k, p]
        update_range(1, 1, size - 1, k, p, 1)

    # Answer queries
    results = []
    for x in queries:
        if x >= MAX_VAL:
            # Should not happen based on constraints, but handle gracefully
            results.append(x)
        else:
            # The final rating for initial rating x is stored at leaf corresponding to x
            # Leaf index in tree array: size + x - 1
            results.append(tree_min[size + x - 1])

    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()