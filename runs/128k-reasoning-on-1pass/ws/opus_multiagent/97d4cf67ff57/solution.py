import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        print(-1)
        return
    n = int(data[0])
    if n < 5:
        # need at least one vertex of degree 4 -> at least 5 vertices
        print(-1)
        return
    m = n - 1
    vals = data[1:1 + 2 * m]
    # parse edges
    ea = [0] * m
    eb = [0] * m
    deg = [0] * (n + 1)
    idx = 0
    for i in range(m):
        a = int(vals[idx]); b = int(vals[idx + 1]); idx += 2
        ea[i] = a; eb[i] = b
        deg[a] += 1
        deg[b] += 1

    good = bytearray(n + 1)
    any_good = False
    for v in range(1, n + 1):
        if deg[v] >= 4:
            good[v] = 1
            any_good = True
    if not any_good:
        print(-1)
        return

    # build CSR on edges with both endpoints good
    cnt = [0] * (n + 2)
    for i in range(m):
        a = ea[i]; b = eb[i]
        if good[a] and good[b]:
            cnt[a] += 1
            cnt[b] += 1
    start = [0] * (n + 2)
    s = 0
    for v in range(1, n + 1):
        start[v] = s
        s += cnt[v]
    start[n + 1] = s
    pos = start[:]  # copy
    adj = [0] * s
    for i in range(m):
        a = ea[i]; b = eb[i]
        if good[a] and good[b]:
            adj[pos[a]] = b
            pos[a] += 1
            adj[pos[b]] = a
            pos[b] += 1

    parent = [0] * (n + 1)
    visited = bytearray(n + 1)
    order = []
    order_append = order.append

    for root in range(1, n + 1):
        if not good[root] or visited[root]:
            continue
        visited[root] = 1
        parent[root] = 0
        stack = [root]
        while stack:
            v = stack.pop()
            order_append(v)
            for j in range(start[v], start[v] + cnt[v]):
                u = adj[j]
                if not visited[u]:
                    visited[u] = 1
                    parent[u] = v
                    stack.append(u)

    b1 = [0] * (n + 1)
    b2 = [0] * (n + 1)
    b3 = [0] * (n + 1)
    b4 = [0] * (n + 1)

    best = 0
    for k in range(len(order) - 1, -1, -1):
        v = order[k]
        x1 = b1[v]; x2 = b2[v]; x3 = b3[v]; x4 = b4[v]
        cand = 1 + x1 + x2 + x3 + x4
        if cand > best:
            best = cand
        dpv = 1 + x1 + x2 + x3
        p = parent[v]
        if p:
            # insert dpv into top-4 of p
            if dpv > b1[p]:
                b4[p] = b3[p]; b3[p] = b2[p]; b2[p] = b1[p]; b1[p] = dpv
            elif dpv > b2[p]:
                b4[p] = b3[p]; b3[p] = b2[p]; b2[p] = dpv
            elif dpv > b3[p]:
                b4[p] = b3[p]; b3[p] = dpv
            elif dpv > b4[p]:
                b4[p] = dpv

    if best <= 0:
        print(-1)
    else:
        print(3 * best + 2)

main()