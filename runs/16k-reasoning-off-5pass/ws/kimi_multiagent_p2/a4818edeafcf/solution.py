import sys

def solve():
    sys.setrecursionlimit(1 << 22)  # safe margin for recursive segtree
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    # L[i] = distinct count of A[0..i] (prefix ending at i, 0-indexed)
    L = [0] * n
    seen = set()
    c = 0
    for i in range(n):
        if A[i] not in seen:
            seen.add(A[i])
            c += 1
        L[i] = c

    # R[i] = distinct count of A[i..n-1] (suffix starting at i)
    R = [0] * (n + 1)
    seen.clear()
    c = 0
    for i in range(n - 1, -1, -1):
        if A[i] not in seen:
            seen.add(A[i])
            c += 1
        R[i] = c

    NEG = float('-inf')
    size = 1
    while size < n:
        size <<= 1
    mx = [NEG] * (2 * size)
    lazy = [0] * (2 * size)

    def apply(p, v):
        mx[p] += v
        lazy[p] += v

    def push(p):
        if lazy[p]:
            apply(p << 1, lazy[p])
            apply(p << 1 | 1, lazy[p])
            lazy[p] = 0

    def pull(p):
        mx[p] = mx[p << 1] if mx[p << 1] >= mx[p << 1 | 1] else mx[p << 1 | 1]

    def point_set(pos, val, p, l, r):
        if l == r:
            mx[p] = val
            return
        push(p)
        m = (l + r) >> 1
        if pos <= m:
            point_set(pos, val, p << 1, l, m)
        else:
            point_set(pos, val, p << 1 | 1, m + 1, r)
        pull(p)

    def range_add(ql, qr, v, p, l, r):
        if ql <= l and r <= qr:
            apply(p, v)
            return
        push(p)
        m = (l + r) >> 1
        if ql <= m:
            range_add(ql, qr, v, p << 1, l, m)
        if qr > m:
            range_add(ql, qr, v, p << 1 | 1, m + 1, r)
        pull(p)

    def range_max(ql, qr, p, l, r):
        if ql <= l and r <= qr:
            return mx[p]
        push(p)
        m = (l + r) >> 1
        res = NEG
        if ql <= m:
            res = range_max(ql, qr, p << 1, l, m)
        if qr > m:
            r2 = range_max(ql, qr, p << 1 | 1, m + 1, r)
            if r2 > res:
                res = r2
        return res

    # Tree index i (0-indexed) represents split after position i:
    # left = A[0..i], middle = A[i+1..j], right = A[j+1..n-1].
    # Valid i: 0 <= i <= j-1, j ranges 1..n-2.
    # value(i) = distinct(A[i+1..j]) + L[i].
    # When j extends by one with v = A[j], distinct(A[i+1..j]) increases by 1
    # iff v not in A[i+1..j-1], i.e. i+1 > last[v] (0-indexed last occurrence),
    # i.e. i >= last[v]. So range-add 1 on i in [last[v], j-1].
    # last[v] initialized to 0: first occurrence adds to all eligible i.
    last = [0] * (n + 1)
    ans = 0
    for j in range(1, n - 1):
        # candidate i = j-1 becomes eligible
        point_set(j - 1, L[j - 1], 1, 0, size - 1)
        v = A[j]
        lv = last[v]
        if lv <= j - 1:
            range_add(lv, j - 1, 1, 1, 0, size - 1)
        last[v] = j
        best = range_max(0, j - 1, 1, 0, size - 1)
        total = best + R[j + 1]
        if total > ans:
            ans = total

    sys.stdout.write(str(ans) + "\n")

solve()