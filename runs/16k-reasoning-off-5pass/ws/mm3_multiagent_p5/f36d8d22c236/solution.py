import sys
input = sys.stdin.readline

def solve():
    N = int(input().strip())
    S = input().strip()
    T = input().strip()
    
    if S == T:
        print(0)
        return
    
    # need[c] = index of character that all 'c' in S must become
    need = [None] * 26
    for i in range(N):
        s_idx = ord(S[i]) - 97
        t_idx = ord(T[i]) - 97
        if s_idx == t_idx:
            continue
        if need[s_idx] is None:
            need[s_idx] = t_idx
        elif need[s_idx] != t_idx:
            print(-1)
            return
    
    # Count edges (c -> need[c] where c != need[c])
    edges = 0
    for c in range(26):
        if need[c] is not None:
            edges += 1
    
    if edges == 0:
        print(0)
        return
    
    # Union-Find
    parent = list(range(26))
    rank = [0] * 26
    
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
    
    # Union each source with its target
    for c in range(26):
        if need[c] is not None:
            union(c, need[c])
    
    # Group edges and nodes by component root
    comp_edges = {}
    comp_nodes = {}
    for c in range(26):
        r = find(c)
        comp_nodes[r] = comp_nodes.get(r, 0) + 1
        if need[c] is not None:
            comp_edges[r] = comp_edges.get(r, 0) + 1
    
    # Count components with cycles
    # In a functional graph (each node has out-degree 0 or 1), a component has a cycle
    # iff the number of edges equals the number of nodes.
    # Self-loops (c == need[c]) are not counted as edges, so any cycle has length >= 2.
    extras = 0
    for r, e in comp_edges.items():
        if e == comp_nodes[r]:
            extras += 1
    
    print(edges + extras)

solve()