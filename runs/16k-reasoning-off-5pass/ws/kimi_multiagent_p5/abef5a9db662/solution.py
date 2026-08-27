import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    N = int(data[pos]); pos += 1
    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = int(data[pos]); R[i] = int(data[pos + 1]); pos += 2

    V = 500000  # domain of initial ratings: indices 1..V

    size = 1
    while size < V + 2:
        size <<= 1

    INF = float('inf')
    NEG = float('-inf')
    mn = [0] * (2 * size)
    mx = [0] * (2 * size)
    lazy = [0] * (2 * size)

    # Initialize leaves: A[x] = x for x in [1, V]; padding leaves get sentinel values.
    for i in range(size):
        x = i  # leaf i corresponds to index i
        if 1 <= x <= V:
            mn[size + i] = x
            mx[size + i] = x
        else:
            mn[size + i] = INF
            mx[size + i] = NEG
    for i in range(size - 1, 0, -1):
        l = i << 1
        r = l | 1
        a = mn[l] if mn[l] < mn[r] else mn[r]
        mn[i] = a
        b = mx[l] if mx[l] > mx[r] else mx[r]
        mx[i] = b

    sys.setrecursionlimit(1 << 22)

    def apply(i, v):
        mn[i] += v
        mx[i] += v
        lazy[i] += v

    def push(i):
        v = lazy[i]
        if v:
            l = i << 1
            r = l | 1
            apply(l, v)
            apply(r, v)
            lazy[i] = 0

    def range_add(i, tl, tr, ql, qr):
        if ql > qr or ql > tr or qr < tl:
            return
        if ql <= tl and tr <= qr:
            apply(i, 1)
            return
        push(i)
        tm = (tl + tr) >> 1
        range_add(i << 1, tl, tm, ql, qr)
        range_add(i << 1 | 1, tm + 1, tr, ql, qr)
        l = i << 1
        r = l | 1
        mn[i] = mn[l] if mn[l] < mn[r] else mn[r]
        mx[i] = mx[l] if mx[l] > mx[r] else mx[r]

    def find_first_ge(i, tl, tr, val):
        # first index in [0, size) with A >= val; returns size if none
        if mx[i] < val:
            return size
        if tl == tr:
            return tl
        push(i)
        tm = (tl + tr) >> 1
        res = find_first_ge(i << 1, tl, tm, val)
        if res != size:
            return res
        return find_first_ge(i << 1 | 1, tm + 1, tr, val)

    def find_last_le(i, tl, tr, val):
        # last index in [0, size) with A <= val; returns -1 if none
        if mn[i] > val:
            return -1
        if tl == tr:
            return tl
        push(i)
        tm = (tl + tr) >> 1
        res = find_last_le(i << 1 | 1, tm + 1, tr, val)
        if res != -1:
            return res
        return find_last_le(i << 1, tl, tm, val)

    for i in range(N):
        li = L[i]
        ri = R[i]
        # qualifying initial indices x satisfy li <= A[x] <= ri; A monotone => contiguous
        p = find_first_ge(1, 0, size - 1, li)
        if p > V:
            continue
        q = find_last_le(1, 0, size - 1, ri)
        if q > V:
            q = V
        if p <= q:
            range_add(1, 0, size - 1, p, q)

    # Point queries: read A[x] for each query
    def point_query(i, tl, tr, idx):
        while tl != tr:
            push(i)
            tm = (tl + tr) >> 1
            if idx <= tm:
                i = i << 1
                tr = tm
            else:
                i = i << 1 | 1
                tl = tm + 1
        return mn[i]

    Q = int(data[pos]); pos += 1
    out = []
    for _ in range(Q):
        x = int(data[pos]); pos += 1
        out.append(str(point_query(1, 0, size - 1, x)))
    sys.stdout.write("\n".join(out) + "\n")

main()