import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); W = int(data[pos + 1]); pos += 2
    N = H * W
    F = [0] * N
    for i in range(N):
        F[i] = int(data[pos]); pos += 1
    Q = int(data[pos]); pos += 1

    lo_arr = [0] * Q
    hi_arr = [0] * Q
    m = [0] * Q
    qs = [None] * N

    for qid in range(Q):
        A = int(data[pos]); B = int(data[pos + 1]); Y = int(data[pos + 2])
        C = int(data[pos + 3]); D = int(data[pos + 4]); Z = int(data[pos + 5])
        pos += 6
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)
        if Y < Z:
            lo_arr[qid] = Y; hi_arr[qid] = Z
        else:
            lo_arr[qid] = Z; hi_arr[qid] = Y
        if u == v:
            m[qid] = F[u]
        else:
            if qs[u] is None:
                qs[u] = {qid}
            else:
                qs[u].add(qid)
            if qs[v] is None:
                qs[v] = {qid}
            else:
                qs[v].add(qid)
    del data

    parent = list(range(N))
    size = [1] * N

    def find(x, parent=parent):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def merge_roots(ru, rv, cap, parent=parent, size=size, qs=qs, m=m):
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        A = qs[ru]; B = qs[rv]
        if B is not None:
            if A is None:
                qs[ru] = B
            else:
                if len(A) < len(B):
                    A, B = B, A
                for qid in B:
                    if qid in A:
                        m[qid] = cap
                        A.remove(qid)
                    else:
                        A.add(qid)
                qs[ru] = A if A else None
        qs[rv] = None
        parent[rv] = ru
        size[ru] += size[rv]
        return ru

    order = sorted(range(N), key=F.__getitem__, reverse=True)
    added = bytearray(N)

    for u in order:
        added[u] = 1
        cap = F[u]
        ru = find(u)
        j = u % W
        if j and added[u - 1]:
            rv = find(u - 1)
            if rv != ru:
                ru = merge_roots(ru, rv, cap)
        if j < W - 1 and added[u + 1]:
            rv = find(u + 1)
            if rv != ru:
                ru = merge_roots(ru, rv, cap)
        if u >= W and added[u - W]:
            rv = find(u - W)
            if rv != ru:
                ru = merge_roots(ru, rv, cap)
        if u + W < N and added[u + W]:
            rv = find(u + W)
            if rv != ru:
                ru = merge_roots(ru, rv, cap)

    out = []
    for qid in range(Q):
        lo = lo_arr[qid]; hi = hi_arr[qid]; mm = m[qid]
        ans = hi - lo
        if lo > mm:
            ans += 2 * (lo - mm)
        out.append(str(ans))
    sys.stdout.write('\n'.join(out) + '\n')

main()