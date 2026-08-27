import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] + [int(x) for x in data[1:1 + n]]  # 1-indexed

    # Prefix distinct counts: P[i] = distinct in A[1..i]
    P = [0] * (n + 1)
    seen = bytearray(n + 1)
    cnt = 0
    for i in range(1, n + 1):
        if not seen[A[i]]:
            seen[A[i]] = 1
            cnt += 1
        P[i] = cnt

    # Suffix distinct counts: Suf[k] = distinct in A[k..n]
    Suf = [0] * (n + 2)
    seen2 = bytearray(n + 1)
    cnt = 0
    for k in range(n, 0, -1):
        if not seen2[A[k]]:
            seen2[A[k]] = 1
            cnt += 1
        Suf[k] = cnt

    # Lazy segment tree over i in [1, n-1], initialized with P[i].
    # f_j(i) = P[i] - (# values whose last occurrence in A[1..j] is at position <= i)
    size = 1
    while size < n + 1:
        size <<= 1
    NEG = -10**9
    mx = [NEG] * (2 * size)
    lazy = [0] * (2 * size)

    for i in range(1, n):
        mx[size + i] = P[i]
    for v in range(size - 1, 0, -1):
        mx[v] = mx[2 * v] if mx[2 * v] > mx[2 * v + 1] else mx[2 * v + 1]

    def push(v):
        if lazy[v]:
            lv = lazy[v]
            c = 2 * v
            lazy[c] += lv
            mx[c] += lv
            lazy[c + 1] += lv
            mx[c + 1] += lv
            lazy[v] = 0

    def range_add(v, l, r, ql, qr, val):
        if qr <= l or r <= ql:
            return
        if ql <= l and r <= qr:
            mx[v] += val
            lazy[v] += val
            return
        push(v)
        m = (l + r) >> 1
        range_add(2 * v, l, m, ql, qr, val)
        range_add(2 * v + 1, m, r, ql, qr, val)
        mx[v] = mx[2 * v] if mx[2 * v] > mx[2 * v + 1] else mx[2 * v + 1]

    def range_max(v, l, r, ql, qr):
        if qr <= l or r <= ql:
            return NEG
        if ql <= l and r <= qr:
            return mx[v]
        push(v)
        m = (l + r) >> 1
        a = range_max(2 * v, l, m, ql, qr)
        b = range_max(2 * v + 1, m, r, ql, qr)
        return a if a > b else b

    prev = [0] * (n + 1)
    D = 0  # distinct count in A[1..j]
    ans = 0
    for j in range(1, n):  # j from 1 to n-1 (suffix must be non-empty)
        x = A[j]
        p = prev[x]
        if p > 0:
            # last occurrence of x moves from p to j: cancel old subtraction on [p, j)
            range_add(1, 0, size, p, j, 1)
        else:
            D += 1
        # new last occurrence at j subtracts 1 for all i >= j (also covers first occurrences)
        range_add(1, 0, size, j, n, -1)
        prev[x] = j
        if j >= 2:
            best_i = range_max(1, 0, size, 1, j)  # max over i in [1, j-1]
            cand = best_i + D + Suf[j + 1]
            if cand > ans:
                ans = cand

    sys.stdout.write(str(ans) + "\n")

solve()