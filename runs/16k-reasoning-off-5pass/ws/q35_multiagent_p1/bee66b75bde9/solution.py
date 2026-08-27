import sys

# Increase recursion depth just in case, though we aim for iterative
sys.setrecursionlimit(200000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # Store black cells to compute initial min bounds
    # We use dictionaries to store R_min and C_min
    # R_min[r] = max column index of black cells in row r
    # C_min[c] = max row index of black cells in column c
    R_min = {}
    C_min = {}
    
    # Store white cells to check later
    white_cells = []
    
    for _ in range(M):
        r = int(next(iterator))
        c = int(next(iterator))
        color = next(iterator)
        
        if color == 'B':
            # Update R_min[r]
            if r not in R_min or c > R_min[r]:
                R_min[r] = c
            # Update C_min[c]
            if c not in C_min or r > C_min[c]:
                C_min[c] = r
        else:
            white_cells.append((r, c))

    # Initialize R and C arrays with min bounds
    # Since N is large, we only store non-zero values in dictionaries
    # R[r] will store the current value for row r
    # C[c] will store the current value for column c
    R = dict(R_min)
    C = dict(C_min)
    
    # We need to propagate constraints.
    # If R[r] increases, it forces C[c] >= r for all c in [1, R[r]]
    # If C[c] increases, it forces R[r] >= c for all r in [1, C[c]]
    
    # To handle large N efficiently, we use a Segment Tree for range max updates.
    # The segment tree will manage the C array for range updates and point queries.
    # Similarly, we might need one for R, but let's see.
    # Actually, we can use one segment tree for C and one for R.
    # Since N is 10^9, we use a dynamic segment tree or coordinate compression.
    # Given the constraints and nature of updates (always [1, K]), 
    # a simple array with a "next pointer" or DSU-like structure for skipping processed indices is efficient.
    # However, since we update ranges [1, K], and we only care about indices that are "active" or need updating,
    # we can use a set of active indices or a segment tree.
    
    # Let's use a Segment Tree with coordinate compression.
    # The relevant coordinates are 1 and all values in R_min and C_min.
    # Also, during propagation, new values might appear.
    # But note: R[r] only takes values from {R_min[r]} U {C_min[c] for some c} U {values forced by propagation}.
    # Actually, R[r] is always >= some initial value.
    
    # Alternative efficient approach:
    # Use a Segment Tree over the domain [1, N]. Since N is large, use a dynamic segment tree (pointer-based).
    # Operations:
    # 1. Range Chmax: for l, r, v: tree[l..r] = max(tree[l..r], v)
    # 2. Point Query: get value at index i.
    # 3. We also need to find if there exists any index in [1, K] with value < v.
    #    If min(tree[1..K]) < v, then we need to update.
    
    # Let's implement a dynamic segment tree for Range Chmax and Range Min Query.
    # Node structure: min_val, lazy_chmax
    
    class Node:
        __slots__ = ['min_val', 'lazy', 'left', 'right']
        def __init__(self, min_val=0, lazy=0):
            self.min_val = min_val
            self.lazy = lazy
            self.left = None
            self.right = None

    class DynamicSegmentTree:
        def __init__(self, size):
            self.size = size
            self.root = Node()
            
        def _push(self, node):
            if node.lazy != 0:
                val = node.lazy
                if node.left is None:
                    node.left = Node()
                if node.right is None:
                    node.right = Node()
                
                node.left.min_val = max(node.left.min_val, val)
                node.left.lazy = max(node.left.lazy, val)
                
                node.right.min_val = max(node.right.min_val, val)
                node.right.lazy = max(node.right.lazy, val)
                
                node.lazy = 0

        def update(self, node, l, r, ql, qr, val):
            if ql > r or qr < l:
                return
            if ql <= l and r <= qr:
                node.min_val = max(node.min_val, val)
                node.lazy = max(node.lazy, val)
                return
            
            self._push(node)
            mid = (l + r) // 2
            if node.left is None:
                node.left = Node()
            if node.right is None:
                node.right = Node()
                
            self.update(node.left, l, mid, ql, qr, val)
            self.update(node.right, mid + 1, r, ql, qr, val)
            node.min_val = min(node.left.min_val, node.right.min_val)

        def query_min(self, node, l, r, ql, qr):
            if ql > r or qr < l:
                return float('inf')
            if ql <= l and r <= qr:
                return node.min_val
            
            self._push(node)
            mid = (l + r) // 2
            if node.left is None:
                node.left = Node()
            if node.right is None:
                node.right = Node()
                
            return min(
                self.query_min(node.left, l, mid, ql, qr),
                self.query_min(node.right, mid + 1, r, ql, qr)
            )

        def get(self, node, l, r, idx):
            if l == r:
                return node.min_val
            self._push(node)
            mid = (l + r) // 2
            if node.left is None:
                node.left = Node()
            if node.right is None:
                node.right = Node()
            if idx <= mid:
                return self.get(node.left, l, mid, idx)
            else:
                return self.get(node.right, mid + 1, r, idx)

    # Initialize trees with 0
    # The trees represent the current C and R values.
    # Initially, all are 0, but we have specific values in R_min and C_min.
    # We can build the tree by updating specific points first.
    
    # However, dynamic segment tree with point updates is easier.
    # Let's create two trees: one for C (indexed by column) and one for R (indexed by row).
    
    # Tree for C: stores C[c] for each column c
    tree_C = DynamicSegmentTree(N)
    # Tree for R: stores R[r] for each row r
    tree_R = DynamicSegmentTree(N)
    
    # Initialize with min values
    for r, val in R_min.items():
        # Update point r in tree_R to at least val
        # Since it's a range chmax tree, we can do point update as range [r, r]
        tree_R.update(tree_R.root, 1, N, r, r, val)
        
    for c, val in C_min.items():
        tree_C.update(tree_C.root, 1, N, c, c, val)
        
    # Queue for propagation
    # We store (type, index, new_value)
    # type 'R' means row index, 'C' means column index
    queue = []
    
    # Add initial changes to queue
    for r, val in R_min.items():
        queue.append(('R', r, val))
    for c, val in C_min.items():
        queue.append(('C', c, val))
        
    # To avoid processing same update multiple times, we can track current values
    # But the tree stores current values. We can check if the update is necessary.
    # Actually, the queue might contain redundant updates. We can check the current value before processing.
    
    # We also need to track which rows/cols have been "processed" to avoid infinite loops?
    # The values only increase, so it will terminate.
    
    # To optimize, we can use a set of active indices or just process.
    # Given M is 2e5, the number of updates is bounded.
    
    # Process queue
    while queue:
        typ, idx, new_val = queue.pop(0)
        
        # Check if this update is still relevant
        # Get current value from tree
        if typ == 'R':
            curr_val = tree_R.get(tree_R.root, 1, N, idx)
            if curr_val >= new_val:
                continue
            # Update tree_R to new_val (it's already updated in the call that pushed this, but let's be safe)
            # Actually, the update should have been done before pushing.
            # Let's assume the value in tree is already updated.
            # We need to propagate to C
            # For all c in [1, new_val], C[c] must be >= idx
            # Check min C in [1, new_val]
            min_C = tree_C.query_min(tree_C.root, 1, N, 1, new_val)
            if min_C < idx:
                # We need to update C[c] to idx for all c where C[c] < idx
                # This is a range chmax update: C[c] = max(C[c], idx) for c in [1, new_val]
                # But we only want to update those that are < idx.
                # The tree supports range chmax.
                tree_C.update(tree_C.root, 1, N, 1, new_val, idx)
                
                # Now we need to find which columns were updated and push them to queue
                # Finding all updated indices is hard with just min query.
                # Alternative: use a DSU-like structure to skip processed indices?
                # Or, since we only care about indices that are "active" or have initial values,
                # we can iterate over the initial columns and check if they need update.
                # But propagation can create new active columns.
                
                # Let's use a different approach for finding updated indices:
                # We can maintain a set of "dirty" intervals or use a segment tree to find indices with value < idx.
                # This is getting complex.
                
                # Simpler approach:
                # Since N is large, but M is small, the number of "interesting" columns is small.
                # The interesting columns are those with C_min[c] > 0.
                # Propagation might activate new columns.
                # A column c becomes active if it is forced by some row r.
                # If C[c] was 0 and becomes > 0, it's a new active column.
                
                # Let's maintain a set of active columns and rows.
                pass 
        else:
            curr_val = tree_C.get(tree_C.root, 1, N, idx)
            if curr_val >= new_val:
                continue
            # Propagate to R
            min_R = tree_R.query_min(tree_R.root, 1, N, 1, new_val)
            if min_R < idx:
                tree_R.update(tree_R.root, 1, N, 1, new_val, idx)
                pass

    # The above queue processing is incomplete because we don't know which specific indices were updated.
    # Let's restart with a more robust propagation method using a set of active indices.
    
    # Active rows and columns
    active_R = set(R_min.keys())
    active_C = set(C_min.keys())
    
    # We can use a list for queue
    q_R = list(R_min.keys())
    q_C = list(C_min.keys())
    
    # To avoid reprocessing, we can check if the value changed.
    # But we need to know which values changed.
    
    # Let's use a simpler propagation:
    # Iterate until no changes.
    # In each iteration, for each active row r, check if R[r] forces any C[c] to increase.
    # For each active col c, check if C[c] forces any R[r] to increase.
    
    # Since M is 2e5, O(M^2) is too slow.
    # We need the segment tree approach to be complete.
    
    # Let's implement the segment tree propagation correctly.
    # We need a function to find all indices in [1, K] with value < V and update them.
    # This can be done by traversing the segment tree.
    
    def propagate_C_updates(node, l, r, ql, qr, val, tree_C_obj, active_C_set, q_C_list):
        # Find all indices in [ql, qr] with current value < val and update them
        if ql > r or qr < l:
            return
        if node.min_val >= val:
            return # No need to update this range
        
        if l == r:
            # Leaf node
            if node.min_val < val:
                node.min_val = val
                node.lazy = max(node.lazy, val)
                if l in active_C_set:
                    # It was already active, but value increased. Push to queue if not already processed?
                    # We push to queue to propagate further.
                    q_C_list.append(l)
                else:
                    # New active column
                    active_C_set.add(l)
                    q_C_list.append(l)
            return
        
        tree_C_obj._push(node)
        mid = (l + r) // 2
        if node.left is None:
            node.left = Node()
        if node.right is None:
            node.right = Node()
            
        propagate_C_updates(node.left, l, mid, ql, qr, val, tree_C_obj, active_C_set, q_C_list)
        propagate_C_updates(node.right, mid + 1, r, ql, qr, val, tree_C_obj, active_C_set, q_C_list)
        node.min_val = min(node.left.min_val, node.right.min_val)

    def propagate_R_updates(node, l, r, ql, qr, val, tree_R_obj, active_R_set, q_R_list):
        if ql > r or qr < l:
            return
        if node.min_val >= val:
            return
        
        if l == r:
            if node.min_val < val:
                node.min_val = val
                node.lazy = max(node.lazy, val)
                if l in active_R_set:
                    q_R_list.append(l)
                else:
                    active_R_set.add(l)
                    q_R_list.append(l)
            return
            
        tree_R_obj._push(node)
        mid = (l + r) // 2
        if node.left is None:
            node.left = Node()
        if node.right is None:
            node.right = Node()
            
        propagate_R_updates(node.left, l, mid, ql, qr, val, tree_R_obj, active_R_set, q_R_list)
        propagate_R_updates(node.right, mid + 1, r, ql, qr, val, tree_R_obj, active_R_set, q_R_list)
        node.min_val = min(node.left.min_val, node.right.min_val)

    # Re-initialize trees and sets
    tree_C = DynamicSegmentTree(N)
    tree_R = DynamicSegmentTree(N)
    
    for r, val in R_min.items():
        tree_R.update(tree_R.root, 1, N, r, r, val)
    for c, val in C_min.items():
        tree_C.update(tree_C.root, 1, N, c, c, val)
        
    active_R = set(R_min.keys())
    active_C = set(C_min.keys())
    
    q_R = list(R_min.keys())
    q_C = list(C_min.keys())
    
    # Process queues
    # Use a while loop with two queues
    while q_R or q_C:
        # Process all R updates
        while q_R:
            r = q_R.pop(0)
            val_R = tree_R.get(tree_R.root, 1, N, r)
            if val_R == 0:
                continue
            # Propagate to C: for c in [1, val_R], C[c] >= r
            # Check if any C[c] < r in [1, val_R]
            min_C = tree_C.query_min(tree_C.root, 1, N, 1, val_R)
            if min_C < r:
                propagate_C_updates(tree_C.root, 1, N, 1, val_R, r, tree_C, active_C, q_C)
                
        # Process all C updates
        while q_C:
            c = q_C.pop(0)
            val_C = tree_C.get(tree_C.root, 1, N, c)
            if val_C == 0:
                continue
            # Propagate to R: for r in [1, val_C], R[r] >= c
            min_R = tree_R.query_min(tree_R.root, 1, N, 1, val_C)
            if min_R < c:
                propagate_R_updates(tree_R.root, 1, N, 1, val_C, c, tree_R, active_R, q_R)

    # Final check for white cells
    for r, c in white_cells:
        R_r = tree_R.get(tree_R.root, 1, N, r)
        C_c = tree_C.get(tree_C.root, 1, N, c)
        # Cell (r, c) is black if c <= R_r and r <= C_c
        # It must be white, so NOT (c <= R_r and r <= C_c)
        if c <= R_r and r <= C_c:
            print("No")
            return
            
    print("Yes")

solve()