import sys


def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    size = 1
    while size < n:
        size <<= 1
    seg = [0] * (2 * size)
    seg[size:size + n] = a
    for i in range(size - 1, 0, -1):
        left = seg[i << 1]
        right = seg[i << 1 | 1]
        seg[i] = left if left >= right else right

    def range_max(l, r):
        # Inclusive endpoints.
        l += size
        r += size
        res = 0
        while l <= r:
            if l & 1:
                if seg[l] > res:
                    res = seg[l]
                l += 1
            if not (r & 1):
                if seg[r] > res:
                    res = seg[r]
                r -= 1
            l >>= 1
            r >>= 1
        return res

    def find_first(l, r, value):
        # Find the leftmost index in [l,r] having exactly value.
        stack = [(1, 0, size - 1)]
        while stack:
            node, nl, nr = stack.pop()
            if nr < l or r < nl or seg[node] < value:
                continue
            if nl == nr:
                return nl
            mid = (nl + nr) >> 1
            # Push right first, so left is processed first.
            stack.append((node << 1 | 1, mid + 1, nr))
            stack.append((node << 1, nl, mid))
        return -1

    pref = [0] * (n + 1)
    for i, x in enumerate(a):
        pref[i + 1] = pref[i] + x

    # Each segment record: [l, r, maximum, positions_of_maximum, child_ids]
    segments = []
    segments.append([0, n - 1, 0, None, None])

    ptr = 0
    while ptr < len(segments):
        l, r, _, _, _ = segments[ptr]
        maximum = range_max(l, r)

        maxima = []
        children_ranges = []
        pending = [(l, r)]

        while pending:
            x, y = pending.pop()
            if x > y:
                continue
            cur = range_max(x, y)
            if cur == maximum:
                p = find_first(x, y, maximum)
                maxima.append(p)
                if x < p:
                    pending.append((x, p - 1))
                if p < y:
                    pending.append((p + 1, y))
            else:
                children_ranges.append((x, y))

        maxima.sort()
        child_ids = []
        for x, y in children_ranges:
            child_ids.append(len(segments))
            segments.append([x, y, 0, None, None])

        segments[ptr] = [l, r, maximum, maxima, child_ids]
        ptr += 1

    m = len(segments)
    head = [-1] * m
    tail = [-1] * m
    ans = [0] * n
    nxt = [-1] * n

    def finalize(group_id, value):
        p = head[group_id]
        while p != -1:
            ans[p] = value
            p = nxt[p]

    for sid in range(m - 1, -1, -1):
        l, r, maximum, maxima, child_ids = segments[sid]
        total = pref[r + 1] - pref[l]

        h = -1
        t = -1

        def append_group(gid):
            nonlocal h, t
            if head[gid] == -1:
                return
            if h == -1:
                h = head[gid]
                t = tail[gid]
            else:
                nxt[t] = head[gid]
                t = tail[gid]

        for cid in child_ids:
            cl, cr = segments[cid][0], segments[cid][1]
            child_sum = pref[cr + 1] - pref[cl]
            if head[cid] != -1:
                if child_sum > maximum:
                    append_group(cid)
                else:
                    finalize(cid, child_sum)

        for p in maxima:
            can_start = (
                (p > l and a[p - 1] < maximum) or
                (p < r and a[p + 1] < maximum)
            )
            if can_start:
                if h == -1:
                    h = t = p
                else:
                    nxt[t] = p
                    t = p
            else:
                ans[p] = maximum

        head[sid] = h
        tail[sid] = t

    root_sum = pref[n]
    if head[0] != -1:
        finalize(0, root_sum)

    print(*ans)


if __name__ == "__main__":
    solve()