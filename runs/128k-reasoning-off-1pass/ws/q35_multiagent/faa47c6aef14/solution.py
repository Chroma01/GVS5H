import sys

def solve():
    # Increase recursion depth just in case, though we will use iterative approaches
    sys.setrecursionlimit(300000)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

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

    # Helper function to find the cycle containing a node in a permutation graph
    # Returns a list of nodes in the cycle in order of traversal: start -> P[start] -> ...
    # Also returns a dictionary mapping node to its distance from start
    def get_cycle(start, perm):
        cycle_nodes = []
        node = start
        visited = set()
        while node not in visited:
            visited.add(node)
            cycle_nodes.append(node)
            node = perm[node]
        
        # Now cycle_nodes contains the cycle starting from 'start'
        # We want to compute distance from each node to 'start' in the cycle?
        # Actually, the operation moves balls from i to perm[i].
        # So if we are at node u, after op on u, ball goes to perm[u].
        # To move a ball from u to start, we need to apply ops on u, perm[u], ... until it reaches start.
        # The path is u -> perm[u] -> perm[perm[u]] -> ... -> start.
        # The set of boxes operated on is the set of nodes on this path excluding start.
        
        # Let's map each node in the cycle to its index in the cycle_nodes list
        # The cycle is cycle_nodes[0], cycle_nodes[1], ..., cycle_nodes[k-1], cycle_nodes[0]...
        # perm[cycle_nodes[i]] = cycle_nodes[(i+1)%k]
        
        # Distance from cycle_nodes[i] to cycle_nodes[0] (which is start) is (k - i) % k ?
        # Let's trace:
        # If i=0 (start), dist=0.
        # If i=1, perm[cycle_nodes[1]] = cycle_nodes[2]. To get to 0, we need to go 1->2->...->k-1->0.
        # Steps: k-1.
        # Generally, dist(i) = (k - i) % k.
        
        k = len(cycle_nodes)
        dist_to_start = {}
        for idx, node in enumerate(cycle_nodes):
            dist_to_start[node] = (k - idx) % k
            
        return cycle_nodes, dist_to_start

    # Check if all red balls are in the same cycle as X in P
    # Find cycle for X in P
    red_cycle_nodes, red_dist = get_cycle(X, P)
    red_cycle_set = set(red_cycle_nodes)
    
    # Check validity of red balls
    red_possible = True
    for i in range(1, N + 1):
        if A[i] > 0:
            if i not in red_cycle_set:
                red_possible = False
                break
    
    if not red_possible:
        print(-1)
        return

    # Find cycle for X in Q
    blue_cycle_nodes, blue_dist = get_cycle(X, Q)
    blue_cycle_set = set(blue_cycle_nodes)
    
    # Check validity of blue balls
    blue_possible = True
    for i in range(1, N + 1):
        if B[i] > 0:
            if i not in blue_cycle_set:
                blue_possible = False
                break
                
    if not blue_possible:
        print(-1)
        return

    # If no balls at all
    has_red = any(A[i] > 0 for i in range(1, N + 1))
    has_blue = any(B[i] > 0 for i in range(1, N + 1))
    
    if not has_red and not has_blue:
        print(0)
        return

    # Calculate the set of boxes to operate on for red
    # For each i with A[i] > 0, we need to operate on the path from i to X in red graph.
    # The path from i to X consists of nodes: i, P[i], P[P[i]], ... up to the node before X.
    # In terms of distances: if dist(i) = d, then we need nodes with distances d, d-1, ..., 1 from X.
    # Specifically, the node with distance k from X is the k-th predecessor of X.
    # Let's build the set of required red boxes.
    
    red_ops = set()
    if has_red:
        # Find the maximum distance required for red balls
        max_red_dist = 0
        for i in range(1, N + 1):
            if A[i] > 0:
                d = red_dist[i]
                if d > max_red_dist:
                    max_red_dist = d
        
        # If max_red_dist is 0, it means all red balls are already at X.
        # In that case, no operations needed for red.
        if max_red_dist > 0:
            # We need to operate on all nodes that are on the path from any source to X.
            # Since it's a single cycle, and we want to move ALL balls to X,
            # do we need to operate on EVERY node in the cycle except X?
            # Let's verify with Sample 1.
            # Red cycle: 3->2->1->4->3. X=3.
            # Nodes: 3 (dist 0), 2 (dist 1? No. P[2]=1, P[1]=4, P[4]=3. Path 2->1->4->3. Dist 3.)
            # Let's re-calculate distances carefully.
            # Cycle nodes from get_cycle(3, P):
            # Start 3. P[3]=2. P[2]=1. P[1]=4. P[4]=3.
            # List: [3, 2, 1, 4].
            # Distances to 3:
            # 3: 0
            # 2: (4-1)%4 = 3. Path 2->1->4->3. Correct.
            # 1: (4-2)%4 = 2. Path 1->4->3. Correct.
            # 4: (4-3)%4 = 1. Path 4->3. Correct.
            
            # Red balls at 2 and 4.
            # Ball at 2 needs dist 3. Path nodes: 2, 1, 4.
            # Ball at 4 needs dist 1. Path nodes: 4.
            # Union: {2, 1, 4}.
            
            # General rule: For a ball at i with distance d, the nodes operated on are those with distances d, d-1, ..., 1.
            # So if we have multiple balls, the union of their paths is the set of all nodes with distance <= max_red_dist?
            # Not necessarily. If we have a ball at dist 3 and a ball at dist 1, the union is {nodes with dist 3, 2, 1} U {nodes with dist 1} = {nodes with dist 1, 2, 3}.
            # Yes, because the path for dist 3 includes the path for dist 1 (since 1 is on the path from 3 to 0? No.
            # Path for dist 3: node_3 -> node_2 -> node_1 -> node_0(X). Nodes: node_3, node_2, node_1.
            # Path for dist 1: node_1 -> node_0(X). Node: node_1.
            # Union: {node_3, node_2, node_1}.
            # This is exactly the set of nodes with distance >= 1 and <= 3?
            # In a cycle, the nodes with distance k are unique.
            # The path from a node with distance d consists of nodes with distances d, d-1, ..., 1.
            # So the union of paths for a set of distances D is the set of nodes with distance in [1, max(D)].
            
            # So, red_ops should contain all nodes in the red cycle with distance in [1, max_red_dist].
            
            for d in range(1, max_red_dist + 1):
                # Find the node with distance d in the red cycle
                # We can precompute a map from distance to node
                pass
            
            # Let's build a map for red cycle
            red_dist_to_node = {}
            for node, d in red_dist.items():
                red_dist_to_node[d] = node
            
            for d in range(1, max_red_dist + 1):
                if d in red_dist_to_node:
                    red_ops.add(red_dist_to_node[d])
                else:
                    # This should not happen if max_red_dist is derived from existing balls
                    pass

    # Similarly for blue
    blue_ops = set()
    if has_blue:
        max_blue_dist = 0
        for i in range(1, N + 1):
            if B[i] > 0:
                d = blue_dist[i]
                if d > max_blue_dist:
                    max_blue_dist = d
        
        if max_blue_dist > 0:
            blue_dist_to_node = {}
            for node, d in blue_dist.items():
                blue_dist_to_node[d] = node
            
            for d in range(1, max_blue_dist + 1):
                if d in blue_dist_to_node:
                    blue_ops.add(blue_dist_to_node[d])

    # The answer is the size of the union
    ans = len(red_ops | blue_ops)
    print(ans)

solve()