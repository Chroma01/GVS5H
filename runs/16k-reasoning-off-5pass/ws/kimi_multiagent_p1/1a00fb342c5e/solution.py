import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    parent = list(range(N + 1))
    size = [1] * (N + 1)
    d = [0] * (N + 1)  # d[v] = A_v XOR A_root(v)

    def find(x):
        # returns (root, xor from x to root), with path compression
        if parent[x] == x:
            return x, 0
        path = []
        node = x
        acc = 0
        while parent[node] != node:
            path.append(node)
            acc ^= d[node]
            node = parent[node]
        root = node
        # acc = xor from x to root
        # compress: for each v on path, xor from v to root = (xor x->v) ^ (xor x->root)
        cur = 0
        for v in path:
            old_d = d[v]
            parent[v] = root
            d[v] = cur ^ acc
            cur ^= old_d
        return root, acc

    def union(x, y, z):
        rx, dx = find(x)
        ry, dy = find(y)
        if rx == ry:
            return (dx ^ dy) == z
        # attach smaller under larger
        if size[rx] < size[ry]:
            rx, ry = ry, rx
            dx, dy = dy, dx
        parent[ry] = rx
        d[ry] = dx ^ dy ^ z
        size[rx] += size[ry]
        return True

    ok = True
    for i in range(M):
        x = int(next(it)); y = int(next(it)); z = int(next(it))
        if ok:
            if not union(x, y, z):
                ok = False
        # if not ok, tokens are still consumed by next(it) above; just skip union work

    if not ok:
        sys.stdout.write("-1\n")
        return

    # group vertices by root, finalizing xor-to-root values
    comp = {}
    for v in range(1, N + 1):
        r, _ = find(v)
        if r in comp:
            comp[r].append(v)
        else:
            comp[r] = [v]

    ans = [0] * (N + 1)
    B = 30  # Z_i <= 1e9 < 2^30
    for r, members in comp.items():
        sz = len(members)
        t = 0
        for k in range(B):
            bit = 1 << k
            c = 0
            for v in members:
                if d[v] & bit:
                    c += 1
            if c > sz - c:
                t |= bit
        for v in members:
            ans[v] = t ^ d[v]

    sys.stdout.write(' '.join(str(ans[i]) for i in range(1, N + 1)) + '\n')

main()