import sys
from array import array

def solve():
    data = sys.stdin.buffer.read()
    pos = 0
    length = len(data)

    def next_int():
        nonlocal pos
        while pos < length and data[pos] <= 32:
            pos += 1
        value = 0
        while pos < length and data[pos] > 32:
            value = value * 10 + data[pos] - 48
            pos += 1
        return value

    H = next_int()
    W = next_int()
    N = H * W

    floors = [next_int() for _ in range(N)]

    # Encode each grid edge as:
    # (weight << 19) | (cell_index << 1) | direction
    # direction 0 = right, 1 = down
    SHIFT = 19
    MASK = (1 << SHIFT) - 1
    edges = []

    for i in range(N):
        r = i // W
        c = i - r * W

        if c + 1 < W:
            j = i + 1
            edges.append((min(floors[i], floors[j]) << SHIFT) | (i << 1))

        if r + 1 < H:
            j = i + W
            edges.append((min(floors[i], floors[j]) << SHIFT) | (i << 1) | 1)

    edges.sort(reverse=True)

    total = 2 * N - 1
    node_weight = array('i', [0]) * total
    node_parent = array('i', [-1]) * total
    left_child = array('i', [-1]) * total
    right_child = array('i', [-1]) * total

    for i, f in enumerate(floors):
        node_weight[i] = f

    dsu = array('i', [-1]) * N
    component_root = array('i', range(N))

    def find(x):
        while dsu[x] >= 0:
            p = dsu[x]
            if dsu[p] >= 0:
                dsu[x] = dsu[p]
            x = p
        return x

    next_node = N

    for encoded in edges:
        u = (encoded & MASK) >> 1
        if encoded & 1:
            v = u + W
        else:
            v = u + 1
        weight = encoded >> SHIFT

        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        # Union by component size.
        if dsu[ru] > dsu[rv]:
            ru, rv = rv, ru

        a = component_root[ru]
        b = component_root[rv]
        k = next_node
        next_node += 1

        left_child[k] = a
        right_child[k] = b
        node_weight[k] = weight
        node_parent[a] = k
        node_parent[b] = k

        dsu[ru] += dsu[rv]
        dsu[rv] = ru
        component_root[ru] = k

        if next_node == total:
            break

    root = next_node - 1

    # Parent indices are always larger than child indices in the
    # Kruskal reconstruction tree, so depths can be computed backwards.
    depth = array('i', [0]) * total
    for i in range(total - 1, -1, -1):
        p = node_parent[i]
        if p >= 0:
            depth[i] = depth[p] + 1

    node_parent[root] = root
    up = [node_parent]

    max_log = total.bit_length()
    for _ in range(1, max_log):
        prev = up[-1]
        cur = array('i', (prev[prev[i]] for i in range(total)))
        up.append(cur)

    Q = next_int()
    answers = []

    for _ in range(Q):
        a = next_int() - 1
        b = next_int() - 1
        y = next_int()
        c = next_int() - 1
        d = next_int() - 1
        z = next_int()

        x = a * W + b
        t = c * W + d

        if depth[x] < depth[t]:
            x, t = t, x

        diff = depth[x] - depth[t]
        bit = 0
        while diff:
            if diff & 1:
                x = up[bit][x]
            diff >>= 1
            bit += 1

        if x != t:
            for k in range(max_log - 1, -1, -1):
                ux = up[k][x]
                ut = up[k][t]
                if ux != ut:
                    x = ux
                    t = ut
            lca = up[0][x]
        else:
            lca = x

        bottleneck = node_weight[lca]
        common_level = min(y, z, bottleneck)
        answers.append(str(y + z - 2 * common_level))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()