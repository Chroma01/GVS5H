import sys


def main():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    left = [-1] * n
    right = [-1] * n
    parent = [-1] * n

    stack = []
    for i, x in enumerate(a):
        last = -1
        while stack and a[stack[-1]] <= x:
            last = stack.pop()

        if stack:
            right[stack[-1]] = i
            parent[i] = stack[-1]

        if last != -1:
            left[i] = last
            parent[last] = i

        stack.append(i)

    root = stack[0]
    while parent[root] != -1:
        root = parent[root]

    order = []
    st = [root]
    while st:
        v = st.pop()
        order.append(v)
        if left[v] != -1:
            st.append(left[v])
        if right[v] != -1:
            st.append(right[v])

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    xl = [a[i] - pref[i] for i in range(n)]
    xr = [a[i] + pref[i + 1] for i in range(n)]

    size = 1
    while size < n:
        size <<= 1

    neg_inf = -(10 ** 30)
    seg_l = [neg_inf] * (2 * size)
    seg_r = [neg_inf] * (2 * size)

    for i in range(n):
        seg_l[size + i] = xl[i]
        seg_r[size + i] = xr[i]

    for i in range(size - 1, 0, -1):
        seg_l[i] = max(seg_l[i << 1], seg_l[i << 1 | 1])
        seg_r[i] = max(seg_r[i << 1], seg_r[i << 1 | 1])

    def range_max(seg, l, r):
        l += size
        r += size + 1
        ret = neg_inf
        while l < r:
            if l & 1:
                ret = max(ret, seg[l])
                l += 1
            if r & 1:
                r -= 1
                ret = max(ret, seg[r])
            l >>= 1
            r >>= 1
        return ret

    sub_sum = [0] * n
    sub_l = [0] * n
    sub_r = [0] * n

    for v in reversed(order):
        total = a[v]
        lo = hi = v

        if left[v] != -1:
            c = left[v]
            total += sub_sum[c]
            lo = sub_l[c]
            hi = sub_r[c]

        if right[v] != -1:
            c = right[v]
            total += sub_sum[c]
            lo = min(lo, sub_l[c])
            hi = max(hi, sub_r[c])

        sub_sum[v] = total
        sub_l[v] = lo
        sub_r[v] = hi

    can_full = [False] * n

    for v in order:
        lc = left[v]
        rc = right[v]

        if lc == -1:
            req_left = 0
            sum_left = 0
        else:
            l, r = sub_l[lc], sub_r[lc]
            req_left = range_max(seg_r, l, r) - pref[r + 1] + 1
            sum_left = sub_sum[lc]

        if rc == -1:
            req_right = 0
            sum_right = 0
        else:
            l, r = sub_l[rc], sub_r[rc]
            req_right = range_max(seg_l, l, r) + pref[l] + 1
            sum_right = sub_sum[rc]

        ok = False

        if a[v] >= req_left:
            if a[v] + sum_left >= req_right:
                ok = True

        if not ok and a[v] >= req_right:
            if a[v] + sum_right >= req_left:
                ok = True

        can_full[v] = ok

    # top[v] is the highest ancestor whose entire subtree can be absorbed
    # when the current slime already has size sub_sum[v].
    top = [0] * n
    top[root] = root

    for v in order:
        if v == root:
            continue

        p = parent[v]
        if sub_sum[v] > a[p]:
            top[v] = top[p]
        else:
            top[v] = v

    # side_cross[v] handles reaching the parent after consuming only the
    # child subtree on the side facing that parent.  The opposite child
    # subtree is not required to be fully consumable beforehand.
    side_cross = [False] * n

    for v in range(n):
        p = parent[v]
        if p == -1:
            continue

        if v < p:
            # v is the left child of p; consume the right side of v first.
            c = right[v]
            if c == -1:
                mass = a[v]
                side_cross[v] = mass > a[p]
            else:
                l, r = sub_l[c], sub_r[c]
                req = range_max(seg_l, l, r) + pref[l] + 1
                if a[v] >= req:
                    side_cross[v] = a[v] + sub_sum[c] > a[p]
        else:
            # v is the right child of p; consume the left side of v first.
            c = left[v]
            if c == -1:
                mass = a[v]
                side_cross[v] = mass > a[p]
            else:
                l, r = sub_l[c], sub_r[c]
                req = range_max(seg_r, l, r) - pref[r + 1] + 1
                if a[v] >= req:
                    side_cross[v] = a[v] + sub_sum[c] > a[p]

    ans = a[:]

    for i in range(n):
        best = a[i]

        if can_full[i]:
            best = max(best, sub_sum[top[i]])

        p = parent[i]
        if p != -1 and side_cross[i]:
            best = max(best, sub_sum[top[p]])

        ans[i] = best

    print(*ans)


if __name__ == "__main__":
    main()