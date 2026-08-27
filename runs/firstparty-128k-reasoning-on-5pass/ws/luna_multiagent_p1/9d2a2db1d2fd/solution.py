import sys
from array import array


def int_stream(data):
    n = len(data)
    i = 0
    while i < n:
        while i < n and data[i] <= 32:
            i += 1
        if i >= n:
            return
        x = 0
        while i < n and data[i] > 32:
            x = x * 10 + data[i] - 48
            i += 1
        yield x


def solve():
    data = sys.stdin.buffer.read()
    it = int_stream(data)

    H = next(it)
    W = next(it)
    N = H * W

    floors = array("i", (next(it) for _ in range(N)))

    horizontal_count = H * (W - 1)
    edge_count = horizontal_count + (H - 1) * W

    edges = []

    for r in range(H):
        base = r * W
        for c in range(W - 1):
            u = base + c
            w = min(floors[u], floors[u + 1])
            edges.append(w * edge_count + (u - r))

    for r in range(H - 1):
        base = r * W
        for c in range(W):
            u = base + c
            w = min(floors[u], floors[u + W])
            eid = horizontal_count + r * W + c
            edges.append(w * edge_count + eid)

    # Maximum spanning tree: process edges by descending weight.
    edges.sort(reverse=True)

    total = 2 * N - 1
    tree_parent = array("i", [-1]) * total
    node_value = array("i", [0]) * total

    for i in range(N):
        node_value[i] = floors[i]

    dsu_parent = array("i", range(N))
    component_root = array("i", range(N))

    def find(x):
        while dsu_parent[x] != x:
            dsu_parent[x] = dsu_parent[dsu_parent[x]]
            x = dsu_parent[x]
        return x

    next_node = N

    for encoded in edges:
        eid = encoded % edge_count
        weight = encoded // edge_count

        if eid < horizontal_count:
            r, c = divmod(eid, W - 1)
            u = r * W + c
            v = u + 1
        else:
            k = eid - horizontal_count
            r, c = divmod(k, W)
            u = r * W + c
            v = u + W

        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        left = component_root[ru]
        right = component_root[rv]

        node = next_node
        next_node += 1
        node_value[node] = weight
        tree_parent[left] = node
        tree_parent[right] = node
        tree_parent[node] = node

        dsu_parent[ru] = rv
        component_root[rv] = node

    del edges
    del dsu_parent
    del component_root
    del floors

    depth = array("i", [0]) * total
    for node in range(total - 2, -1, -1):
        depth[node] = depth[tree_parent[node]] + 1

    levels = total.bit_length()
    ancestors = [tree_parent]

    for _ in range(1, levels):
        prev = ancestors[-1]
        cur = array("i", [0]) * total
        for i in range(total):
            cur[i] = prev[prev[i]]
        ancestors.append(cur)

    Q = next(it)
    out = []
    max_level = levels - 1

    for _ in range(Q):
        a = next(it) - 1
        b = next(it) - 1
        y = next(it)
        c = next(it) - 1
        d = next(it) - 1
        z = next(it)

        start = a * W + b
        goal = c * W + d

        if start == goal:
            out.append(str(abs(y - z)))
            continue

        x = start
        w = goal

        if depth[x] < depth[w]:
            x, w = w, x

        diff = depth[x] - depth[w]
        bit = 0
        while diff:
            if diff & 1:
                x = ancestors[bit][x]
            diff >>= 1
            bit += 1

        if x != w:
            for level in range(max_level, -1, -1):
                ax = ancestors[level][x]
                aw = ancestors[level][w]
                if ax != aw:
                    x = ax
                    w = aw
            x = ancestors[0][x]

        bottleneck = node_value[x]
        low = min(y, z)

        if bottleneck >= low:
            answer = abs(y - z)
        else:
            answer = y + z - 2 * bottleneck

        out.append(str(answer))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()