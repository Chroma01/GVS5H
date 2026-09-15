import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos]); pos += 1
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = int(data[pos]) - 1; pos += 1
        b = int(data[pos]) - 1; pos += 1
        adj[a].append(b)
        adj[b].append(a)

    # Smallest valid alkane = star K1,4 with 5 vertices.
    if n < 5:
        sys.stdout.write("-1")
        return

    # Root the host tree at 0, get pre-order and parents iteratively.
    parent = [-1] * n
    order = []
    visited = bytearray(n)
    stack = [0]
    visited[0] = 1
    while stack:
        v = stack.pop()
        order.append(v)
        for w in adj[v]:
            if not visited[w]:
                visited[w] = 1
                parent[w] = v
                stack.append(w)

    # up[v] = f(v, parent[v]): best size of v's branch when the edge to its
    # parent is used.  v is a leaf (value 1) or an internal vertex needing
    # exactly 3 child branches (value 1 + top-3 children).
    up = [1] * n
    for v in reversed(order):
        p = parent[v]
        if p == -1:
            continue
        m1 = m2 = m3 = -1
        for w in adj[v]:
            if w == p:
                continue
            val = up[w]
            if val > m1:
                m3 = m2; m2 = m1; m1 = val
            elif val > m2:
                m3 = m2; m2 = val
            elif val > m3:
                m3 = val
        if m3 > 0:
            up[v] = 1 + m1 + m2 + m3

    # pm[v] = f(parent[v], v): message from parent down to v.
    pm = [1] * n
    ans = -1
    for v in order:
        p = parent[v]
        neigh_vals = []
        for w in adj[v]:
            if w == p:
                neigh_vals.append(pm[v])
            else:
                neigh_vals.append(up[w])
        m = len(neigh_vals)

        if m >= 4:
            # top-4 of incoming messages  (for v as the alkane root)
            bv0 = bv1 = bv2 = bv3 = -1
            bi0 = bi1 = bi2 = bi3 = -1
            for i in range(m):
                val = neigh_vals[i]
                if val > bv0:
                    bv3, bv2, bv1 = bv2, bv1, bv0
                    bi3, bi2, bi1 = bi2, bi1, bi0
                    bv0 = val; bi0 = i
                elif val > bv1:
                    bv3, bv2 = bv2, bv1
                    bi3, bi2 = bi2, bi1
                    bv1 = val; bi1 = i
                elif val > bv2:
                    bv3 = bv2; bi3 = bi2
                    bv2 = val; bi2 = i
                elif val > bv3:
                    bv3 = val; bi3 = i
            cand = 1 + bv0 + bv1 + bv2 + bv3
            if cand > ans:
                ans = cand

            # top-3 excluding each child, to build down messages
            for i, w in enumerate(adj[v]):
                if w == p:
                    continue
                s = 0; cnt = 0
                if bi0 != i:
                    s += bv0; cnt += 1
                if bi1 != i:
                    s += bv1; cnt += 1
                if bi2 != i:
                    s += bv2; cnt += 1
                if cnt == 3:
                    pm[w] = 1 + s
                else:
                    if bi3 != i:
                        s += bv3
                    pm[w] = 1 + s

    sys.stdout.write(str(ans))

main()