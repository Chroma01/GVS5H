import sys
from array import array

def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    n = H * W

    heights = []
    for _ in range(H):
        heights.extend(map(int, input().split()))

    order = list(range(n))
    order.sort(key=heights.__getitem__, reverse=True)

    # DSU is maintained over original cells. For each DSU component, comp_tree
    # stores the corresponding node of the Kruskal reconstruction tree.
    dsu = array('i', [0]) * n
    comp_tree = array('i', range(n))
    active = bytearray(n)

    total_capacity = 2 * n
    parent = array('i', [-1]) * total_capacity
    value = array('i', heights)
    if n > 1:
        value.extend([0] * (n - 1))

    next_node = n

    def find(x):
        while dsu[x] >= 0:
            if dsu[dsu[x]] >= 0:
                dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    def unite(a, b, level):
        nonlocal next_node
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return

        node = next_node
        next_node += 1
        value[node] = level
        parent[comp_tree[ra]] = node
        parent[comp_tree[rb]] = node

        if dsu[ra] > dsu[rb]:
            ra, rb = rb, ra
        dsu[ra] += dsu[rb]
        dsu[rb] = ra
        comp_tree[ra] = node

    for v in order:
        active[v] = 1
        dsu[v] = -1
        level = heights[v]
        r = v // W
        c = v - r * W

        if r > 0:
            u = v - W
            if active[u]:
                unite(v, u, level)
        if r + 1 < H:
            u = v + W
            if active[u]:
                unite(v, u, level)
        if c > 0:
            u = v - 1
            if active[u]:
                unite(v, u, level)
        if c + 1 < W:
            u = v + 1
            if active[u]:
                unite(v, u, level)

    root = comp_tree[find(0)]
    total = next_node
    parent[root] = root

    # Every internal node was created after its children, so iterating downwards
    # computes depths directly from parent pointers.
    depth = array('i', [0]) * total
    for v in range(total - 1, -1, -1):
        if v != root:
            depth[v] = depth[parent[v]] + 1

    up = [array('i', parent[:total])]
    LOG = total.bit_length()
    for _ in range(1, LOG):
        prev = up[-1]
        up.append(array('i', (prev[prev[i]] for i in range(total))))

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        if a == b:
            return a

        for k in range(LOG - 1, -1, -1):
            na = up[k][a]
            nb = up[k][b]
            if na != nb:
                a = na
                b = nb
        return up[0][a]

    Q = int(input())
    out = []

    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        s = (A - 1) * W + (B - 1)
        t = (C - 1) * W + (D - 1)

        threshold = value[lca(s, t)]
        lowest_needed = min(threshold, Y, Z)
        out.append(str(Y + Z - 2 * lowest_needed))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()