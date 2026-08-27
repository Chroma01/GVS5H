import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = 0
    n = data[it]
    it += 1

    m = 500000
    size = 1
    while size < m:
        size <<= 1

    neg_inf = -10**18
    mx = [neg_inf] * (size * 2)
    lazy = [0] * (size * 2)

    for i in range(m):
        mx[size + i] = i + 1
    for i in range(size - 1, 0, -1):
        mx[i] = max(mx[i << 1], mx[i << 1 | 1])

    def push(v):
        z = lazy[v]
        if z:
            lc = v << 1
            rc = lc | 1
            mx[lc] += z
            mx[rc] += z
            lazy[lc] += z
            lazy[rc] += z
            lazy[v] = 0

    def range_add(ql, qr):
        def dfs(v, l, r):
            if qr < l or r < ql:
                return
            if ql <= l and r <= qr:
                mx[v] += 1
                lazy[v] += 1
                return
            push(v)
            mid = (l + r) >> 1
            dfs(v << 1, l, mid)
            dfs(v << 1 | 1, mid + 1, r)
            mx[v] = max(mx[v << 1], mx[v << 1 | 1])

        dfs(1, 1, size)

    def first_ge(x):
        if mx[1] < x:
            return m + 1

        v = 1
        l = 1
        r = size
        while l != r:
            push(v)
            mid = (l + r) >> 1
            lc = v << 1
            if mx[lc] >= x:
                v = lc
                r = mid
            else:
                v = lc | 1
                l = mid + 1
        return l

    def first_gt(x):
        if mx[1] <= x:
            return m + 1

        v = 1
        l = 1
        r = size
        while l != r:
            push(v)
            mid = (l + r) >> 1
            lc = v << 1
            if mx[lc] > x:
                v = lc
                r = mid
            else:
                v = lc | 1
                l = mid + 1
        return l

    for _ in range(n):
        left = data[it]
        right = data[it + 1]
        it += 2

        a = first_ge(left)
        b = first_gt(right)
        if a < b:
            range_add(a, b - 1)

    q = data[it]
    it += 1

    out = []
    for _ in range(q):
        x = data[it]
        it += 1

        v = 1
        l = 1
        r = size
        added = 0
        while l != r:
            added += lazy[v]
            mid = (l + r) >> 1
            if x <= mid:
                v <<= 1
                r = mid
            else:
                v = v << 1 | 1
                l = mid + 1
        out.append(str(x + added + lazy[v]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()