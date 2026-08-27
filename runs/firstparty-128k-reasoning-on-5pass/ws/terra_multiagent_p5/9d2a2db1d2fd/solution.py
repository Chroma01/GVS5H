import sys
from array import array

def main():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    N = H * W

    heights = array('i')
    for _ in range(H):
        heights.extend(map(int, input().split()))

    Q = int(input())

    # Build a union tree while activating buildings in descending height order.
    # The LCA label of two original vertices is their maximum common
    # walkway-connected floor.
    order = list(range(N))
    order.sort(key=heights.__getitem__, reverse=True)

    dsu = array('i', range(N))
    comp_node = array('i', range(N))
    active = bytearray(N)

    tree_parent = array('i', [-1]) * (2 * N)
    value = array('i', [0]) * (2 * N)
    value[:N] = heights

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    total = N

    for v in order:
        active[v] = 1
        h = heights[v]

        if v >= W and active[v - W]:
            a = find(v)
            b = find(v - W)
            if a != b:
                node = total
                total += 1
                value[node] = h
                tree_parent[comp_node[a]] = node
                tree_parent[comp_node[b]] = node
                dsu[b] = a
                comp_node[a] = node

        if v + W < N and active[v + W]:
            a = find(v)
            b = find(v + W)
            if a != b:
                node = total
                total += 1
                value[node] = h
                tree_parent[comp_node[a]] = node
                tree_parent[comp_node[b]] = node
                dsu[b] = a
                comp_node[a] = node

        if v % W != 0 and active[v - 1]:
            a = find(v)
            b = find(v - 1)
            if a != b:
                node = total
                total += 1
                value[node] = h
                tree_parent[comp_node[a]] = node
                tree_parent[comp_node[b]] = node
                dsu[b] = a
                comp_node[a] = node

        if v % W != W - 1 and active[v + 1]:
            a = find(v)
            b = find(v + 1)
            if a != b:
                node = total
                total += 1
                value[node] = h
                tree_parent[comp_node[a]] = node
                tree_parent[comp_node[b]] = node
                dsu[b] = a
                comp_node[a] = node

    root = comp_node[find(0)]
    tree_parent[root] = root

    del order, heights, dsu, comp_node, active

    up0 = tree_parent[:total]
    del tree_parent

    depth = array('i', [0]) * total
    for v in range(total - 2, -1, -1):
        depth[v] = depth[up0[v]] + 1

    LOG = total.bit_length()
    up = [up0]
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

    out = []
    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        s = (A - 1) * W + (B - 1)
        t = (C - 1) * W + (D - 1)

        common_floor = value[lca(s, t)]
        low = Y if Y < Z else Z

        if common_floor >= low:
            ans = Y - Z if Y >= Z else Z - Y
        else:
            ans = Y + Z - 2 * common_floor

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()