import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]

    # suf[j] = number of distinct values in A[j+1..N] (1-indexed positions), j = 1..N-1
    suf = [0] * (n + 2)
    seen = bytearray(n + 1)
    cnt = 0
    for idx in range(n, 0, -1):
        v = A[idx - 1]
        if not seen[v]:
            seen[v] = 1
            cnt += 1
        suf[idx - 1] = cnt  # distinct among positions idx..N

    # Lazy segment tree over left-cut positions i = 1..N-1 (leaf index i-1).
    # Leaf i holds P[i] + D(A_{i+1..j}) for the current right cut j.
    size = 1
    while size < n:
        size <<= 1
    NEG = -10**9
    mx = [0] * (2 * size)
    lazy = [0] * (2 * size)

    def push(node):
        v = lazy[node]
        if v:
            left = node * 2
            right = left + 1
            lazy[left] += v
            mx[left] += v
            lazy[right] += v
            mx[right] += v
            lazy[node] = 0

    def range_add(l, r, val, node, nl, nr):
        # add val to leaves [l, r] inclusive
        if r < nl or nr < l:
            return
        if l <= nl and nr <= r:
            lazy[node] += val
            mx[node] += val
            return
        push(node)
        mid = (nl + nr) >> 1
        range_add(l, r, val, node * 2, nl, mid)
        range_add(l, r, val, node * 2 + 1, mid + 1, nr)
        a = mx[node * 2]
        b = mx[node * 2 + 1]
        mx[node] = a if a >= b else b

    def range_max(l, r, node, nl, nr):
        if r < nl or nr < l:
            return NEG
        if l <= nl and nr <= r:
            return mx[node]
        push(node)
        mid = (nl + nr) >> 1
        a = range_max(l, r, node * 2, nl, mid)
        b = range_max(l, r, node * 2 + 1, mid + 1, nr)
        return a if a >= b else b

    # Initialize leaves with prefix distinct counts P[i] for i = 1..N-1.
    seen2 = bytearray(n + 1)
    pcnt = 0
    for i in range(1, n + 1):
        v = A[i - 1]
        if not seen2[v]:
            seen2[v] = 1
            pcnt += 1
        if i < n:
            mx[size + i - 1] = pcnt
    for node in range(size - 1, 0, -1):
        a = mx[node * 2]
        b = mx[node * 2 + 1]
        mx[node] = a if a >= b else b

    last = [0] * (n + 1)  # last occurrence position (1-indexed) of each value; 0 = none
    ans = 0
    # Sweep right cut j = 2..N-1. Element A_j enters the middle; with previous
    # occurrence p, it adds +1 to middle distinct count exactly for cuts
    # i in [max(p,1), j-1] (cut i excludes position p from the middle iff i >= p).
    for j in range(2, n):
        v = A[j - 1]
        p = last[v]
        last[v] = j
        L = p if p >= 1 else 1
        # 1-indexed i in [L, j-1] -> leaf indices [L-1, j-2]; L <= j-1 since p < j
        range_add(L - 1, j - 2, 1, 1, 0, size - 1)
        best = range_max(0, j - 2, 1, 0, size - 1)  # max over i in [1, j-1]
        cand = best + suf[j]
        if cand > ans:
            ans = cand

    sys.stdout.write(str(ans) + "\n")

main()