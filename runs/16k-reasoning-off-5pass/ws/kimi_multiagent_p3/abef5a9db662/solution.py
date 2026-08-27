import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0
    N = data[p]; p += 1
    L = [0] * N
    R = [0] * N
    for i in range(N):
        L[i] = data[p]; R[i] = data[p + 1]; p += 2
    Q = data[p]; p += 1
    queries = data[p:p + Q]

    V = 500000
    size = 1
    while size < V + 2:
        size <<= 1

    INF = float('inf')
    NEG = float('-inf')
    mn = [0.0] * (2 * size)
    mx = [0.0] * (2 * size)
    lazy = [0] * (2 * size)
    # leaves represent x = 0 .. size-1; valid domain x in [1, V]
    for x in range(size):
        if 1 <= x <= V:
            mn[size + x] = x
            mx[size + x] = x
        else:
            mn[size + x] = INF
            mx[size + x] = NEG
    for i in range(size - 1, 0, -1):
        a = mn[2 * i]; b = mn[2 * i + 1]
        mn[i] = a if a < b else b
        a = mx[2 * i]; b = mx[2 * i + 1]
        mx[i] = a if a > b else b

    sys.setrecursionlimit(1 << 20)

    def push(i):
        z = lazy[i]
        if z:
            lazy[2 * i] += z
            lazy[2 * i + 1] += z
            mn[2 * i] += z
            mx[2 * i] += z
            mn[2 * i + 1] += z
            mx[2 * i + 1] += z
            lazy[i] = 0

    def range_add(i, l, r, ql, qr):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            mn[i] += 1
            mx[i] += 1
            lazy[i] += 1
            return
        push(i)
        m = (l + r) >> 1
        range_add(2 * i, l, m, ql, qr)
        range_add(2 * i + 1, m + 1, r, ql, qr)
        a = mn[2 * i]; b = mn[2 * i + 1]
        mn[i] = a if a < b else b
        a = mx[2 * i]; b = mx[2 * i + 1]
        mx[i] = a if a > b else b

    def find_first_geq(T):
        # smallest x with h(x) >= T, or None
        if mx[1] < T:
            return None
        i = 1
        l = 0
        r = size - 1
        while i < size:
            push(i)
            m = (l + r) >> 1
            if mx[2 * i] >= T:
                i = 2 * i
                r = m
            else:
                i = 2 * i + 1
                l = m + 1
        return i - size

    def find_last_leq(T):
        # largest x with h(x) <= T, or None
        if mn[1] > T:
            return None
        i = 1
        l = 0
        r = size - 1
        while i < size:
            push(i)
            m = (l + r) >> 1
            if mn[2 * i + 1] <= T:
                i = 2 * i + 1
                l = m + 1
            else:
                i = 2 * i
                r = m
        return i - size

    for i in range(N):
        Li = L[i]
        Ri = R[i]
        a = find_first_geq(Li)
        if a is None:
            continue
        b = find_last_leq(Ri)
        if b is None or a > b:
            continue
        range_add(1, 0, size - 1, a, b)

    out = []
    for X in queries:
        # point query of added(X)
        i = 1
        l = 0
        r = size - 1
        acc = 0
        while i < size:
            acc += lazy[i]
            m = (l + r) >> 1
            if X <= m:
                i = 2 * i
                r = m
            else:
                i = 2 * i + 1
                l = m + 1
        acc += lazy[i]
        out.append(str(X + acc))
    sys.stdout.write("\n".join(out) + "\n")

main()