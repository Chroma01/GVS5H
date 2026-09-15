import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    if n < 5:
        sys.stdout.write("-1\n")
        return

    adj = [[] for _ in range(n)]
    idx = 1
    for _ in range(n - 1):
        a = int(data[idx]) - 1
        b = int(data[idx + 1]) - 1
        idx += 2
        adj[a].append(b)
        adj[b].append(a)

    # BFS to fix parent and order (iterative, no recursion depth issues)
    parent = [-1] * n
    order = []
    visited = [False] * n
    dq = deque([0])
    visited[0] = True
    while dq:
        u = dq.popleft()
        order.append(u)
        for w in adj[u]:
            if not visited[w]:
                visited[w] = True
                parent[w] = u
                dq.append(w)

    # down[v] = h(v, parent[v]): best full-ternary branch rooted at v, away from parent.
    # h(v,p) = 1 if v has < 3 neighbours besides p, else 1 + (sum of 3 largest h(c,v)).
    down = [1] * n
    for v in reversed(order):
        pu = parent[v]
        vals = []
        for w in adj[v]:
            if w != pu:
                vals.append(down[w])
        if len(vals) >= 3:
            vals.sort(reverse=True)
            down[v] = 1 + vals[0] + vals[1] + vals[2]

    # up[v] = h(parent[v], v): branch rooted at parent, away from v (rerooting / top-down pass).
    up = [0] * n
    for u in order:
        pu = parent[u]
        nl = []
        if pu != -1:
            nl.append((up[u], pu))
        for w in adj[u]:
            if w != pu:
                nl.append((down[w], w))
        total = len(nl)  # == deg(u)
        nl.sort(key=lambda t: -t[0])
        top4 = nl[:4]  # top-4 is enough to get top-3 after removing any single source
        for w in adj[u]:
            if w == pu:
                continue
            if total - 1 >= 3:
                s = 0
                cnt = 0
                for val, src in top4:
                    if src == w:
                        continue
                    s += val
                    cnt += 1
                    if cnt == 3:
                        break
                up[w] = 1 + s
            else:
                up[w] = 1

    # Answer: pick internal root R (deg >= 4), its leaf L = smallest-valued neighbour,
    # and the three largest branches as R's children.
    ans = -1
    for R in range(n):
        if len(adj[R]) < 4:
            continue
        pu = parent[R]
        vals = []
        for w in adj[R]:
            if w == pu:
                vals.append(up[R])
            else:
                vals.append(down[w])
        vals.sort(reverse=True)
        cand = 2 + vals[0] + vals[1] + vals[2]
        if cand > ans:
            ans = cand

    sys.stdout.write(str(ans) + "\n")


main()