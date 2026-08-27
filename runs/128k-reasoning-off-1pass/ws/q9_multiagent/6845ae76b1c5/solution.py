import sys

# Increase recursion depth to handle deep segment trees if necessary
sys.setrecursionlimit(300000)

class PersistentSegmentTree:
    def __init__(self, max_val):
        # Each node stores: count, sum_val, left_child, right_child
        # We use arrays to simulate nodes for performance and memory efficiency
        self.count = [0]
        self.sum_val = [0]
        self.left = [0]
        self.right = [0]
        self.n = max_val
        self._init_root()

    def _init_root(self):
        # Create a dummy root node (index 0) representing empty range
        self.count.append(0)
        self.sum_val.append(0)
        self.left.append(0)
        self.right.append(0)

    def _new_node(self):
        idx = len(self.count)
        self.count.append(0)
        self.sum_val.append(0)
        self.left.append(0)
        self.right.append(0)
        return idx

    def update(self, prev_node, l, r, idx, val):
        """
        Creates a new version of the tree by adding 'val' at 'idx'.
        Returns the index of the new root.
        """
        new_node = self._new_node()
        self.left[new_node] = self.left[prev_node]
        self.right[new_node] = self.right[prev_node]
        
        if l == r:
            self.count[new_node] = self.count[prev_node] + 1
            self.sum_val[new_node] = self.sum_val[prev_node] + val
            return new_node
        
        mid = (l + r) // 2
        if idx <= mid:
            self.left[new_node] = self.update(self.left[prev_node], l, mid, idx, val)
        else:
            self.right[new_node] = self.update(self.right[prev_node], mid + 1, r, idx, val)
        
        self.count[new_node] = self.count[self.left[new_node]] + self.count[self.right[new_node]]
        self.sum_val[new_node] = self.sum_val[self.left[new_node]] + self.sum_val[self.right[new_node]]
        
        return new_node

    def query_sum_min(self, node, l, r, limit):
        """
        Calculates sum(min(x, limit)) for all x in the range covered by 'node'.
        """
        if node == 0:
            return 0
        
        if l >= limit:
            # All values in this range are >= limit, so min(x, limit) is limit
            return self.count[node] * limit
        
        if r <= limit:
            # All values in this range are <= limit, so min(x, limit) is x
            return self.sum_val[node]
        
        mid = (l + r) // 2
        left_res = self.query_sum_min(self.left[node], l, mid, limit)
        right_res = self.query_sum_min(self.right[node], mid + 1, r, limit)
        return left_res + right_res

    def query_sum_max(self, node, l, r, limit):
        """
        Calculates sum(max(0, x - limit)) for all x in the range covered by 'node'.
        """
        if node == 0:
            return 0
        
        if r <= limit:
            # All values are <= limit, so max(0, x - limit) is 0
            return 0
        
        if l >= limit:
            # All values are >= limit, so max(0, x - limit) is x - limit
            # Sum(x - limit) = Sum(x) - count * limit
            return self.sum_val[node] - self.count[node] * limit
        
        mid = (l + r) // 2
        left_res = self.query_sum_max(self.left[node], l, mid, limit)
        right_res = self.query_sum_max(self.right[node], mid + 1, r, limit)
        return left_res + right_res

    def find_pivot(self, node_a, node_b, l, r):
        """
        Finds the largest value 'v' (rank) such that count_A(v) >= count_B(v).
        Returns the rank index in the coordinate compressed array (1-based).
        If count_A is always < count_B, returns 0.
        """
        if node_a == 0 and node_b == 0:
            return 0
        
        if l == r:
            # At leaf, check counts
            if self.count[node_a] >= self.count[node_b]:
                return l
            else:
                return l - 1 
        
        mid = (l + r) // 2
        
        # Check left child
        cnt_a_left = self.count[self.left[node_a]]
        cnt_b_left = self.count[self.left[node_b]]
        
        if cnt_a_left >= cnt_b_left:
            # The pivot is in the left subtree or at the boundary
            res = self.find_pivot(self.left[node_a], self.left[node_b], l, mid)
            if res != 0:
                return res
            # If not found in left (meaning for all v in left, A < B), 
            # but we entered here because total left A >= total left B?
            # Wait, if cnt_a_left >= cnt_b_left, there MUST be a point in left where A >= B.
            # Because at the leaf level, if A >= B, we return it.
            # So res will never be 0 if we enter this branch.
            return res
        else:
            # Left child has A < B. The pivot must be in the right child.
            return self.find_pivot(self.right[node_a], self.right[node_b], mid + 1, r)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        K = int(next(iterator))
        queries = []
        for _ in range(K):
            x = int(next(iterator))
            y = int(next(iterator))
            queries.append((x, y))
    except StopIteration:
        return

    # Coordinate Compression
    # We need to map values to ranks 1..M
    # The values can be up to 2*10^8, so we compress.
    # We include all values from A and B.
    all_vals = sorted(list(set(A) | set(B)))
    val_map = {v: i + 1 for i, v in enumerate(all_vals)}
    M = len(all_vals)
    
    # Build Persistent Segment Trees
    # Range of values in compressed domain is [1, M]
    tree_A = PersistentSegmentTree(M)
    tree_B = PersistentSegmentTree(M)
    
    # Build tree A
    # We need versions for each prefix length 1..N
    root_A = [0] * (N + 1)
    root_A[0] = tree_A._init_root() # This is 0
    
    for i in range(N):
        idx = val_map[A[i]]
        root_A[i+1] = tree_A.update(root_A[i], 1, M, idx, A[i])
        
    root_B = [0] * (N + 1)
    root_B[0] = tree_B._init_root() # This is 0
    
    for i in range(N):
        idx = val_map[B[i]]
        root_B[i+1] = tree_B.update(root_B[i], 1, M, idx, B[i])

    # Process Queries
    results = []
    
    for x, y in queries:
        # Get roots for prefixes
        node_a = root_A[x]
        node_b = root_B[y]
        
        # Find pivot
        pivot_idx = tree_A.find_pivot(node_a, node_b, 1, M)
        
        if pivot_idx == 0:
            # countA < countB everywhere
            # Ans = Sum(B) - Sum(A)
            sum_a = tree_A.sum_val[node_a]
            sum_b = tree_B.sum_val[node_b]
            results.append(sum_b - sum_a)
        else:
            # Get the actual value
            limit_val = all_vals[pivot_idx - 1]
            
            # Calculate terms
            # Term 1: sum(min(a, limit)) - sum(min(b, limit))
            term1_a = tree_A.query_sum_min(node_a, 1, M, limit_val)
            term1_b = tree_B.query_sum_min(node_b, 1, M, limit_val)
            
            # Term 2: sum(max(0, b - limit)) - sum(max(0, a - limit))
            term2_a = tree_A.query_sum_max(node_a, 1, M, limit_val)
            term2_b = tree_B.query_sum_max(node_b, 1, M, limit_val)
            
            ans = (term1_a - term1_b) + (term2_b - term2_a)
            results.append(ans)

    for res in results:
        print(res)

if __name__ == '__main__':
    solve()