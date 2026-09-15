import sys

def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = H * W
    F = [0] * N
    for i in range(N):
        F[i] = int(next(it))
    Q = int(next(it))
    attach = [[] for _ in range(N)]
    Ys = [0] * Q
    Zs = [0] * Q
    ans = [-1] * Q
    for q in range(Q):
        A = int(next(it)) - 1
        B = int(next(it)) - 1
        Y = int(next(it))
        C = int(next(it)) - 1
        D = int(next(it)) - 1
        Z = int(next(it))
        Ys[q] = Y
        Zs[q] = Z
        u = A * W + B
        v = C * W + D
        if u == v:
            ans[q] = F[u]
        else:
            attach[u].append(q)
            attach[v].append(q)

    parent = list(range(N))
    size = [1] * N
    active = [False] * N
    qset = [None] * N

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b, h):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        sa = qset[ra]
        sb = qset[rb]
        if sa is None:
            new_qset = sb
        elif sb is None:
            new_qset = sa
        else:
            if len(sa) < len(sb):
                sa, sb = sb, sa
            for qid in sb:
                if qid in sa:
                    ans[qid] = h
                    sa.discard(qid)
                else:
                    sa.add(qid)
            new_qset = sa
        if new_qset is not None and len(new_qset) == 0:
            new_qset = None
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        qset[ra] = new_qset
        qset[rb] = None

    order = list(range(N))
    order.sort(key=F.__getitem__, reverse=True)

    for idx in order:
        h = F[idx]
        active[idx] = True
        att = attach[idx]
        if att:
            qset[idx] = set(att)
        else:
            qset[idx] = None
        i = idx // W
        j = idx - i * W
        if i > 0:
            nbr = idx - W
            if active[nbr]:
                union(idx, nbr, h)
        if i < H - 1:
            nbr = idx + W
            if active[nbr]:
                union(idx, nbr, h)
        if j > 0:
            nbr = idx - 1
            if active[nbr]:
                union(idx, nbr, h)
        if j < W - 1:
            nbr = idx + 1
            if active[nbr]:
                union(idx, nbr, h)

    out = []
    for q in range(Q):
        M = ans[q]
        Y = Ys[q]
        Z = Zs[q]
        if M >= min(Y, Z):
            out.append(str(abs(Y - Z)))
        else:
            out.append(str(Y + Z - 2 * M))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()