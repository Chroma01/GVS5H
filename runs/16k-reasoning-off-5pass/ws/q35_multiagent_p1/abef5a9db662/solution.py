import sys

# Increase recursion depth just in case, though we'll use iterative or limited recursion
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
        queries.append(int(next(iterator)))
        
    # Maximum possible rating we need to consider.
    # Initial X <= 500,000. Max increments = N = 200,000.
    # So max rating can be 700,000. But queries are only for X <= 500,000.
    # We need to track current ratings for initial X in [1, 500000].
    # The current rating can go up to 500000 + 200000 = 700000.
    
    MAX_X = 500000
    MAX_RATING = 700005
    
    # Segment Tree to manage current ratings for each initial X.
    # Each leaf i (0-indexed, representing initial rating i+1) stores the current rating.
    # We need to support: for a contest [L, R], find all leaves with value in [L, R] and increment them.
    # Optimization: Use a segment tree where each node stores min_val and max_val in its range.
    # If max_val < L or min_val > R, skip.
    # If min_val >= L and max_val <= R, apply lazy increment to the whole node.
    # Otherwise, recurse.
    
    # Size of segment tree: power of 2 >= MAX_X
    size = 1
    while size <= MAX_X:
        size *= 2
    
    # Tree arrays
    # tree_min[v], tree_max[v] for node v
    # lazy[v] for lazy propagation
    tree_min = [0] * (2 * size)
    tree_max = [0] * (2 * size)
    lazy = [0] * (2 * size)
    
    # Initialize leaves
    # Leaf i corresponds to initial rating i+1.
    # Initial current rating for initial X is X.
    for i in range(MAX_X):
        tree_min[size + i] = i + 1
        tree_max[size + i] = i + 1
        
    # Build the tree
    for i in range(size - 1, 0, -1):
        tree_min[i] = min(tree_min[2*i], tree_min[2*i+1])
        tree_max[i] = max(tree_max[2*i], tree_max[2*i+1])
        
    def push(v):
        if lazy[v] != 0:
            lz = lazy[v]
            for node in [2*v, 2*v+1]:
                tree_min[node] += lz
                tree_max[node] += lz
                lazy[node] += lz
            lazy[v] = 0
            
    def update_node(v):
        tree_min[v] = min(tree_min[2*v], tree_min[2*v+1])
        tree_max[v] = max(tree_max[2*v], tree_max[2*v+1])
        
    # We will process each contest.
    # For each contest [L, R], we want to increment all leaves with current rating in [L, R].
    # We use a recursive function that visits nodes.
    
    # To avoid deep recursion and overhead, we can use an iterative approach or ensure recursion is efficient.
    # Given N=2e5, and each leaf incremented at most N times, but the structure prunes heavily, it should be fine.
    # However, worst-case might be tricky. Let's use a recursive function with pruning.
    
    def apply_range(v, l, r, ql, qr):
        """
        Apply increment to all leaves in range [ql, qr] (in terms of initial X index)
        that have current rating in [L, R] (global condition).
        Wait, the condition is on current rating, not on initial X index.
        This is the key difficulty. The standard segment tree range update is on indices.
        Here, we want to update indices i where tree_min/max indicates current rating is in [L, R].
        But the current rating is stored in the leaf. The condition is:
        Find all i in [0, MAX_X-1] such that current_rating[i] in [L, R].
        This is NOT a contiguous range of indices i.
        
        So the standard "range update on indices" doesn't directly apply.
        We need to find all leaves with value in [L, R] and increment them.
        This is a "value range query" on the segment tree.
        
        Algorithm for "increment all leaves with value in [L, R]":
        1. Start at root.
        2. If node's max_val < L or min_val > R, return (no leaves in this node have value in [L, R]).
        3. If node is a leaf:
             Increment its value.
             Update min/max.
             Return.
        4. If node's min_val >= L and max_val <= R:
             This means ALL leaves in this node have value in [L, R].
             Apply lazy increment to this node.
             Return.
        5. Otherwise, recurse left and right.
        
        This works because the values in a node are not necessarily contiguous, but if the entire range of values [min, max] is within [L, R], then all leaves are in [L, R].
        If the range [min, max] overlaps [L, R] but is not contained, we must recurse.
        
        Complexity: Each leaf is incremented at most N times. Each increment might cause O(log MAX_X) work if we visit the leaf.
        However, when we do a lazy update on a node, we don't visit its children.
        The number of nodes visited per contest is bounded by O(log MAX_X + number of leaves updated).
        Total complexity: O(N * log(MAX_X) + total_increments * log(MAX_X)).
        Total increments is at most N * MAX_X, which is too big.
        
        Wait, total increments is sum over all contests of (number of people who get incremented).
        In worst case, all 500,000 people get incremented in each of 200,000 contests.
        That's 10^11 operations. This approach is too slow.
        
        We need a better approach.
        
        Let's go back to the DSU / next pointer idea, but correctly.
        We want to compute final_rating[X] for each X.
        final_rating[X] = X + total_increments[X].
        
        Alternative Insight:
        Let f(X) be the final rating for initial X.
        f(X) = X + sum_{i=1}^N I(L_i <= rating_i(X) <= R_i)
        
        Notice that rating_i(X) is non-decreasing in X.
        So the set of X that get incremented in contest i is an interval (possibly empty).
        Let S_i be the set of X such that rating_i(X) in [L_i, R_i].
        Since rating_i(X) is non-decreasing, S_i is an interval [a_i, b_i].
        
        We can find a_i and b_i for each contest if we know the function rating_i(X).
        But rating_i(X) depends on previous increments.
        
        However, we can maintain the function rating_i(X) implicitly.
        Since it's non-decreasing, we can represent it by its values at key points, or use a segment tree to store the values.
        
        But we established that updating the segment tree for value ranges is slow.
        
        Let's try the DSU on "current rating values" again, but track the mapping from initial X to current rating.
        
        Actually, there is a known solution for this problem using a segment tree that stores the current rating for each initial X, and we use the "min/max" pruning to find leaves with value in [L, R].
        The key is that the total number of times we visit a leaf and increment it is exactly the total number of increments, which is at most N * MAX_X.
        But we can't afford 10^11.
        
        Wait, is the total number of increments really that large?
        In the worst case, yes. But perhaps the pruning is very effective?
        No, if all L_i=1, R_i=500000, then all leaves are updated every time.
        
        Let's reconsider the problem constraints and typical solutions.
        This is AtCoder ABC 280 F or similar? No, it's ABC 279 F?
        Actually, this is a classic problem.
        
        Correct efficient approach:
        Use a segment tree where each leaf stores the current rating.
        But instead of updating by value range, we note that the function g(X) = current_rating(X) is piecewise linear or has few changes?
        No, it's just non-decreasing.
        
        Another idea:
        Process contests in reverse? No.
        
        Let's use the fact that the answer for X is X + count of i such that L_i <= X + inc_before_i(X) <= R_i.
        
        Let's define h_i(X) = X + inc_before_i(X).
        h_1(X) = X.
        h_{i+1}(X) = h_i(X) + 1 if L_i <= h_i(X) <= R_i, else h_i(X).
        
        We want to compute h_{N+1}(X) for all X.
        
        We can use a segment tree to store h_i(X) for all X.
        For contest i, we want to find all X such that h_i(X) in [L_i, R_i] and increment h_i(X).
        This is the same problem.
        
        However, note that h_i(X) is non-decreasing.
        So the set of X such that h_i(X) in [L_i, R_i] is an interval [A_i, B_i].
        We can find A_i and B_i by binary search on the segment tree!
        
        Algorithm:
        1. Maintain a segment tree storing h(X) for all X. Initially h(X) = X.
        2. For each contest [L, R]:
           a. Find the smallest X such that h(X) >= L. Call it A.
           b. Find the largest X such that h(X) <= R. Call it B.
           c. If A <= B, then for all X in [A, B], h(X) increases by 1.
           d. Update the segment tree: add 1 to h(X) for X in [A, B].
           
        This works because h(X) is non-decreasing.
        The set {X : L <= h(X) <= R} is exactly [A, B] where A = min{X : h(X) >= L} and B = max{X : h(X) <= R}.
        
        Steps for finding A and B:
        - To find A: Find the first leaf with value >= L.
          We can do this by walking down the segment tree.
          Start at root. If left child's max < L, go right. Else go left.
          This finds the first leaf with value >= L.
        - To find B: Find the last leaf with value <= R.
          Start at root. If right child's min > R, go left. Else go right.
          This finds the last leaf with value <= R.
          
        Then we do a range update [A, B] with +1.
        
        Complexity:
        - Finding A: O(log MAX_X)
        - Finding B: O(log MAX_X)
        - Range update: O(log MAX_X)
        - Total per contest: O(log MAX_X)
        - Total for N contests: O(N log MAX_X)
        - Final query: O(1) per query after O(MAX_X) build.
        
        This is efficient!
        
        Implementation details:
        - Segment tree size: 2 * size, where size is power of 2 >= MAX_X.
        - Each node stores min_val and max_val.
        - Lazy propagation for range add.
        
        Let's implement this.
        """
        pass
    except StopIteration:
        pass

    # Re-implementing the correct solution inside the function
    size = 1
    while size <= MAX_X:
        size *= 2
    
    tree_min = [0] * (2 * size)
    tree_max = [0] * (2 * size)
    lazy = [0] * (2 * size)
    
    # Initialize leaves
    for i in range(MAX_X):
        tree_min[size + i] = i + 1
        tree_max[size + i] = i + 1
        
    # Build
    for i in range(size - 1, 0, -1):
        tree_min[i] = min(tree_min[2*i], tree_min[2*i+1])
        tree_max[i] = max(tree_max[2*i], tree_max[2*i+1])
        
    def push(v):
        if lazy[v] != 0:
            lz = lazy[v]
            for node in [2*v, 2*v+1]:
                tree_min[node] += lz
                tree_max[node] += lz
                lazy[node] += lz
            lazy[v] = 0
            
    def update_node(v):
        tree_min[v] = min(tree_min[2*v], tree_min[2*v+1])
        tree_max[v] = max(tree_max[2*v], tree_max[2*v+1])
        
    def range_add(v, l, r, ql, qr, val):
        """
        Add val to all leaves in index range [ql, qr].
        v: current node index
        l, r: current node covers index range [l, r)
        """
        if ql >= r or qr <= l:
            return
        if ql <= l and r <= qr:
            tree_min[v] += val
            tree_max[v] += val
            lazy[v] += val
            return
        
        push(v)
        mid = (l + r) // 2
        range_add(2*v, l, mid, ql, qr, val)
        range_add(2*v+1, mid, r, ql, qr, val)
        update_node(v)
        
    def find_first_ge(v, l, r, val):
        """
        Find the smallest index i in [0, MAX_X) such that tree value at i >= val.
        Returns index or MAX_X if not found.
        """
        if tree_max[v] < val:
            return MAX_X
        if l + 1 == r:
            return l - 1 # 0-indexed, leaf index is l-1? No.
            # Let's say leaf i is at index size+i.
            # Node v covers [l, r) in terms of leaf indices.
            # If leaf, l == r-1.
            return l
        
        push(v)
        mid = (l + r) // 2
        if tree_min[2*v] >= val:
            return find_first_ge(2*v, l, mid, val)
        elif tree_max[2*v] >= val:
            return find_first_ge(2*v, l, mid, val)
        else:
            return find_first_ge(2*v+1, mid, r, val)
            
    def find_last_le(v, l, r, val):
        """
        Find the largest index i in [0, MAX_X) such that tree value at i <= val.
        Returns index or -1 if not found.
        """
        if tree_min[v] > val:
            return -1
        if l + 1 == r:
            return l
            
        push(v)
        mid = (l + r) // 2
        if tree_max[2*v+1] <= val:
            return find_last_le(2*v+1, mid, r, val)
        elif tree_min[2*v] <= val:
            return find_last_le(2*v, l, mid, val)
        else:
            return find_last_le(2*v, l, mid, val)

    # Process contests
    for L, R in contests:
        # Find A: first X such that h(X) >= L
        # Our leaves are 0 to MAX_X-1, representing initial X = 1 to MAX_X.
        # Leaf i corresponds to initial X = i+1.
        # We want to find index i in [0, MAX_X-1] such that h(i+1) >= L.
        
        # find_first_ge returns the leaf index in [0, size-1).
        # We only care about [0, MAX_X-1].
        idx_a = find_first_ge(1, 0, size, L)
        if idx_a >= MAX_X:
            continue
            
        # Find B: last X such that h(X) <= R
        idx_b = find_last_le(1, 0, size, R)
        if idx_b < 0:
            continue
            
        if idx_a <= idx_b:
            # Range update on indices [idx_a, idx_b]
            range_add(1, 0, size, idx_a, idx_b + 1, 1)
            
    # Extract results
    # For each initial X, final rating is h(X).
    # We need to query the leaf for each X.
    # But we have lazy values. We can push all down or query individually.
    # Since we need all values, we can do a final push down or just query.
    
    results = []
    for x in queries:
        # Initial X is x. Leaf index is x-1.
        idx = x - 1
        # Query leaf idx
        # We can just traverse down to the leaf, pushing lazy.
        v = 1
        l, r = 0, size
        path = []
        while l + 1 < r:
            path.append(v)
            push(v)
            mid = (l + r) // 2
            if idx < mid:
                v = 2*v
                r = mid
            else:
                v = 2*v+1
                l = mid
        
        # Now v is the leaf
        final_rating = tree_min[v] # or tree_max[v], they are same for leaf
        results.append(str(final_rating))
        
    print('\n'.join(results))

solve()