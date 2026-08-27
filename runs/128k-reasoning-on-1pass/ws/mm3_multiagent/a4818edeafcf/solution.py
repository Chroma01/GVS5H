import sys

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)

    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # ---------- prefix distinct counts ----------
    seen = [False] * (N + 1)
    pref = [0] * N
    cnt = 0
    for i, x in enumerate(A):
        if not seen[x]:
            seen[x] = True
            cnt += 1
        pref[i] = cnt

    # ---------- suffix distinct counts ----------
    seen = [False] * (N + 1)
    suff = [0] * N
    cnt = 0
    for i in range(N - 1, -1, -1):
        x = A[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        suff[i] = cnt

    # ---------- segment tree (range add, range max) ----------
    size = 1
    while size < N:
        size <<= 1
    maxv = [0] * (2 * size)   # maximum values
    lazy = [0] * (2 * size)   # lazy additions

    # build leaves
    for i in range(N):
        maxv[size + i] = pref[i]
    for i in range(size - 1, 0, -1):
        maxv[i] = max(maxv[2 * i], maxv[2 * i + 1])

    def apply(node, val):
        maxv[node] += val
        lazy[node] += val

    def push(node):
        if lazy[node]:
            apply(node * 2, lazy[node])
            apply(node * 2 + 1, lazy[node])
            lazy[node] = 0

    # range add on [l, r] (inclusive)
    def range_add(l, r, val):
        def _add(node, left, right):
            if r < left or l > right:
                return
            if l <= left and right <= r:
                apply(node, val)
                return
            push(node)
            mid = (left + right) // 2
            _add(node * 2, left, mid)
            _add(node * 2 + 1, mid + 1, right)
            maxv[node] = max(maxv[node * 2], maxv[node * 2 + 1])
        _add(1, 0, size - 1)

    # range max query on [l, r]
    def range_max(l, r):
        def _query(node, left, right):
            if r < left or l > right:
                return -10**9
            if l <= left and right <= r:
                return maxv[node]
            push(node)
            mid = (left + right) // 2
            left_max = _query(node * 2, left, mid)
            right_max = _query(node * 2 + 1, mid + 1, right)
            return left_max if left_max > right_max else right_max
        return _query(1, 0, size - 1)

    # ---------- main loop ----------
    last = [-1] * (N + 1)          # last occurrence of each value (0‑based)
    ans = 0

    # j is the right end of the middle subarray (0‑based)
    for j in range(1, N - 1):
        val = A[j]
        prev = last[val]          # previous occurrence of A[j]
        l = prev if prev != -1 else 0
        r = j - 1
        if l <= r:
            range_add(l, r, 1)    # A[j] becomes a new distinct value for i in [prev, j-1]

        best = range_max(0, j - 1)    # max_i (pref[i] + distinct(i+1..j))
        cand = best + suff[j + 1]     # add the suffix part
        if cand > ans:
            ans = cand

        last[val] = j

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()