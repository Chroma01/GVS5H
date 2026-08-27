import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    parent = list(range(N + 1))
    xr = [0] * (N + 1)   # xor from node to its parent
    rank = [0] * (N + 1)
    touched = [False] * (N + 1)

    def find(x):
        # returns (root, xor from x to root), with path compression
        if parent[x] == x:
            return x, 0
        root = x
        acc = 0
        while parent[root] != root:
            acc ^= xr[root]
            root = parent[root]
        # compress: node originally had xor cur to old parent chain start;
        # after compression, xr[node] = xor from node to root = acc ^ (xor from x to node)
        node = x
        cur = 0
        while parent[node] != root:
            nxt = parent[node]
            nxr = xr[node]
            parent[node] = root
            xr[node] = acc ^ cur
            cur ^= nxr
            node = nxt
        return root, acc

    ok = True
    for _ in range(M):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        touched[x] = True
        touched[y] = True
        if not ok:
            continue
        if x == y:
            if z != 0:
                ok = False
            continue
        rx, mx = find(x)
        ry, my = find(y)
        if rx == ry:
            if (mx ^ my) != z:
                ok = False
        else:
            if rank[rx] < rank[ry]:
                rx, ry = ry, rx
                mx, my = my, mx
            parent[ry] = rx
            xr[ry] = mx ^ my ^ z
            if rank[rx] == rank[ry]:
                rank[rx] += 1

    if not ok:
        sys.stdout.write("-1\n")
        return

    # group touched vertices by root
    groups = {}
    for v in range(1, N + 1):
        if not touched[v]:
            continue
        r, m = find(v)
        if r in groups:
            groups[r].append((v, m))
        else:
            groups[r] = [(v, m)]

    A = [0] * (N + 1)
    B = 30  # Z <= 1e9 < 2^30
    for r, members in groups.items():
        s = len(members)
        cnt = [0] * B
        for v, m in members:
            mm = m
            while mm:
                lb = mm & (-mm)
                b = lb.bit_length() - 1
                cnt[b] += 1
                mm ^= lb
        rval = 0
        for b in range(B):
            c = cnt[b]
            if s - c < c:
                rval |= (1 << b)
        for v, m in members:
            A[v] = m ^ rval

    out = ' '.join(str(A[i]) for i in range(1, N + 1))
    sys.stdout.write(out + "\n")

main()