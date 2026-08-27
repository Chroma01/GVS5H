import sys

# Increase recursion depth just in case, though iterative approach is preferred for safety
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    edges = []
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        edges.append((w, u, v))

    # Read A and B sequences
    A = []
    for _ in range(K):
        A.append(int(next(iterator)))
        
    B = []
    for _ in range(K):
        B.append(int(next(iterator)))

    # 1. Build MST using Kruskal's Algorithm
    # Sort edges by weight
    edges.sort(key=lambda x: x[0])
    
    parent = list(range(N + 1))
    rank = [0] * (N + 1)
    
    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False

    mst_adj = [[] for _ in range(N + 1)]
    mst_edges_count = 0
    
    for w, u, v in edges:
        if union(u, v):
            mst_adj[u].append((v, w))
            mst_adj[v].append((u, w))
            mst_edges_count += 1
            if mst_edges_count == N - 1:
                break

    # 2. Count occurrences of each vertex in A and B
    # Using arrays for speed
    countA = [0] * (N + 1)
    for x in A:
        countA[x] += 1
        
    countB = [0] * (N + 1)
    for x in B:
        countB[x] += 1

    # 3. DFS to compute subtree sums of A and B counts
    # We use an iterative DFS to avoid recursion depth issues
    # We need to process children before parents (post-order)
    
    root = 1
    parent_map = [0] * (N + 1)
    edge_weight_to_parent = [0] * (N + 1) # Weight of edge connecting node to its parent
    order = []
    stack = [root]
    visited = [False] * (N + 1)
    visited[root] = True
    
    # Standard iterative DFS to establish parent pointers and traversal order
    while stack:
        u = stack.pop()
        order.append(u)
        
        for v, w in mst_adj[u]:
            if not visited[v]:
                visited[v] = True
                parent_map[v] = u
                edge_weight_to_parent[v] = w
                stack.append(v)
    
    # Process in reverse order (leaves to root)
    subA = [0] * (N + 1)
    subB = [0] * (N + 1)
    
    # Initialize with the counts of the nodes themselves
    for i in range(1, N + 1):
        subA[i] = countA[i]
        subB[i] = countB[i]
        
    total_cost = 0
    
    # Reverse order ensures we process children before parents
    for u in reversed(order):
        if u == root:
            continue
            
        p = parent_map[u]
        w = edge_weight_to_parent[u]
        
        # The component below the edge (u, p) is the subtree rooted at u
        # The number of A nodes in this component is subA[u]
        # The number of B nodes in this component is subB[u]
        
        diff = abs(subA[u] - subB[u])
        total_cost += diff * w
        
        # Add the counts from the child to the parent
        subA[p] += subA[u]
        subB[p] += subB[u]
        
    print(total_cost)

solve()