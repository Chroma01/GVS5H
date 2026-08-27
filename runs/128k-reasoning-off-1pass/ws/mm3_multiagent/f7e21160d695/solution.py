import sys
sys.setrecursionlimit(1 << 25)

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    
    edges = []
    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        w = int(data[idx]); idx += 1
        edges.append((w, u, v))
    
    edges.sort()
    
    # DSU with parent tracking
    dsu_parent = list(range(N + 1))
    node_id = [0] * (N + 1)  # current root node id for each DSU component
    
    # We'll build nodes 1..N as original vertices
    # New internal nodes will be N+1, N+2, ...
    # children: for node i, left child and right child (for internal nodes)
    left = [0] * (2 * N)
    right = [0] * (2 * N)
    weight = [0] * (2 * N)  # weight of internal node, 0 for leaves
    
    # Initialize: each vertex i is represented by node i initially
    for i in range(1, N + 1):
        node_id[i] = i
    
    def find(x):
        while dsu_parent[x] != x:
            dsu_parent[x] = dsu_parent[dsu_parent[x]]
            x = dsu_parent[x]
        return x
    
    next_node = N  # next available node id (we'll use 1-indexed up to 2N-1)
    total_nodes = N  # current number of nodes
    
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        # Create new node
        next_node += 1
        total_nodes = next_node
        left[next_node] = node_id[ru]
        right[next_node] = node_id[rv]
        weight[next_node] = w
        # Union: make new node the root of both components
        # We need to link DSU sets
        dsu_parent[ru] = rv  # union by... we'll use a separate array
        # Actually let's use a proper DSU
        # Let's redo DSU properly
        pass
    
    # The above incomplete. Let me rewrite with proper DSU.
    
    # Reset
    dsu_parent = list(range(N + 1))
    rank = [0] * (N + 1)
    node_id = [0] * (N + 1)
    for i in range(1, N + 1):
        node_id[i] = i
    
    left = [0] * (2 * N + 1)
    right = [0] * (2 * N + 1)
    weight = [0] * (2 * N + 1)
    
    def find(x):
        while dsu_parent[x] != x:
            dsu_parent[x] = dsu_parent[dsu_parent[x]]
            x = dsu_parent[x]
        return x
    
    def union(x, y, new_node):
        # x and y are DSU roots, merge into new_node
        # We'll attach x to y for simplicity (union by rank would be better)
        # Actually let's do union by rank
        rx = find(x)
        ry = find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            dsu_parent[rx] = ry
            node_id[ry] = new_node
        else:
            dsu_parent[ry] = rx
            node_id[rx] = new_node
            if rank[rx] == rank[ry]:
                rank[rx] += 1
        return True
    
    next_node = N
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        next_node += 1
        left[next_node] = node_id[ru]
        right[next_node] = node_id[rv]
        weight[next_node] = w
        # The new node represents the merged component
        # We need to make sure the merged component's node_id is the new node
        # Union ru and rv, setting the new node_id for the merged set
        # We'll do manual union to control node_id
        if rank[ru] < rank[rv]:
            dsu_parent[ru] = rv
            node_id[rv] = next_node
        else:
            dsu_parent[rv] = ru
            node_id[ru] = next_node
            if rank[ru] == rank[rv]:
                rank[ru] += 1
    
    # After processing all edges, we should have one component
    # The root of DSU gives us the root of the Kruskal tree
    root = -1
    for i in range(1, N + 1):
        if find(i) == i:
            root = node_id[i]
            break
    
    # Read A and B sequences
    A = [0] * (K + 1)
    B = [0] * (K + 1)
    for i in range(1, K + 1):
        A[i] = int(data[idx]); idx += 1
    for i in range(1, K + 1):
        B[i] = int(data[idx]); idx += 1
    
    # Count occurrences: cntA[i] = number of times vertex i appears in A
    # cntB[i] = number of times vertex i appears in B
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    for i in range(1, K + 1):
        cntA[A[i]] += 1
        cntB[B[i]] += 1
    
    # Post-order traversal (DFS) on the tree
    # We need to compute, for each node, the surplus of A and B from its subtree
    # But we only need to propagate: total_A, total_B
    # Actually we need to handle: a node can have both A and B leaves in its subtree
    # The matches at this node: min(total_A_from_children, total_B_from_children)
    # But wait: we also need to consider if the node itself is a leaf (original vertex)
    # Original vertices are nodes 1..N. They may have cntA > 0 or cntB > 0.
    # For internal nodes, they have no A/B count themselves.
    
    # The key insight: we match pairs at each internal node.
    # For a node, the number of A-type leaves in its subtree is sum of cntA[leaves in subtree]
    # Similarly for B.
    # The cost added at this node is min(a, b) * weight[node], where a and b are
    # the total counts of A and B in the entire subtree of this node.
    # The unmatched surplus (|a - b|) is passed to the parent.
    
    # But we need to be careful: the children might have their own internal nodes where
    # matches already happened. The "surplus" passed up is |a - b|.
    # However, the pairing strategy that minimizes total cost is: at each node,
    # we want to match as many cross pairs as possible, which means we match
    # min(a, b) pairs at cost weight[node] each, and the remaining (a-b or b-a)
    # unmatched must be matched higher up at higher cost.
    # This is correct: it's the standard optimal strategy for this tree matching problem.
    
    # So we do a DFS. For each node:
    #   if node <= N (original vertex): a = cntA[node], b = cntB[node]
    #   else (internal): a = sum of a from children, b = sum of b from children
    #   matches = min(a, b)
    #   answer += matches * weight[node]  (weight[node] is 0 for original vertices, so safe)
    #   return (a - matches, b - matches) to parent
    
    ans = 0
    # Use iterative DFS to avoid recursion depth issues, or increase recursion limit
    # We have up to 2N-1 nodes, recursion is fine with setrecursionlimit
    
    sys.setrecursionlimit(1 << 25)
    
    def dfs(u):
        global ans
        if u <= N:
            return cntA[u], cntB[u]
        a = 0
        b = 0
        for child in (left[u], right[u]):
            ca, cb = dfs(child)
            a += ca
            b += cb
        m = min(a, b)
        ans += m * weight[u]
        return a - m, b - m
    
    dfs(root)
    print(ans)

solve()