import sys
import gc
from array import array

def solve():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    N = H * W

    heights = []
    edges = []
    prev_row_start = -W

    for i in range(H):
        row = list(map(int, input().split()))
        base = i * W
        heights.extend(row)

        for j in range(W - 1):
            u = base + j
            edges.append((row[j] if row[j] < row[j + 1] else row[j + 1], u, u + 1))

        if i > 0:
            for j in range(W):
                u = base + j
                above = heights[u - W]
                cur = row[j]
                edges.append((above if above < cur else cur, u - W, u))

    edges.sort(reverse=True)

    dsu = array('i', range(N))
    size = array('i', [1]) * N

    def find(x):
        while dsu[x] != x:
            dsu[x] = dsu[dsu[x]]
            x = dsu[x]
        return x

    head = array('i', [-1]) * N
    to = array('i')
    nxt = array('i')
    cap = array('i')

    used = 0
    for weight, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        if size[ru] < size[rv]:
            ru, rv = rv, ru
        dsu[rv] = ru
        size[ru] += size[rv]

        to.append(v)
        cap.append(weight)
        nxt.append(head[u])
        head[u] = len(to) - 1

        to.append(u)
        cap.append(weight)
        nxt.append(head[v])
        head[v] = len(to) - 1

        used += 1
        if used == N - 1:
            break

    del edges
    del dsu
    del size
    gc.collect()

    INF = 1_000_000_007

    depth = array('i', [0]) * N
    parent0 = array('i', [-1]) * N
    min0 = array('i', [INF]) * N
    parent0[0] = 0

    stack = [0]
    while stack:
        u = stack.pop()
        e = head[u]
        pu = parent0[u]
        while e != -1:
            v = to[e]
            if v != pu:
                parent0[v] = u
                depth[v] = depth[u] + 1
                min0[v] = cap[e]
                stack.append(v)
            e = nxt[e]

    LOG = N.bit_length()
    ups = [parent0]
    mins = [min0]

    for _ in range(1, LOG):
        prev_up = ups[-1]
        prev_min = mins[-1]

        new_up = array('i', (prev_up[prev_up[i]] for i in range(N)))
        new_min = array(
            'i',
            (
                prev_min[i]
                if prev_min[i] < prev_min[prev_up[i]]
                else prev_min[prev_up[i]]
                for i in range(N)
            )
        )
        ups.append(new_up)
        mins.append(new_min)

    Q = int(input())
    out = []

    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)

        if u == v:
            level = heights[u]
        else:
            best = INF

            if depth[u] < depth[v]:
                u, v = v, u

            diff = depth[u] - depth[v]
            bit = 0
            while diff:
                if diff & 1:
                    if mins[bit][u] < best:
                        best = mins[bit][u]
                    u = ups[bit][u]
                diff >>= 1
                bit += 1

            if u != v:
                for k in range(LOG - 1, -1, -1):
                    if ups[k][u] != ups[k][v]:
                        if mins[k][u] < best:
                            best = mins[k][u]
                        if mins[k][v] < best:
                            best = mins[k][v]
                        u = ups[k][u]
                        v = ups[k][v]

                if min0[u] < best:
                    best = min0[u]
                if min0[v] < best:
                    best = min0[v]

            level = best

        lower = Y if Y < Z else Z
        if level >= lower:
            ans = Y - Z if Y >= Z else Z - Y
        else:
            ans = Y + Z - 2 * level

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()