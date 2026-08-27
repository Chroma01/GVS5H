import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    N = next(it); M = next(it); K = next(it)

    edges = []
    for _ in range(M):
        u = next(it) - 1
        v = next(it) - 1
        w = next(it)
        edges.append((w, u, v))

    A = [next(it) - 1 for _ in range(K)]
    B = [next(it) - 1 for _ in range(K)]

    edges.sort(key=lambda x: x[0])

    parent = list(range(N))
    size = [1] * N
    comp_node = list(range(N))

    total_nodes = 2 * N
    weight = [0] * total_nodes
    left_child = [-1] * total_nodes
    right_child = [-1] * total_nodes
    red = [0] * total_nodes
    blue = [0] * total_nodes

    for a in A:
        red[a] += 1
    for b in B:
        blue[b] += 1

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    cur = N  # next new node index
    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue
        node_u = comp_node[ru]
        node_v = comp_node[rv]
        nid = cur
        cur += 1
        weight[nid] = w
        left_child[nid] = node_u
        right_child[nid] = node_v

        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        comp_node[ru] = nid

    ans = 0
    for nid in range(N, cur):
        l = left_child[nid]
        r = right_child[nid]
        rl = red[l]
        bl = blue[l]
        rr = red[r]
        br = blue[r]

        m1 = rl if rl < br else br
        m2 = rr if rr < bl else bl
        matches = m1 + m2

        ans += matches * weight[nid]
        red[nid] = rl + rr - matches
        blue[nid] = bl + br - matches

    print(ans)

if __name__ == "__main__":
    solve()