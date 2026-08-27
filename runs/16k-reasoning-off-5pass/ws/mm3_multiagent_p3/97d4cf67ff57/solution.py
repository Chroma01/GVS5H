import sys

def solve():
    import sys
    input_data = sys.stdin.buffer.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    g = [[] for _ in range(N+1)]
    for _ in range(N-1):
        a = int(next(it)); b = int(next(it))
        g[a].append(b)
        g[b].append(a)

    if N < 5:
        print(-1)
        return

    # Root the tree at node 1 using iterative DFS
    parent = [0]*(N+1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if v != parent[u]:
                parent[v] = u
                stack.append(v)

    children = [[] for _ in range(N+1)]
    for u in range(1, N+1):
        for v in g[u]:
            if v != parent[u]:
                children[u].append(v)

    NEG = -10**9

    # dp0[u]: (size, has_hub) best alkane in subtree of u where edge (parent, u) is NOT used.
    #          u may be absent (size=0) or present as a hub using 4 child edges.
    # dp1[u]: edge to parent IS used, u is present. u uses 0 child edges (leaf) or 3 child edges (hub).
    # dp2[u]: same as dp1 but u MUST be a hub (3 child edges used) -- for propagation.

    dp0 = [(0, 0)]*(N+1)
    dp1 = [(0, 0)]*(N+1)
    dp2 = [(NEG, 0)]*(N+1)

    for u in reversed(order):
        ch = children[u]
        if not ch:
            dp0[u] = (0, 0)
            dp1[u] = (1, 0)
            dp2[u] = (NEG, 0)
            continue

        # Candidate: including child c via edge (u,c) contributes dp1[c] + 1 (vertex c).
        vals = []
        for c in ch:
            s, h = dp1[c]
            vals.append((s + 1, h))
        vals.sort(key=lambda x: -x[0])

        def topk(k):
            """Return (size, has_hub) summing top k vals, or (NEG, 0) if fewer than k vals."""
            if len(vals) < k:
                return (NEG, 0)
            total_s = 0
            total_h = 0
            for i in range(k):
                total_s += vals[i][0]
                total_h |= vals[i][1]
            return (total_s, total_h)

        best1 = topk(1)
        best3 = topk(3)
        best4 = topk(4)

        # dp2: u is a hub, uses exactly 3 children, parent edge is used.
        if best3[0] > NEG:
            dp2[u] = (1 + best3[0], 1)
        else:
            dp2[u] = (NEG, 0)

        # dp1: u present, parent edge used. Options: leaf (size=1, hub=0) or hub (size=1+best3, hub=1).
        leaf_opt = (1, 0)
        hub_opt1 = (1 + best3[0], 1) if best3[0] > NEG else (NEG, 0)
        if hub_opt1[0] > leaf_opt[0]:
            dp1[u] = hub_opt1
        elif hub_opt1[0] == leaf_opt[0] and hub_opt1[1] > leaf_opt[1]:
            dp1[u] = hub_opt1
        else:
            dp1[u] = leaf_opt

        # dp0: parent edge NOT used. Options: u absent (size=0, hub=0) or u is hub using 4 children.
        absent = (0, 0)
        hub_opt0 = (1 + best4[0], 1) if best4[0] > NEG else (NEG, 0)
        if hub_opt0[0] > absent[0]:
            dp0[u] = hub_opt0
        elif hub_opt0[0] == absent[0] and hub_opt0[1] > absent[1]:
            dp0[u] = hub_opt0
        else:
            dp0[u] = absent

    # Find best valid alkane anywhere. dp0[u] for any node u represents a valid alkane
    # entirely within u's subtree (since edge to parent is not used, the subgraph is
    # self-contained). We need has_hub=True and size >= 5.
    best_size = NEG
    best_hub = 0
    for u in range(1, N+1):
        s, h = dp0[u]
        if s > best_size or (s == best_size and h > best_hub):
            best_size = s
            best_hub = h

    if best_size < 5 or best_hub == 0:
        print(-1)
    else:
        print(best_size)

solve()