import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    contests = [(next(it), next(it)) for _ in range(n)]

    q = next(it)
    queries = [next(it) for _ in range(q)]

    M = 500000
    S = 1
    while S < M:
        S <<= 1

    mx = [0] * (2 * S)
    lazy = [0] * (2 * S)

    for i in range(M):
        mx[S + i] = i + 1

    for k in range(S - 1, 0, -1):
        left = mx[k << 1]
        right = mx[k << 1 | 1]
        mx[k] = left if left >= right else right

    def push(k):
        z = lazy[k]
        if z:
            lc = k << 1
            rc = lc | 1
            mx[lc] += z
            mx[rc] += z
            lazy[lc] += z
            lazy[rc] += z
            lazy[k] = 0

    def range_add(k, l, r, ql, qr):
        if ql <= l and r <= qr:
            mx[k] += 1
            lazy[k] += 1
            return

        push(k)
        mid = (l + r) >> 1

        if ql <= mid:
            range_add(k << 1, l, mid, ql, qr)
        if mid < qr:
            range_add(k << 1 | 1, mid + 1, r, ql, qr)

        left = mx[k << 1]
        right = mx[k << 1 | 1]
        mx[k] = left if left >= right else right

    def first_at_least(target):
        if mx[1] < target:
            return M + 1

        k = 1
        l = 1
        r = S
        while l != r:
            push(k)
            mid = (l + r) >> 1
            lc = k << 1
            if mx[lc] >= target:
                k = lc
                r = mid
            else:
                k = lc | 1
                l = mid + 1
        return l

    for L, R in contests:
        left = first_at_least(L)
        if left <= M:
            right_exclusive = first_at_least(R + 1)
            right = min(M, right_exclusive - 1)
            if left <= right:
                range_add(1, 1, S, left, right)

    def point_value(x):
        k = 1
        l = 1
        r = S
        result = x

        while True:
            result += lazy[k]
            if l == r:
                return result

            mid = (l + r) >> 1
            if x <= mid:
                k <<= 1
                r = mid
            else:
                k = k << 1 | 1
                l = mid + 1

    print("\n".join(map(str, (point_value(x) for x in queries))))

if __name__ == "__main__":
    solve()