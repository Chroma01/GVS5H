import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = [0] + data[1:]

    # Prefix distinct counts.
    pref = [0] * (n + 1)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(1, n + 1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        pref[i] = cnt

    # Suffix distinct counts.
    suf = [0] * (n + 2)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(n, 0, -1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        suf[i] = cnt

    # Lazy range-add / range-maximum segment tree.
    size = 1
    while size < n + 1:
        size <<= 1

    neg = -10**9
    mx = [neg] * (size * 2)
    lazy = [0] * (size * 2)
    height = size.bit_length() - 1

    def pull(k):
        mx[k] = lazy[k] + max(mx[k << 1], mx[k << 1 | 1])

    def range_add(left, right, value):
        # Add value to [left, right).
        if left >= right:
            return

        l = left + size
        r = right + size
        l0 = l
        r0 = r

        while l < r:
            if l & 1:
                mx[l] += value
                lazy[l] += value
                l += 1
            if r & 1:
                r -= 1
                mx[r] += value
                lazy[r] += value
            l >>= 1
            r >>= 1

        for h in range(1, height + 1):
            x = l0 >> h
            y = (r0 - 1) >> h
            pull(x)
            if x != y:
                pull(y)

    def point_set(pos, value):
        # Every position is inserted before it can receive any range update,
        # so no pending lazy tag exists on its root-to-leaf path.
        p = pos + size
        mx[p] = value
        p >>= 1
        while p:
            pull(p)
            p >>= 1

    # At second cut j=2, only first cut i=1 is possible.
    # Value for cut i is:
    # distinct(A[1..i]) + distinct(A[i+1..j]).
    point_set(1, pref[1] + 1)

    last = [0] * (n + 1)
    last[a[1]] = 1
    last[a[2]] = 2

    ans = neg

    for j in range(2, n):
        # The right subarray is A[j+1..n].
        ans = max(ans, mx[1] + suf[j + 1])

        # Advance the second cut from j to j+1.
        if j + 1 < n:
            x = a[j + 1]
            # Existing first cuts i in [last[x], j-1] gain one distinct
            # value in their middle segment. If x has not appeared before,
            # all existing cuts i in [1, j-1] gain one.
            left = max(1, last[x])
            range_add(left, j, 1)

            # Add the newly valid first cut i=j. Its middle segment is the
            # one-element segment A[j+1].
            point_set(j, pref[j] + 1)
            last[x] = j + 1

    print(ans)


if __name__ == "__main__":
    solve()