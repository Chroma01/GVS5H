import sys

CAND = 4  # candidates per role; top-2 provably suffices, 4 gives margin


def solve_case(cakes, K):
    n = len(cakes)
    M = [0] * n
    for i, c in enumerate(cakes):
        m = c[0]
        if c[1] > m:
            m = c[1]
        if c[2] > m:
            m = c[2]
        M[i] = m

    order = sorted(range(n), key=lambda i: (-M[i], i))
    base = order[:2 * K]
    in_base = [False] * n
    for i in base:
        in_base[i] = True

    cls = [0] * n
    cnt = [0, 0, 0]
    V0 = 0
    for i in base:
        c = cakes[i]
        m = M[i]
        V0 += m
        if c[0] == m:
            p = 0
        elif c[1] == m:
            p = 1
        else:
            p = 2
        cls[i] = p
        cnt[p] += 1

    odd = [p for p in range(3) if cnt[p] & 1]
    if not odd:
        return V0
    A, B = odd
    C = 3 - A - B

    by_class = [[], [], []]
    for i in base:
        by_class[cls[i]].append(i)
    outsiders = [i for i in range(n) if not in_base[i]]

    add_sorted = [None, None, None]

    def top_add(q):
        if add_sorted[q] is None:
            add_sorted[q] = sorted(outsiders, key=lambda i: (-cakes[i][q], i))
        return add_sorted[q][:CAND]

    def top_reassign(p, q):
        return sorted(by_class[p],
                      key=lambda i: (M[i] - cakes[i][q], i))[:CAND]

    def top_rem(p):
        return sorted(by_class[p], key=lambda i: (M[i], i))[:CAND]

    def ops_flipping(p, q):
        # All single ops flipping parities of classes p and q:
        #   reassign base-p item to q ; reassign base-q item to p ;
        #   swap out base-p item & add outsider to q ; and symmetric.
        ops = []
        for i in top_reassign(p, q):
            ops.append((M[i] - cakes[i][q], (i,)))
        for i in top_reassign(q, p):
            ops.append((M[i] - cakes[i][p], (i,)))
        add_q = top_add(q)
        add_p = top_add(p)
        for i in top_rem(p):
            mi = M[i]
            for o in add_q:
                ops.append((mi - cakes[o][q], (i, o)))
        for i in top_rem(q):
            mi = M[i]
            for o in add_p:
                ops.append((mi - cakes[o][p], (i, o)))
        return ops

    best = None
    # 1-op direct edges flipping {A,B}
    for loss, _ in ops_flipping(A, B):
        if best is None or loss < best:
            best = loss
    # 2-op simple paths A-C-B with disjoint items
    ops_ac = ops_flipping(A, C)
    ops_bc = ops_flipping(B, C)
    for l1, t1 in ops_ac:
        s1 = frozenset(t1)
        for l2, t2 in ops_bc:
            if s1.isdisjoint(t2):
                tot = l1 + l2
                if best is None or tot < best:
                    best = tot
    # best always exists: class A is nonempty, so reassign A->B is a 1-op.
    return V0 - best


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    T = int(data[pos]); pos += 1
    out = []
    for _ in range(T):
        N = int(data[pos]); K = int(data[pos + 1]); pos += 2
        cakes = []
        for _ in range(N):
            x = int(data[pos]); y = int(data[pos + 1]); z = int(data[pos + 2])
            pos += 3
            cakes.append((x, y, z))
        out.append(str(solve_case(cakes, K)))
    sys.stdout.write("\n".join(out) + "\n")


main()