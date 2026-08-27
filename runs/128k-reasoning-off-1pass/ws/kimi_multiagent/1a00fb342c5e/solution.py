import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    parent = list(range(N + 1))
    size = [1] * (N + 1)
    pot = [0] * (N + 1)  # pot[v] = A_v XOR A_root(v)

    def find(x):
        # iterative find with path compression, maintaining xor potential to root
        if parent[x] == x:
            return x
        # find root and accumulate xor
        root = x
        acc = 0
        while parent[root] != root:
            acc ^= pot[root]
            root = parent[root]
        # compress path
        cur = x
        cur_acc = 0
        while parent[cur] != root:
            nxt = parent[cur]
            old_pot = pot[cur]
            parent[cur] = root
            pot[cur] = acc ^ cur_acc
            cur_acc ^= old_pot
            cur = nxt
        return root

    def union(x, y, z):
        # enforce A_x XOR A_y = z
        rx = find(x)
        ry = find(y)
        val = pot[x] ^ pot[y] ^ z  # required xor between roots: A_rx XOR A_ry = val
        if rx == ry:
            return val == 0
        if size[rx] < size[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        pot[ry] = val
        size[rx] += size[ry]
        return True

    ok = True
    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        z = int(next(it))
        if ok:
            if not union(x, y, z):
                ok = False

    if not ok:
        sys.stdout.write("-1\n")
        return

    # group vertices by root
    # comp_id[root] -> index; for each component store size and bit counts
    comp_index = {}
    comp_size = []
    comp_bits = []  # list of [30] counts
    root_of = [0] * (N + 1)

    for v in range(1, N + 1):
        r = find(v)
        root_of[v] = r
        idx = comp_index.get(r)
        if idx is None:
            idx = len(comp_size)
            comp_index[r] = idx
            comp_size.append(0)
            comp_bits.append([0] * 30)
        comp_size[idx] += 1
        d = pot[v]
        bits = comp_bits[idx]
        b = 0
        while d:
            if d & 1:
                bits[b] += 1
            d >>= 1
            b += 1

    # choose optimal t per component
    comp_t = [0] * len(comp_size)
    for idx in range(len(comp_size)):
        sz = comp_size[idx]
        bits = comp_bits[idx]
        t = 0
        for b in range(30):
            c = bits[b]
            # t bit = 0 -> c vertices have bit set; t bit = 1 -> sz - c
            if sz - c < c:
                t |= (1 << b)
        comp_t[idx] = t

    ans = [0] * (N + 1)
    for v in range(1, N + 1):
        ans[v] = comp_t[comp_index[root_of[v]]] ^ pot[v]

    out = sys.stdout
    out.write(" ".join(str(ans[v]) for v in range(1, N + 1)))
    out.write("\n")

solve()