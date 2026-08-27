import sys
from array import array

def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))

    H = next(it)
    W = next(it)
    N = H * W

    floors = [next(it) for _ in range(N)]

    # Encode each edge as:
    # (weight << 36) | (u << 18) | v
    # Since N <= 250000 < 2^18.
    SHIFT = 18
    MASK = (1 << SHIFT) - 1
    edges = []

    for r in range(H):
        row = r * W
        for c in range(W):
            u = row + c
            if c + 1 < W:
                v = u + 1
                w = floors[u] if floors[u] < floors[v] else floors[v]
                edges.append((w << (2 * SHIFT)) | (u << SHIFT) | v)
            if r + 1 < H:
                v = u + W
                w = floors[u] if floors[u] < floors[v] else floors[v]
                edges.append((w << (2 * SHIFT)) | (u << SHIFT) | v)

    edges.sort(reverse=True)

    parent_dsu = array('i', range(N))
    size_dsu = array('i', [1]) * N

    def find(x):
        y = x
        while parent_dsu[y] != y:
            y = parent_dsu[y]
        while parent_dsu[x] != x:
            p = parent_dsu[x]
            parent_dsu[x] = y
            x = p
        return y

    head = array('i', [-1]) * N
    to = array('i')
    weight = array('i')
    nxt = array('i')

    def add_edge(u, v, w):
        to.append(v)
        weight.append(w)
        nxt.append(head[u])
        head[u] = len(to) - 1

    used = 0
    for code in edges:
        w = code >> (2 * SHIFT)
        u = (code >> SHIFT) & MASK
        v = code & MASK

        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        if size_dsu[ru] < size_dsu[rv]:
            ru, rv = rv, ru
        parent_dsu[rv] = ru
        size_dsu[ru] += size_dsu[rv]

        add_edge(u, v, w)
        add_edge(v, u, w)
        used += 1
        if used == N - 1:
            break

    # Root the maximum spanning tree and prepare binary lifting tables.
    depth = array('i', [-1]) * N
    up0 = array('i', [0]) * N
    mn0 = array('i', [0]) * N

    root = 0
    depth[root] = 0
    up0[root] = root
    mn0[root] = 1_000_000_001

    stack = [root]
    while stack:
        u = stack.pop()
        e = head[u]
        while e != -1:
            v = to[e]
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                up0[v] = u
                mn0[v] = weight[e]
                stack.append(v)
            e = nxt[e]

    LOG = N.bit_length()
    ups = [up0]
    mins = [mn0]

    for _ in range(1, LOG):
        prev_up = ups[-1]
        prev_mn = mins[-1]
        cur_up = array('i', (prev_up[prev_up[i]] for i in range(N)))
        cur_mn = array(
            'i',
            (prev_mn[i] if prev_mn[i] < prev_mn[prev_up[i]]
             else prev_mn[prev_up[i]] for i in range(N))
        )
        ups.append(cur_up)
        mins.append(cur_mn)

    Q = next(it)
    out = []
    INF = 1_000_000_001

    for _ in range(Q):
        a = next(it) - 1
        b = next(it) - 1
        y = next(it)
        c = next(it) - 1
        d = next(it) - 1
        z = next(it)

        u = a * W + b
        v = c * W + d

        if u == v:
            bottleneck = INF
        else:
            bottleneck = INF
            if depth[u] < depth[v]:
                u, v = v, u

            diff = depth[u] - depth[v]
            bit = 0
            while diff:
                if diff & 1:
                    if mins[bit][u] < bottleneck:
                        bottleneck = mins[bit][u]
                    u = ups[bit][u]
                diff >>= 1
                bit += 1

            if u != v:
                for k in range(LOG - 1, -1, -1):
                    if ups[k][u] != ups[k][v]:
                        if mins[k][u] < bottleneck:
                            bottleneck = mins[k][u]
                        if mins[k][v] < bottleneck:
                            bottleneck = mins[k][v]
                        u = ups[k][u]
                        v = ups[k][v]

                if mins[0][u] < bottleneck:
                    bottleneck = mins[0][u]
                if mins[0][v] < bottleneck:
                    bottleneck = mins[0][v]

        direct = abs(y - z)
        via_lowest = y + z - 2 * bottleneck
        answer = direct if direct > via_lowest else via_lowest
        out.append(str(answer))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()