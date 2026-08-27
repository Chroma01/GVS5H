import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u, v))
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    # Kruskal's algorithm to find MST
    edges.sort()
    parent = list(range(n + 1))
    rank = [0] * (n + 1)
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True
    
    mst_edges = []
    for w, u, v in edges:
        if union(u, v):
            mst_edges.append((u, v, w))
    
    # Build adjacency list of MST
    adj = [[] for _ in range(n + 1)]
    for u, v, w in mst_edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # Binary lifting setup
    LOG = (n).bit_length()
    up = [[0] * (n + 1) for _ in range(LOG)]
    max_edge = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    order = []
    parent_arr = [0] * (n + 1)
    edge_weight_to_parent = [0] * (n + 1)
    
    # Iterative DFS to compute tin/tout, depth, parent, edge_weight
    timer = 0
    stack = [(1, 0, 0, 0)]  # (node, parent, edge_weight, state) state 0=enter, 1=exit
    visited = [False] * (n + 1)
    visited[1] = True
    while stack:
        u, p, w, state = stack.pop()
        if state == 0:
            tin[u] = timer
            timer += 1
            order.append(u)
            parent_arr[u] = p
            edge_weight_to_parent[u] = w
            depth[u] = depth[p] + 1 if p != 0 else 0
            stack.append((u, p, w, 1))
            for v, ew in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, u, ew, 0))
        else:
            tout[u] = timer
            timer += 1
    
    # Process order to set up[0], max_edge[0] correctly (already set during DFS)
    up[0] = parent_arr[:]
    max_edge[0] = edge_weight_to_parent[:]
    
    # Fill binary lifting tables
    for i in range(1, LOG):
        for v in range(1, n + 1):
            up[i][v] = up[i-1][up[i-1][v]]
            max_edge[i][v] = max(max_edge[i-1][v], max_edge[i-1][up[i-1][v]])
    
    def is_ancestor(u, v):
        return tin[u] <= tin[v] and tout[v] <= tout[u]
    
    def lca(u, v):
        if is_ancestor(u, v):
            return u
        if is_ancestor(v, u):
            return v
        for i in range(LOG - 1, -1, -1):
            if not is_ancestor(up[i][u], v):
                u = up[i][u]
        return up[0][u]
    
    def get_max_on_path(u, v):
        # Get max edge weight on path between u and v
        l = lca(u, v)
        cur_max = 0
        # Path from u to l
        node = u
        diff = depth[node] - depth[l]
        for i in range(LOG):
            if diff & (1 << i):
                cur_max = max(cur_max, max_edge[i][node])
                node = up[i][node]
        # Path from v to l
        node = v
        diff = depth[node] - depth[l]
        for i in range(LOG):
            if diff & (1 << i):
                cur_max = max(cur_max, max_edge[i][node])
                node = up[i][node]
        return cur_max
    
    # Build virtual tree over S = A ∪ B
    S = list(set(A + B))
    S.sort(key=lambda x: tin[x])
    
    # Add LCAs of consecutive nodes in sorted S
    stack = []
    virtual_adj = {}
    virtual_nodes = set(S)
    
    for node in S:
        while stack and not is_ancestor(stack[-1], node):
            stack.pop()
        if stack:
            parent_node = stack[-1]
            # Edge between parent_node and node
            cost = get_max_on_path(parent_node, node)
            if parent_node not in virtual_adj:
                virtual_adj[parent_node] = []
            virtual_adj[parent_node].append((node, cost))
            if node not in virtual_adj:
                virtual_adj[node] = []
        else:
            if node not in virtual_adj:
                virtual_adj[node] = []
        stack.append(node)
    
    # Now we need to add the LCA nodes that were not in S
    # Actually, the standard virtual tree construction: after processing sorted nodes, we pop stack and add edges
    # But we need to include the LCAs. The above code only added edges between nodes in S and their ancestors that are in the stack.
    # We need to explicitly add the LCAs.
    # Let's do the standard virtual tree construction:
    # 1. Sort S by tin
    # 2. For each consecutive pair, add their LCA to the set
    # 3. Sort again, then build the tree using a stack
    
    S_with_lca = set(S)
    for i in range(len(S) - 1):
        S_with_lca.add(lca(S[i], S[i+1]))
    S_with_lca = list(S_with_lca)
    S_with_lca.sort(key=lambda x: tin[x])
    
    # Build virtual tree using stack
    virtual_adj = {}
    stack = []
    for node in S_with_lca:
        while stack and not is_ancestor(stack[-1], node):
            stack.pop()
        if stack:
            parent_node = stack[-1]
            cost = get_max_on_path(parent_node, node)
            if parent_node not in virtual_adj:
                virtual_adj[parent_node] = []
            virtual_adj[parent_node].append((node, cost))
            if node not in virtual_adj:
                virtual_adj[node] = []
        else:
            if node not in virtual_adj:
                virtual_adj[node] = []
        stack.append(node)
    
    # Output the virtual tree for testing
    # Print number of nodes and edges
    nodes = list(virtual_adj.keys())
    print(f"Virtual tree has {len(nodes)} nodes")
    edge_count = sum(len(children) for children in virtual_adj.values())
    print(f"Virtual tree has {edge_count} edges")
    
    # Print edges in format: parent child cost
    for parent_node, children in virtual_adj.items():
        for child, cost in children:
            print(f"{parent_node} {child} {cost}")

if __name__ == "__main__":
    solve()