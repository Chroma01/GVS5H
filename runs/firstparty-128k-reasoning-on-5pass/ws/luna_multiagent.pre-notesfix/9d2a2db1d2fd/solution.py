import sys
from array import array


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0

    H = data[pos]
    W = data[pos + 1]
    pos += 2

    N = H * W
    height = data[pos:pos + N]
    pos += N

    edges = []

    for i in range(H):
        base = i * W
        for j in range(W - 1):
            u = base + j
            v = u + 1
            edges.append((min(height[u], height[v]), u, v))

    for i in range(H - 1):
        base = i * W
        nxt = base + W
        for j in range(W):
            u = base + j
            v = nxt + j
            edges.append((min(height[u], height[v]), u, v))

    edges.sort(reverse=True)

    dsu_parent = list(range(N))
    dsu_size = [1] * N

    def find(x):
        while dsu_parent[x] != x:
            dsu_parent[x] = dsu_parent[dsu_parent[x]]
            x = dsu_parent[x]
        return x

    adj = [[] for _ in range(N)]
    used = 0

    for cap, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        if dsu_size[ru] < dsu_size[rv]:
            ru, rv = rv, ru

        dsu_parent[rv] = ru
        dsu_size[ru] += dsu_size[rv]

        adj[u].append((v, cap))
        adj[v].append((u, cap))
        used += 1

        if used == N - 1:
            break

    parent0 = array("i", [-1]) * N
    min0 = array("i", [1000001]) * N
    depth = array("i", [0]) * N

    parent0[0] = 0
    queue = [0]
    head = 0

    while head < len(queue):
        v = queue[head]
        head += 1

        for to, cap in adj[v]:
            if to == parent0[v]:
                continue
            parent0[to] = v
            min0[to] = cap
            depth[to] = depth[v] + 1
            queue.append(to)

    del adj
    del queue
    del edges
    del dsu_parent
    del dsu_size

    LOG = N.bit_length()
    ups = [parent0]
    mins = [min0]

    for _ in range(1, LOG):
        prev_up = ups[-1]
        prev_min = mins[-1]

        cur_up = array("i", [0]) * N
        cur_min = array("i", [0]) * N

        for v in range(N):
            p = prev_up[v]
            cur_up[v] = prev_up[p]

            a = prev_min[v]
            b = prev_min[p]
            cur_min[v] = a if a < b else b

        ups.append(cur_up)
        mins.append(cur_min)

    Q = data[pos]
    pos += 1
    out = []

    for _ in range(Q):
        a = data[pos] - 1
        b = data[pos + 1] - 1
        y = data[pos + 2]
        c = data[pos + 3] - 1
        d = data[pos + 4] - 1
        z = data[pos + 5]
        pos += 6

        start = a * W + b
        goal = c * W + d

        if start == goal:
            out.append(str(abs(y - z)))
            continue

        u = start
        v = goal
        bottleneck = 1000001

        if depth[u] < depth[v]:
            u, v = v, u

        diff = depth[u] - depth[v]
        bit = 0

        while diff:
            if diff & 1:
                value = mins[bit][u]
                if value < bottleneck:
                    bottleneck = value
                u = ups[bit][u]
            diff >>= 1
            bit += 1

        if u != v:
            for k in range(LOG - 1, -1, -1):
                if ups[k][u] != ups[k][v]:
                    value = mins[k][u]
                    if value < bottleneck:
                        bottleneck = value

                    value = mins[k][v]
                    if value < bottleneck:
                        bottleneck = value

                    u = ups[k][u]
                    v = ups[k][v]

            value = mins[0][u]
            if value < bottleneck:
                bottleneck = value

            value = mins[0][v]
            if value < bottleneck:
                bottleneck = value

        low = y if y < z else z
        if bottleneck >= low:
            answer = abs(y - z)
        else:
            answer = y + z - 2 * bottleneck

        out.append(str(answer))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()