import sys

def solve():
    # Increase recursion depth just in case, though we'll use iterative approaches
    sys.setrecursionlimit(300000)
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        
        A = [0] * (N + 1)
        for i in range(1, N + 1):
            A[i] = int(next(iterator))
            
        B = [0] * (N + 1)
        for i in range(1, N + 1):
            B[i] = int(next(iterator))
            
        P = [0] * (N + 1)
        for i in range(1, N + 1):
            P[i] = int(next(iterator))
            
        Q = [0] * (N + 1)
        for i in range(1, N + 1):
            Q[i] = int(next(iterator))
            
    except StopIteration:
        return

    # Helper function to find the cycle containing a node and distances to a target in that cycle
    # Returns: (cycle_nodes_list, dist_map)
    # cycle_nodes_list: list of nodes in the cycle in order of traversal (u -> P[u] -> ...)
    # dist_map: dict mapping node -> distance to target X in the cycle
    # If target X is not in the cycle, returns None
    
    def get_cycle_info(target, perm):
        # Find the cycle containing target
        # Since it's a permutation, we can just follow the path until we loop back
        # But we need to identify the cycle specifically.
        
        # Step 1: Find the cycle
        # Start from target and follow until we return to target
        cycle_nodes = []
        curr = target
        visited = set()
        
        while curr not in visited:
            visited.add(curr)
            cycle_nodes.append(curr)
            curr = perm[curr]
            
        # Now curr is the first repeated node. Since we started at target and followed a permutation,
        # we must have returned to target if target is in a cycle.
        # Actually, in a permutation, every node is in exactly one cycle.
        # So starting from target and following perm will eventually return to target.
        
        # Verify we returned to target
        if curr != target:
            # This should not happen in a permutation if we start from a node in the cycle
            # But let's be safe. If curr != target, it means we entered a cycle that doesn't contain target?
            # Impossible in a permutation. Every component is a cycle.
            pass
            
        # cycle_nodes contains the cycle in order: target -> perm[target] -> ... -> target
        # Let's create a distance map from each node in the cycle to target.
        # Distance is the number of steps to reach target.
        # dist(target) = 0
        # dist(perm[target]) = 1? No, we want distance TO target.
        # If we are at node u, dist(u) is k such that perm^k(u) = target.
        
        # Let's reverse the cycle to make it easier to compute distances to target
        # The cycle is: c0, c1, c2, ..., c_{m-1} where c0 = target, c1 = perm[c0], etc.
        # perm[c_i] = c_{i+1} (indices mod m)
        # We want dist(c_i) such that applying perm dist(c_i) times gets us to c0.
        # perm^k(c_i) = c_{(i+k)%m} = c0 => (i+k)%m = 0 => k = (m - i) % m.
        
        m = len(cycle_nodes)
        dist_map = {}
        for i, node in enumerate(cycle_nodes):
            # node is at index i in the cycle list starting with target at index 0
            # Distance to target (index 0) is (m - i) % m
            dist_map[node] = (m - i) % m
            
        return cycle_nodes, dist_map

    # Process Red balls (P graph)
    cycle_P, dist_P = get_cycle_info(X, P)
    set_P = set()
    
    # Check if all red balls are in the cycle of X
    for i in range(1, N + 1):
        if A[i] == 1:
            if i not in dist_P:
                print(-1)
                return
            # Add all nodes on the path from i to X (excluding X)
            # The path from i to X consists of nodes with distances 1, 2, ..., dist_P[i]
            # Actually, the set of nodes operated on is the set of ancestors of X that are reachable from i.
            # In the cycle, this is the contiguous segment from i to the node before X.
            # The number of nodes is dist_P[i].
            # But we need the actual set of nodes to compute union later.
            # Instead of adding all, let's just mark the max distance for now?
            # No, we need the set of nodes.
            # The nodes on the path from i to X (excluding X) are the nodes v in the cycle such that
            # dist(v) <= dist(i) and v is "upstream" from i?
            # Actually, in a cycle, the path from i to X is unique.
            # It consists of the nodes: i, perm[i], perm[perm[i]], ..., up to the node before X.
            # These are exactly the nodes in the cycle that appear in the sequence starting from i and ending before X.
            # In terms of indices in cycle_nodes (where cycle_nodes[0] = X):
            # i is at index i_idx. The path goes i_idx, i_idx+1, ..., m-1.
            # The nodes are cycle_nodes[k] for k in range(i_idx, m).
            # Wait, dist(i) = (m - i_idx) % m.
            # If i_idx = 0 (i=X), dist=0. Path is empty.
            # If i_idx = 1, dist=1. Path is [cycle_nodes[1]].
            # If i_idx = 2, dist=2. Path is [cycle_nodes[2], cycle_nodes[1]]? No.
            # Let's trace:
            # cycle: X -> c1 -> c2 -> ... -> c_{m-1} -> X
            # perm[X] = c1, perm[c1] = c2, ..., perm[c_{m-1}] = X.
            # Path from c1 to X: c1 -> c2 -> ... -> c_{m-1} -> X.
            # Nodes operated: c1, c2, ..., c_{m-1}.
            # Indices in cycle_nodes: 1, 2, ..., m-1.
            # Path from c2 to X: c2 -> ... -> c_{m-1} -> X.
            # Nodes operated: c2, ..., c_{m-1}.
            # Indices: 2, ..., m-1.
            # So, for a node at index i_idx, the nodes operated are cycle_nodes[k] for k in range(i_idx, m).
            # This is a contiguous segment of the cycle_nodes list.
            
            # To compute the union efficiently, we can just collect all such segments.
            # Since N is up to 2e5, we can't iterate all nodes for each ball.
            # But we can find the maximum index i_idx among all red balls.
            # The union of segments [i_idx, m-1] for all red balls is [min_i_idx, m-1].
            # min_i_idx is the minimum index among all red balls in the cycle.
            
            # Let's find the min index for red balls in P-cycle
            pass

    # Let's refactor to find min index for each color
    min_idx_P = float('inf')
    has_red = False
    for i in range(1, N + 1):
        if A[i] == 1:
            has_red = True
            if i in dist_P:
                idx = cycle_P.index(i) # This is O(N) per ball, too slow if many balls
                # We need a faster way to get index
                # We can precompute a map from node to index in cycle
                pass
    
    # Precompute node to index map for P cycle
    node_to_idx_P = {node: idx for idx, node in enumerate(cycle_P)}
    
    min_idx_P = float('inf')
    for i in range(1, N + 1):
        if A[i] == 1:
            if i not in node_to_idx_P:
                print(-1)
                return
            idx = node_to_idx_P[i]
            if idx < min_idx_P:
                min_idx_P = idx
                
    if has_red:
        # The set S_P is { cycle_P[k] for k in range(min_idx_P, m_P) }
        # Size is m_P - min_idx_P
        # But we need the actual set for union with S_Q
        # We can just mark these nodes in a boolean array or set
        pass
    else:
        min_idx_P = -1 # No red balls

    # Same for Q
    cycle_Q, dist_Q = get_cycle_info(X, Q)
    node_to_idx_Q = {node: idx for idx, node in enumerate(cycle_Q)}
    
    min_idx_Q = float('inf')
    has_blue = False
    for i in range(1, N + 1):
        if B[i] == 1:
            has_blue = True
            if i not in node_to_idx_Q:
                print(-1)
                return
            idx = node_to_idx_Q[i]
            if idx < min_idx_Q:
                min_idx_Q = idx
                
    if not has_blue:
        min_idx_Q = -1

    # Now compute the union of nodes
    # S_P = { cycle_P[k] for k in range(min_idx_P, len(cycle_P)) } if has_red else empty
    # S_Q = { cycle_Q[k] for k in range(min_idx_Q, len(cycle_Q)) } if has_blue else empty
    
    required_ops = set()
    
    if has_red:
        m_P = len(cycle_P)
        for k in range(min_idx_P, m_P):
            required_ops.add(cycle_P[k])
            
    if has_blue:
        m_Q = len(cycle_Q)
        for k in range(min_idx_Q, m_Q):
            required_ops.add(cycle_Q[k])
            
    print(len(required_ops))

solve()