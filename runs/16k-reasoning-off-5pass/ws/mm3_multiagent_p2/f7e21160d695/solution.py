import sys
sys.setrecursionlimit(1 << 25)

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
    edges = []
    for _ in range(M):
        u = int(input_data[idx]); idx += 1
        v = int(input_data[idx]); idx += 1
        w = int(input_data[idx]); idx += 1
        edges.append((w, u, v))
    
    cntA = [0] * (N + 1)
    cntB = [0] * (N + 1)
    
    for _ in range(K):
        a = int(input_data[idx]); idx += 1
        cntA[a] += 1
    for _ in range(K):
        b = int(input_data[idx]); idx += 1
        cntB[b] += 1
    
    # Sort edges by weight for Kruskal
    edges.sort()
    
    # DSU
    parent = list(range(N + 1))
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[px] = py
        return True
    
    # KRT: nodes N+1 .. 2N-1
    # krt_left[node], krt_right[node], krt_weight[node]
    # We need to know for each DSU root, what is the corresponding KRT node.
    # Initially, each vertex i is its own KRT leaf with id i.
    krt_left = [0] * (2 * N + 2)
    krt_right = [0] * (2 * N + 2)
    krt_weight = [0] * (2 * N + 2)
    # dsu_node[rep] = current KRT node id for that DSU component
    dsu_node = [0] * (2 * N + 2)
    for i in range(1, N + 1):
        dsu_node[i] = i
    
    next_id = N
    total_unmatched_A_root = 0
    total_unmatched_B_root = 0
    
    for w, u, v in edges:
        pu = find(u)
        pv = find(v)
        if pu == pv:
            continue
        next_id += 1
        krt_left[next_id] = dsu_node[pu]
        krt_right[next_id] = dsu_node[pv]
        krt_weight[next_id] = w
        # Union DSU: make pu's parent = pv (or vice versa)
        parent[pu] = pv
        dsu_node[pv] = next_id
    
    # Now next_id should be 2N-1, and dsu_node[find(any)] = root
    root = dsu_node[find(1)]
    
    # Post-order DFS
    # Returns (unmatched_A, unmatched_B) for the subtree
    def dfs(node):
        if node <= N:
            # Leaf
            return (cntA[node], cntB[node])
        aL, bL = dfs(krt_left[node])
        aR, bR = dfs(krt_right[node])
        # Cross pairings
        cross = min(aL, bR) + min(aR, bL)
        dfs.cost += krt_weight[node] * cross
        # New unmatched
        new_a = (aL - min(aL, bR)) + (aR - min(aR, bL))
        new_b = (bL - min(aL, bR)) + (bR - min(aR, bL))
        return (new_a, new_b)
    
    dfs.cost = 0
    dfs(root)
    
    print(dfs.cost)

solve()