import sys

def solve():
    # Increase recursion depth just in case
    sys.setrecursionlimit(300000)
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    A = []
    for _ in range(N):
        A.append(int(next(iterator)))
        
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
        
    queries = []
    for _ in range(Q):
        L = int(next(iterator))
        R = int(next(iterator))
        queries.append((L, R))
        
    # Build a Segment Tree for Range Minimum Query
    # The tree will store the minimum value in each range.
    # We need to find the smallest index i in [L, R] such that A[i] <= X.
    
    # Size of the segment tree
    size = 1
    while size < N:
        size *= 2
        
    # tree[i] stores the minimum value in the range covered by node i
    tree = [float('inf')] * (2 * size)
    
    # Build the tree
    for i in range(N):
        tree[size + i] = A[i]
    for i in range(size - 1, 0, -1):
        tree[i] = min(tree[2 * i], tree[2 * i + 1])
        
    def find_first_le_iterative(q_l, q_r, x):
        """
        Find the smallest index in [q_l, q_r] (0-indexed) such that A[index] <= x.
        """
        # First, check if any element in the range satisfies the condition using RMQ.
        l, r = q_l + size, q_r + 1 + size
        min_val = float('inf')
        while l < r:
            if l & 1:
                min_val = min(min_val, tree[l])
                l += 1
            if r & 1:
                r -= 1
                min_val = min(min_val, tree[r])
            l >>= 1
            r >>= 1
            
        if min_val > x:
            return -1
            
        # Now find the first index by descending from the root.
        node = 1
        node_l, node_r = 0, size
        
        while node_r - node_l > 1:
            mid = (node_l + node_r) // 2
            
            # Check if left child has a valid element in the query range
            # Left child covers [node_l, mid)
            # We need to check if left child overlaps with [q_l, q_r+1) and has min <= x
            
            # Overlap check: left child range [node_l, mid) overlaps with [q_l, q_r+1)
            # if not (mid <= q_l or node_l >= q_r + 1)
            if not (mid <= q_l or node_l >= q_r + 1):
                if tree[2 * node] <= x:
                    node = 2 * node
                    node_r = mid
                    continue
            
            # If left child doesn't have it, go right
            node = 2 * node + 1
            node_l = mid
            
        return node_l

    results = []
    
    for L, R in queries:
        # Convert to 0-indexed
        l_idx = L - 1
        r_idx = R - 1
        
        # Greedy simulation with optimization using Segment Tree
        left = l_idx
        right = r_idx
        count = 0
        
        while left < right:
            # We want to pair A[left] with A[right] if possible.
            # Condition: A[left] <= A[right] // 2
            # If not, we skip A[left] because it's too big for A[right] (and thus for any smaller bottom).
            # If yes, we pair them and move both pointers.
            
            # However, the optimal strategy is to match the smallest available top with the smallest valid bottom.
            # But since the array is sorted, the smallest valid bottom for A[left] is the first element >= 2*A[left].
            # But we want to maximize pairs. The standard greedy for this problem is:
            # Try to pair the smallest top with the largest bottom.
            # If A[left] <= A[right] // 2, pair them.
            # Else, A[left] is too big for A[right]. Since A[right] is the largest, A[left] can't be a top for any bottom.
            # So we discard A[left].
            
            if A[left] <= A[right] // 2:
                count += 1
                left += 1
                right -= 1
            else:
                left += 1
                
        results.append(str(count))
        
    print('\n'.join(results))

solve()