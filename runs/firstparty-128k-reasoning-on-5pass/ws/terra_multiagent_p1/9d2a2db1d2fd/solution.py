import sys
from array import array

def main():
    input = sys.stdin.buffer.readline

    H, W = map(int, input().split())
    N = H * W
    F = [0] * N
    for i in range(H):
        row = list(map(int, input().split()))
        F[i * W:(i + 1) * W] = row

    # Encode edges as:
    # (weight << 36) | (u << 18) | v
    # N <= 250000 < 2^18.
    SHIFT = 18
    MASK = (1 << SHIFT) - 1
    edges = []

    for r in range(H):
        base = r * W
        for c in range(W):
            u = base + c
            if c + 1 < W:
                v = u + 1
                w = F[u] if F[u] < F[v] else F[v]
                edges.append((w << 36) | (u << SHIFT) | v)
            if r + 1 < H:
                v = u + W
                w = F[u] if F[u] < F[v] else F[v]
                edges.append((w << 36) | (u << SHIFT) | v)

    edges.sort(reverse=True)

    # DSU: negative size at roots.
    dsu = array('i', [-1]) * N

    def find(x):
        root = x
        while dsu[root] >= 0:
            root = dsu[root]
        while x != root:
            px = dsu[x]
            dsu[x] = root
            x = px
        return root

    # Compact adjacency representation of maximum spanning tree.
    head = array('i', [-1]) * N
    to = array('i')
    nxt = array('i')
    ew = array('i')

    used = 0
    for code in edges:
        v = code & MASK
        u = (code >> SHIFT) & MASK
        w = code >> 36

        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        if dsu[ru] > dsu[rv]:
            ru, rv = rv, ru
        dsu[ru] += dsu[rv]
        dsu[rv] = ru

        to.append(v)
        ew.append(w)
        nxt.append(head[u])
        head[u] = len(to) - 1

        to.append(u)
        ew.append(w)
        nxt.append(head[v])
        head[v] = len(to) - 1

        used += 1
        if used == N - 1:
            break

    INF = 1_000_000_007

    # Root the tree at vertex 0.
    depth = array('i', [0]) * N
    up0 = array('i', [0]) * N
    mn0 = array('i', [INF]) * N

    stack = [0]
    while stack:
        u = stack.pop()
        e = head[u]
        parent = up0[u]
        while e != -1:
            v = to[e]
            if v != parent:
                up0[v] = u
                depth[v] = depth[u] + 1
                mn0[v] = ew[e]
                stack.append(v)
            e = nxt[e]

    LOG = N.bit_length()
    up = [up0]
    mn = [mn0]

    for _ in range(1, LOG):
        prev_up = up[-1]
        prev_mn = mn[-1]
        cur_up = array('i', [0]) * N
        cur_mn = array('i', [INF]) * N

        for i in range(N):
            p = prev_up[i]
            cur_up[i] = prev_up[p]
            a = prev_mn[i]
            b = prev_mn[p]
            cur_mn[i] = a if a < b else b

        up.append(cur_up)
        mn.append(cur_mn)

    Q = int(input())
    out = []

    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)

        if u == v:
            threshold = INF
        else:
            ans_min = INF

            if depth[u] < depth[v]:
                u, v = v, u

            diff = depth[u] - depth[v]
            bit = 0
            while diff:
                if diff & 1:
                    val = mn[bit][u]
                    if val < ans_min:
                        ans_min = val
                    u = up[bit][u]
                diff >>= 1
                bit += 1

            if u != v:
                for k in range(LOG - 1, -1, -1):
                    pu = up[k][u]
                    pv = up[k][v]
                    if pu != pv:
                        val = mn[k][u]
                        if val < ans_min:
                            ans_min = val
                        val = mn[k][v]
                        if val < ans_min:
                            ans_min = val
                        u = pu
                        v = pv

                val = mn[0][u]
                if val < ans_min:
                    ans_min = val
                val = mn[0][v]
                if val < ans_min:
                    ans_min = val

            threshold = ans_min

        low = Y if Y < Z else Z
        result = abs(Y - Z)
        if low > threshold:
            result += 2 * (low - threshold)
        out.append(str(result))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()