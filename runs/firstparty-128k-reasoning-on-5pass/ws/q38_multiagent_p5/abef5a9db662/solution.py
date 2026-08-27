import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    qpos = 1 + 2 * N
    Q = data[qpos]
    queries = data[qpos + 1:]
    M = max(queries)

    # Hybrid choice from the plan: use the query subset only when it would
    # need a strictly smaller power-of-two size than the full domain.
    size_q = 1 << (Q - 1).bit_length()
    size_m = 1 << (M - 1).bit_length()
    subset = size_q < size_m

    if subset:
        n = Q
        sorted_queries = sorted(queries)
        f1 = sorted_queries[0]
        nd = n - 1

        if nd:
            D = [sorted_queries[i] - sorted_queries[i - 1] for i in range(1, n)]
            total = sorted_queries[-1] - f1

            tree = [0] * (nd + 1)
            for i in range(1, nd + 1):
                tree[i] += D[i - 1]
                j = i + (i & -i)
                if j <= nd:
                    tree[j] += tree[i]

            bitmask = 1 << (nd.bit_length() - 1)
        else:
            D = []
            total = 0
            tree = [0]
            bitmask = 0
    else:
        n = M
        f1 = 1
        nd = n - 1

        if nd:
            D = [1] * nd
            total = nd
            tree = [0] + [i & -i for i in range(1, nd + 1)]
            bitmask = 1 << (nd.bit_length() - 1)
        else:
            D = []
            total = 0
            tree = [0]
            bitmask = 0

    tr = tree
    dd = D
    bm = bitmask
    nn = n
    tot = total

    def lower_bound(target, tr=tr, nd=nd, bm=bm):
        pos = 0
        bit = bm
        while bit:
            nxt = pos + bit
            if nxt <= nd and tr[nxt] < target:
                pos = nxt
                target -= tr[nxt]
            bit >>= 1
        return pos + 1

    def add(i, delta, tr=tr, nd=nd):
        while i <= nd:
            tr[i] += delta
            i += i & -i

    end = 1 + 2 * N
    for idx in range(1, end, 2):
        L = data[idx]
        rp1 = data[idx + 1] + 1

        t = L - f1
        if t <= 0:
            l = 0
            if rp1 <= f1:
                continue
        elif t > tot:
            continue
        else:
            l = lower_bound(t)

        t = rp1 - f1
        if t <= 0:
            continue
        if t > tot:
            r1 = nn
        else:
            r1 = lower_bound(t)

        if r1 == l:
            continue

        if l == 0:
            f1 += 1

        if l > 0:
            dd[l - 1] += 1
            add(l, 1)
            tot += 1

        if r1 < nn:
            dd[r1 - 1] -= 1
            add(r1, -1)
            tot -= 1

    del data

    final_val = [0] * (M + 1)
    cur = f1

    if subset:
        for i, x in enumerate(sorted_queries):
            final_val[x] = cur
            if i < nn - 1:
                cur += dd[i]
    else:
        for x in range(1, M + 1):
            final_val[x] = cur
            if x < M:
                cur += dd[x - 1]

    out = [str(final_val[x]) for x in queries]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()