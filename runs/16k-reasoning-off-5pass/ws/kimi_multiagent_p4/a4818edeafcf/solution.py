import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # P[i] = number of distinct values in A[1..i]
    P = [0] * (n + 1)
    seen = bytearray(n + 1)
    cnt = 0
    for i in range(1, n + 1):
        x = A[i]
        if not seen[x]:
            seen[x] = 1
            cnt += 1
        P[i] = cnt

    # S[i] = number of distinct values in A[i..n]
    S = [0] * (n + 2)
    seen = bytearray(n + 1)
    cnt = 0
    for i in range(n, 0, -1):
        x = A[i]
        if not seen[x]:
            seen[x] = 1
            cnt += 1
        S[i] = cnt

    # Lazy segment tree over l in [1..n], base value P[l-1].
    # Supports range add and range max query.
    size = 1
    while size < n + 2:
        size <<= 1
    INF_NEG = -10**9
    mx = [INF_NEG] * (2 * size)
    lazy = [0] * (2 * size)

    # Build leaves: position l (1-indexed) -> P[l-1]
    for l in range(1, n + 1):
        mx[size + l] = P[l - 1]
    for i in range(size - 1, 0, -1):
        mx[i] = mx[2 * i] if mx[2 * i] > mx[2 * i + 1] else mx[2 * i + 1]

    def apply(i, v):
        mx[i] += v
        lazy[i] += v

    def push(i):
        if lazy[i]:
            v = lazy[i]
            apply(2 * i, v)
            apply(2 * i + 1, v)
            lazy[i] = 0

    def range_add(l, r, v, i, lo, hi):
        if r < lo or hi < l:
            return
        if l <= lo and hi <= r:
            apply(i, v)
            return
        push(i)
        mid = (lo + hi) // 2
        range_add(l, r, v, 2 * i, lo, mid)
        range_add(l, r, v, 2 * i + 1, mid + 1, hi)
        mx[i] = mx[2 * i] if mx[2 * i] > mx[2 * i + 1] else mx[2 * i + 1]

    def range_max(l, r, i, lo, hi):
        if r < lo or hi < l:
            return INF_NEG
        if l <= lo and hi <= r:
            return mx[i]
        push(i)
        mid = (lo + hi) // 2
        a = range_max(l, r, 2 * i, lo, mid)
        b = range_max(l, r, 2 * i + 1, mid + 1, hi)
        return a if a > b else b

    last = [0] * (n + 1)
    ans = 0
    # r = j (right cut). Need 2 <= r <= n-1, l in [2, r].
    # At step r, h[l] = P[l-1] + distinct(A[l..r]).
    # Adding A_r increments distinct(A[l..r]) by 1 exactly for l in (last[A_r], r].
    # Updates from position 1 only affect l=1 (never queried), so starting at r=2 is safe.
    for r in range(2, n):
        x = A[r]
        p = last[x]
        range_add(p + 1, r, 1, 1, 0, size - 1)
        last[x] = r
        best = range_max(2, r, 1, 0, size - 1)
        cand = best + S[r + 1]
        if cand > ans:
            ans = cand

    print(ans)

main()