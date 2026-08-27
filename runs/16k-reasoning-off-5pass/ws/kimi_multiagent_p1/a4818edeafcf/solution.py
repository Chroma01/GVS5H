import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # prev[k] = previous occurrence index of A[k], 0 if none
    prev = [0] * (n + 1)
    last = {}
    for k in range(1, n + 1):
        v = A[k]
        prev[k] = last.get(v, 0)
        last[v] = k

    # P[i] = distinct count of A[1..i]
    P = [0] * (n + 1)
    seen = set()
    c = 0
    for i in range(1, n + 1):
        if A[i] not in seen:
            seen.add(A[i])
            c += 1
        P[i] = c

    # S[i] = distinct count of A[i..N]
    S = [0] * (n + 2)
    seen.clear()
    c = 0
    for i in range(n, 0, -1):
        if A[i] not in seen:
            seen.add(A[i])
            c += 1
        S[i] = c

    # Iterative lazy segment tree over indices 1..n (0 unused), supporting
    # range add and range max query.
    size = 1
    while size < n + 1:
        size <<= 1
    NEG = float('-inf')
    mx = [NEG] * (2 * size)
    lz = [0] * (2 * size)

    # build leaves: val[i] = P[i]
    for i in range(1, n + 1):
        mx[size + i] = P[i]
    for i in range(size - 1, 0, -1):
        mx[i] = mx[2 * i] if mx[2 * i] > mx[2 * i + 1] else mx[2 * i + 1]

    def push(v):
        if lz[v]:
            lz[2 * v] += lz[v]
            mx[2 * v] += lz[v]
            lz[2 * v + 1] += lz[v]
            mx[2 * v + 1] += lz[v]
            lz[v] = 0

    def range_add(l, r, val, v=1, tl=0, tr=None):
        if tr is None:
            tr = size - 1
        if l > r or r < tl or tr < l:
            return
        if l <= tl and tr <= r:
            mx[v] += val
            lz[v] += val
            return
        push(v)
        tm = (tl + tr) // 2
        range_add(l, r, val, 2 * v, tl, tm)
        range_add(l, r, val, 2 * v + 1, tm + 1, tr)
        mx[v] = mx[2 * v] if mx[2 * v] > mx[2 * v + 1] else mx[2 * v + 1]

    def range_max(l, r, v=1, tl=0, tr=None):
        if tr is None:
            tr = size - 1
        if l > r or r < tl or tr < l:
            return NEG
        if l <= tl and tr <= r:
            return mx[v]
        push(v)
        tm = (tl + tr) // 2
        a = range_max(l, r, 2 * v, tl, tm)
        b = range_max(l, r, 2 * v + 1, tm + 1, tr)
        return a if a > b else b

    ans = 0
    # j from 2 to n-1; i in [1, j-1]
    for j in range(2, n):
        # position k=j contributes +1 to all i in [max(1, prev[j]), j-1]
        lo = prev[j] if prev[j] > 1 else 1
        range_add(lo, j - 1, 1)
        best = range_max(1, j - 1)
        total = best + S[j + 1]
        if total > ans:
            ans = total

    print(ans)

solve()