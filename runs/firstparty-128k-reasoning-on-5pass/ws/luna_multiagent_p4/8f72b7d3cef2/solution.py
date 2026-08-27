import sys

sys.setrecursionlimit(2_000_000)


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    left = [-1] * n
    right = [-1] * n

    stack = []
    for i, x in enumerate(a):
        last = -1
        while stack and a[stack[-1]] < x:
            last = stack.pop()

        if stack:
            right[stack[-1]] = i
        if last != -1:
            left[i] = last

        stack.append(i)

    root = stack[0]

    order = []
    st = [root]
    while st:
        v = st.pop()
        order.append(v)
        if left[v] != -1:
            st.append(left[v])
        if right[v] != -1:
            st.append(right[v])

    sub_sum = [0] * n
    sub_l = list(range(n))
    sub_r = list(range(n))

    for v in reversed(order):
        total = a[v]
        l = v
        r = v

        if left[v] != -1:
            u = left[v]
            total += sub_sum[u]
            l = sub_l[u]

        if right[v] != -1:
            u = right[v]
            total += sub_sum[u]
            r = sub_r[u]

        sub_sum[v] = total
        sub_l[v] = l
        sub_r[v] = r

    size = 1
    while size < n:
        size <<= 1

    inf = 10**30
    mn = [inf] * (size << 1)
    mx = [-inf] * (size << 1)
    lazy = [None] * (size << 1)

    for i, x in enumerate(a):
        p = size + i
        mn[p] = x
        mx[p] = x

    for p in range(size - 1, 0, -1):
        mn[p] = min(mn[p << 1], mn[p << 1 | 1])
        mx[p] = max(mx[p << 1], mx[p << 1 | 1])

    def apply(p, value):
        mn[p] = value
        mx[p] = value
        lazy[p] = value

    def push(p):
        value = lazy[p]
        if value is not None:
            apply(p << 1, value)
            apply(p << 1 | 1, value)
            lazy[p] = None

    def point_set(p, nl, nr, index, value):
        if nl == nr:
            apply(p, value)
            return

        push(p)
        mid = (nl + nr) >> 1

        if index <= mid:
            point_set(p << 1, nl, mid, index, value)
        else:
            point_set(p << 1 | 1, mid + 1, nr, index, value)

        mn[p] = min(mn[p << 1], mn[p << 1 | 1])
        mx[p] = max(mx[p << 1], mx[p << 1 | 1])

    def replace_greater(p, nl, nr, ql, qr, threshold, value):
        if nr < ql or qr < nl or mx[p] <= threshold:
            return

        if ql <= nl and nr <= qr and mn[p] > threshold:
            apply(p, value)
            return

        if nl == nr:
            apply(p, value)
            return

        push(p)
        mid = (nl + nr) >> 1

        replace_greater(
            p << 1, nl, mid, ql, qr, threshold, value
        )
        replace_greater(
            p << 1 | 1, mid + 1, nr, ql, qr, threshold, value
        )

        mn[p] = min(mn[p << 1], mn[p << 1 | 1])
        mx[p] = max(mx[p << 1], mx[p << 1 | 1])

    for v in reversed(order):
        point_set(1, 0, size - 1, v, sub_sum[v])

        if left[v] != -1:
            u = left[v]
            replace_greater(
                1,
                0,
                size - 1,
                sub_l[u],
                sub_r[u],
                a[v],
                sub_sum[v],
            )

        if right[v] != -1:
            u = right[v]
            replace_greater(
                1,
                0,
                size - 1,
                sub_l[u],
                sub_r[u],
                a[v],
                sub_sum[v],
            )

    ans = [0] * n

    def collect(p, nl, nr):
        if nl == nr:
            if nl < n:
                ans[nl] = mn[p]
            return

        push(p)
        mid = (nl + nr) >> 1
        collect(p << 1, nl, mid)
        collect(p << 1 | 1, mid + 1, nr)

    collect(1, 0, size - 1)
    print(*ans)


if __name__ == "__main__":
    main()