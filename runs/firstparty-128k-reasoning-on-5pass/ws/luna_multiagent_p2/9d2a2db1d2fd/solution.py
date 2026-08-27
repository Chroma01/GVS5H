import sys
from array import array


def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    n = H * W

    floors = []
    for _ in range(H):
        floors.extend(map(int, input().split()))

    edges = []
    for r in range(H):
        base = r * W
        for c in range(W):
            u = base + c
            if c + 1 < W:
                v = u + 1
                edges.append((min(floors[u], floors[v]), u, v))
            if r + 1 < H:
                v = u + W
                edges.append((min(floors[u], floors[v]), u, v))

    edges.sort(reverse=True)

    total = 2 * n - 1
    tree_parent = array('i', [-1]) * total
    node_weight = array('i', [0]) * total

    dsu = array('i', range(total))

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    next_node = n
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        x = next_node
        next_node += 1

        tree_parent[ru] = x
        tree_parent[rv] = x
        node_weight[x] = w

        dsu[ru] = x
        dsu[rv] = x
        dsu[x] = x

        if next_node == total:
            break

    # Compute depths. Every parent has a larger node index than its children.
    depth = array('i', [0]) * total
    for x in range(total - 1, -1, -1):
        p = tree_parent[x]
        if p != -1:
            depth[x] = depth[p] + 1

    log = total.bit_length()
    up = [tree_parent]
    for _ in range(1, log):
        prev = up[-1]
        cur = array(
            'i',
            (
                -1 if prev[i] == -1 else prev[prev[i]]
                for i in range(total)
            )
        )
        up.append(cur)

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

        for k in range(log - 1, -1, -1):
            pa = up[k][a]
            pb = up[k][b]
            if pa != pb and pa != -1 and pb != -1:
                a = pa
                b = pb

        return tree_parent[a]

    q = int(input())
    out = []

    for _ in range(q):
        a, b, y, c, d, z = map(int, input().split())
        s = (a - 1) * W + (b - 1)
        t = (c - 1) * W + (d - 1)

        if s == t:
            out.append(str(abs(y - z)))
        else:
            bottleneck = node_weight[lca(s, t)]
            out.append(str(y + z - 2 * min(y, z, bottleneck)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()