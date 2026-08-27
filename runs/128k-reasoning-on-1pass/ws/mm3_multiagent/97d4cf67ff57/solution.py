import sys
import heapq

INF_NEG = -10 ** 9          # value meaning “impossible”

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        adj[a].append(b)
        adj[b].append(a)

    # ---------- root the tree ----------
    parent = [-1] * n
    order = []                     # preorder
    stack = [0]
    parent[0] = -2                 # mark root, no parent
    while stack:
        v = stack.pop()
        order.append(v)
        for u in adj[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            stack.append(u)

    # ---------- down DP : best3 ----------
    best3 = [INF_NEG] * n
    for v in reversed(order):       # postorder
        child_vals = []
        for u in adj[v]:
            if parent[u] == v:      # child
                val = best3[u] if best3[u] != INF_NEG else 1
                child_vals.append(val)
        if len(child_vals) >= 3:
            top3 = heapq.nlargest(3, child_vals)
            best3[v] = 1 + sum(top3)

    # ---------- up DP ----------
    up = [INF_NEG] * n
    up[0] = INF_NEG                 # root has no parent side

    for v in order:                 # preorder, parent already processed
        # build (neighbour, contribution) pairs
        neigh = []
        p = parent[v]
        if p != -2:                 # has a parent
            val = up[v] if up[v] != INF_NEG else 1
            neigh.append((p, val))
        for u in adj[v]:
            if parent[u] == v:      # child
                val = best3[u] if best3[u] != INF_NEG else 1
                neigh.append((u, val))

        if len(neigh) < 4:
            for u in adj[v]:
                if parent[u] == v:
                    up[u] = INF_NEG
            continue

        # four largest contributions
        top4 = heapq.nlargest(4, neigh, key=lambda x: x[1])
        sum_top3 = top4[0][1] + top4[1][1] + top4[2][1]
        top3_set = {top4[0][0], top4[1][0], top4[2][0]}

        for u in adj[v]:
            if parent[u] != v:
                continue
            if u not in top3_set:
                sum_excl = sum_top3
            else:
                # find u's value among the three biggest
                val_u = None
                for nid, val in top4[:3]:
                    if nid == u:
                        val_u = val
                        break
                # the fourth value always exists because len(neigh) >= 4
                next_val = top4[3][1]
                sum_excl = sum_top3 - val_u + next_val
            up[u] = 1 + sum_excl

    # ---------- final answer ----------
    answer = INF_NEG
    for v in range(n):
        # collect best3 values of all neighbour sides
        neigh_best3 = []
        for u in adj[v]:
            if parent[u] == v:          # child
                neigh_best3.append(best3[u])
        if parent[v] != -2:            # has a parent
            neigh_best3.append(up[v])

        # ----- leaf root (v is leaf) -----
        max_internal = INF_NEG
        for x in neigh_best3:
            if x != INF_NEG and x > max_internal:
                max_internal = x
        if max_internal != INF_NEG:
            leaf_best = 1 + max_internal
            if leaf_best > answer:
                answer = leaf_best

        # ----- internal root (v has degree 4 in the alkane) -----
        if len(neigh_best3) >= 4:
            # contribution of a neighbour = max(1, best3 side)
            contribs = [x if x != INF_NEG else 1 for x in neigh_best3]
            top4 = heapq.nlargest(4, contribs)
            internal_best = 1 + sum(top4)
            if internal_best > answer:
                answer = internal_best

    if answer == INF_NEG:
        print(-1)
    else:
        print(answer)

if __name__ == "__main__":
    solve()