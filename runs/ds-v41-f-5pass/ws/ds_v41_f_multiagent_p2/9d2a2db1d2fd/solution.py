import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); pos += 1
    W = int(data[pos]); pos += 1
    N = H * W
    F = [0] * N
    for k in range(N):
        F[k] = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1

    qY = [0] * Q
    qZ = [0] * Q
    Mval = [-1] * Q
    query_at = [[] for _ in range(N)]

    for qi in range(Q):
        A = int(data[pos]); B = int(data[pos + 1]); Y = int(data[pos + 2])
        C = int(data[pos + 3]); D = int(data[pos + 4]); Z = int(data[pos + 5])
        pos += 6
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)
        qY[qi] = Y
        qZ[qi] = Z
        if u == v:
            Mval[qi] = F[u]
        else:
            query_at[u].append(qi)
            query_at[v].append(qi)

    del data

    order = sorted(range(N), key=F.__getitem__, reverse=True)

    parent = list(range(N))
    sz = [1] * N
    comp_set = [None] * N
    active = bytearray(N)

    def find(x):
        px = parent
        while px[x] != x:
            px[x] = px[px[x]]
            x = px[x]
        return x

    def merge(ra, rb, fc):
        if sz[ra] >= sz[rb]:
            big, small = ra, rb
        else:
            big, small = rb, ra
        s = comp_set[small]
        if s is not None:
            l = comp_set[big]
            if l is None:
                comp_set[big] = s
            else:
                common = s & l
                for qid in common:
                    Mval[qid] = fc
                l |= s
            comp_set[small] = None
        parent[small] = big
        sz[big] += sz[small]

    for c in order:
        active[c] = 1
        qs = query_at[c]
        query_at[c] = None
        if qs:
            comp_set[c] = set(qs)
        fc = F[c]
        col = c % W
        if col:
            nb = c - 1
            if active[nb]:
                ra = find(c); rb = find(nb)
                if ra != rb:
                    merge(ra, rb, fc)
        if col + 1 < W:
            nb = c + 1
            if active[nb]:
                ra = find(c); rb = find(nb)
                if ra != rb:
                    merge(ra, rb, fc)
        if c >= W:
            nb = c - W
            if active[nb]:
                ra = find(c); rb = find(nb)
                if ra != rb:
                    merge(ra, rb, fc)
        if c + W < N:
            nb = c + W
            if active[nb]:
                ra = find(c); rb = find(nb)
                if ra != rb:
                    merge(ra, rb, fc)

    out = []
    for qi in range(Q):
        y = qY[qi]; z = qZ[qi]
        m = Mval[qi]
        if y >= z:
            base = y - z
            mn = z
        else:
            base = z - y
            mn = y
        extra = mn - m
        if extra > 0:
            base += extra + extra
        out.append(str(base))
    sys.stdout.write('\n'.join(out))
    sys.stdout.write('\n')

main()