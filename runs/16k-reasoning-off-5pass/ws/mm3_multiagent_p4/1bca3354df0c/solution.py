import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    
    parent = list(range(n))
    rank = [0] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        x = find(x)
        y = find(y)
        if x == y:
            return
        if rank[x] < rank[y]:
            x, y = y, x
        parent[y] = x
        if rank[x] == rank[y]:
            rank[x] += 1
    
    edges = []
    for _ in range(m):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        edges.append((u, v))
        union(u, v)
    
    comp = [0] * n
    comp_id = {}
    cur_id = 0
    for i in range(n):
        r = find(i)
        if r not in comp_id:
            comp_id[r] = cur_id
            cur_id += 1
        comp[i] = comp_id[r]
    
    k = cur_id
    color = [-1] * n
    # BFS for each component
    from collections import deque
    for cid in range(k):
        # find any vertex in this component
        # we can scan
        pass
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    
    # Re-BFS properly
    for i in range(n):
        if color[i] == -1:
            color[i] = 0
            dq = deque([i])
            while dq:
                u = dq.popleft()
                for v in adj[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        dq.append(v)
                    # no need to check conflict; input guarantees bipartite
    
    # Count non-empty color groups per component
    # group size = number of vertices of given color in given component
    group_count = [0] * (2 * k)  # store sizes, but we only count non-empty
    for i in range(n):
        cid = comp[i]
        idx = 2 * cid + color[i]
        group_count[idx] += 1
    
    # Count number of non-empty groups
    g = sum(1 for cnt in group_count if cnt > 0)
    
    total_pairs = g * (g - 1) // 2
    remaining = total_pairs - m
    if remaining % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

solve()