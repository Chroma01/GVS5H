import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    # Weighted DSU where parity[x] = bitmask (30 bits):
    # bit k of parity[x] = XOR of bit k of A_x and bit k of A_root(x)
    parent = list(range(N + 1))
    size = [1] * (N + 1)
    parity = [0] * (N + 1)

    def find(x):
        # Iterative find with path compression, accumulating parity mask.
        # After find(x): parent[x] == root and parity[x] = mask of x relative to root.
        if parent[x] == x:
            return x
        root = x
        acc = 0
        while parent[root] != root:
            acc ^= parity[root]
            root = parent[root]
        # compress path from x to root
        while parent[x] != root:
            nxt = parent[x]
            p = parity[x]
            parity[x] = acc
            parent[x] = root
            acc ^= p
            x = nxt
        return root

    feasible = True
    for i in range(M):
        x = int(data[idx]); idx += 1
        y = int(data[idx]); idx += 1
        z = int(data[idx]); idx += 1

        rx = find(x)
        ry = find(y)
        # after find, parity[x]/parity[y] are masks relative to rx/ry
        px = parity[x]
        py = parity[y]
        if rx == ry:
            if (px ^ py) != z:
                feasible = False
                break
        else:
            # Need w = parity of new child root such that px ^ w ^ py = z
            w = px ^ py ^ z
            if size[rx] < size[ry]:
                parent[rx] = ry
                parity[rx] = w
                size[ry] += size[rx]
            else:
                parent[ry] = rx
                parity[ry] = w
                size[rx] += size[ry]

    if not feasible:
        sys.stdout.write("-1\n")
        return

    # Finalize roots and parity masks for every vertex
    roots = [0] * (N + 1)
    pmasks = [0] * (N + 1)
    comp_index = {}
    ncomp = 0
    for v in range(1, N + 1):
        r = find(v)
        roots[v] = r
        pmasks[v] = parity[v]
        if r not in comp_index:
            comp_index[r] = ncomp
            ncomp += 1

    NBITS = 30
    cnt1 = [[0] * NBITS for _ in range(ncomp)]
    comp_sz = [0] * ncomp

    for v in range(1, N + 1):
        ci = comp_index[roots[v]]
        comp_sz[ci] += 1
        p = pmasks[v]
        row = cnt1[ci]
        b = 0
        while p:
            if p & 1:
                row[b] += 1
            p >>= 1
            b += 1

    # For each component and bit, choose root bit to minimize # of 1s:
    # root bit 0 -> c1 ones; root bit 1 -> c0 = size - c1 ones.
    root_mask = [0] * ncomp
    for ci in range(ncomp):
        total = comp_sz[ci]
        row = cnt1[ci]
        mask = 0
        for b in range(NBITS):
            c1 = row[b]
            if c1 > total - c1:
                mask |= (1 << b)
        root_mask[ci] = mask

    A = [0] * (N + 1)
    for v in range(1, N + 1):
        ci = comp_index[roots[v]]
        A[v] = pmasks[v] ^ root_mask[ci]

    out = ' '.join(str(A[v]) for v in range(1, N + 1))
    sys.stdout.write(out + "\n")

main()