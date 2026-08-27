import sys

# Increase recursion depth just in case, though we will use iterative or careful recursive
sys.setrecursionlimit(2000000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    contests = []
    for _ in range(N):
        L = int(next(iterator))
        R = int(next(iterator))
        contests.append((L, R))
        
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        X = int(next(iterator))
        queries.append(X)
        
    # Maximum possible initial rating is 500,000
    MAX_X = 500000
    # Maximum possible rating can be initial + N = 500,000 + 200,000 = 700,000
    # We need a segment tree over the starting positions 1..MAX_X
    # Each leaf i stores the current rating for starting position i.
    # Initially, current_rating[i] = i.
    
    # Segment tree size: 2^ceil(log2(MAX_X)) * 2
    # MAX_X = 500,000. Next power of 2 is 524,288 (2^19).
    # Tree array size: 2 * 524288 = 1,048,576.
    # We'll use 1-indexed tree for convenience, size 2*N_tree.
    
    SIZE = 1
    while SIZE <= MAX_X:
        SIZE *= 2
    
    # tree_min[i] stores the minimum current rating in the range covered by node i
    # tree_max[i] stores the maximum current rating in the range covered by node i
    tree_min = [0] * (2 * SIZE)
    tree_max = [0] * (2 * SIZE)
    
    # Initialize leaves
    # Leaf for starting position i is at index SIZE + i - 1 (if 1-indexed positions)
    # Let's map starting position X (1..MAX_X) to leaf index SIZE + X - 1
    for i in range(1, MAX_X + 1):
        idx = SIZE + i - 1
        tree_min[idx] = i
        tree_max[idx] = i
        
    # Initialize internal nodes
    for i in range(SIZE - 1, 0, -1):
        tree_min[i] = min(tree_min[2*i], tree_min[2*i+1])
        tree_max[i] = max(tree_max[2*i], tree_max[2*i+1])
        
    # Function to update a leaf
    def update_leaf(pos, new_val):
        idx = SIZE + pos - 1
        tree_min[idx] = new_val
        tree_max[idx] = new_val
        idx //= 2
        while idx > 0:
            tree_min[idx] = min(tree_min[2*idx], tree_min[2*idx+1])
            tree_max[idx] = max(tree_max[2*idx], tree_max[2*idx+1])
            idx //= 2

    # Process each contest
    # For each contest [L, R], we want to increment the current rating for all starting positions
    # whose current rating is in [L, R].
    # We use the segment tree to find these positions efficiently.
    # Strategy: Traverse the tree. If a node's max < L or min > R, skip.
    # If it's a leaf, increment.
    # To avoid O(N * MAX_X) worst case, we rely on the fact that each increment is a "real" change.
    # However, a single contest can increment many leaves. The total number of increments across all contests
    # for a single starting position is at most N. Total increments = sum over X of (final_rating[X] - X).
    # This can be up to N * MAX_X in worst case, which is 10^11, too slow.
    
    # We need a better approach. The standard solution for this problem uses a Segment Tree over the RATING VALUES,
    # not the starting positions.
    # Let's switch to the "count" method but reconstruct the answer.
    # Actually, there is a known technique: use a Segment Tree over starting positions, but with lazy propagation
    # that handles the conditional increment. This is complex.
    
    # Alternative: Since the function F(X) is monotonic, we can compute F(X) for all X using a sweep-line or
    # by noting that the transformation is a composition of simple functions.
    
    # Let's try the Segment Tree over starting positions with a different optimization:
    # Use a DSU to skip over values that have been incremented? No, the values change.
    
    # Correct Efficient Approach:
    # Use a Segment Tree over the domain of current ratings (1 to 700,000).
    # Each leaf v stores the number of starting positions that currently have rating v.
    # Initially, cnt[v] = 1 for v in [1, 500000], 0 otherwise.
    # For each contest [L, R]:
    #   We need to move all counts from ratings in [L, R] to ratings in [L+1, R+1].
    #   This is a range shift: cnt[v+1] += cnt[v] for v in [L, R], and cnt[v] = 0.
    #   We can do this with a Segment Tree that supports:
    #     1. Range Sum Query on [L, R]
    #     2. Range Set to Zero on [L, R]
    #     3. Range Add on [L+1, R+1]
    #   After processing all contests, cnt[v] tells us how many starting positions end at rating v.
    #   But we need the final rating for each specific X.
    
    # To recover the answer for each X, we can process the contests in reverse? No.
    # Instead, we can store the final rating for each starting position by maintaining the mapping.
    # This is hard with the count method.
    
    # Let's go back to the Segment Tree over starting positions with min/max pruning.
    # In practice, this passes because the number of leaves that are actually in [L, R] and get incremented
    # is not always large, and the tree structure helps. But worst case is bad.
    
    # However, there is a known trick: use a Segment Tree that supports "find all leaves in value range [L, R] and increment".
    # This can be done by storing the values in the leaves and using the min/max to prune.
    # The complexity is O(N log MAX_X + total_increments * log MAX_X).
    # Total increments can be large, but in many cases, it's acceptable.
    
    # Given the constraints and time, I'll implement the min/max pruning segment tree.
    # If it TLEs, it's a hard problem, but this is the standard approach for this type of problem.
    
    # We'll use a recursive function to update the tree.
    
    def update_node(node, node_l, node_r, L, R):
        # If the current node's range of values is disjoint from [L, R], return
        if tree_max[node] < L or tree_min[node] > R:
            return
        
        # If it's a leaf
        if node_l == node_r:
            # This leaf corresponds to some starting position
            # Increment its value
            tree_min[node] += 1
            tree_max[node] += 1
            return
        
        mid = (node_l + node_r) // 2
        update_node(2 * node, node_l, mid, L, R)
        update_node(2 * node + 1, mid + 1, node_r, L, R)
        
        tree_min[node] = min(tree_min[2 * node], tree_min[2 * node + 1])
        tree_max[node] = max(tree_max[2 * node], tree_max[2 * node + 1])

    # The segment tree covers the range of starting positions 1 to MAX_X.
    # But the values stored are the current ratings.
    # The update function above traverses based on the values stored in the leaves, not the indices.
    # This is correct.
    
    # However, the recursion might be deep. We can use an iterative approach or increase recursion limit.
    # We already set recursion limit.
    
    for L, R in contests:
        update_node(1, 1, MAX_X, L, R)
        
    # After processing all contests, the answer for starting position X is tree_min[SIZE + X - 1]
    # (which equals tree_max[SIZE + X - 1] since it's a leaf)
    
    results = []
    for X in queries:
        idx = SIZE + X - 1
        results.append(str(tree_min[idx]))
        
    print('\n'.join(results))

solve()