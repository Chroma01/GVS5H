import sys
from bisect import bisect_left, bisect_right
from array import array


def solve():
    input = sys.stdin.buffer.readline
    N, M, Q = map(int, input().split())

    left = [0] * M
    right = [0] * M
    typ = [0] * M

    by_left = {}
    by_right = {}

    for i in range(M):
        s, t = map(int, input().split())
        if s < t:
            a, b, z = s, t, 1
        else:
            a, b, z = t, s, -1

        left[i] = a
        right[i] = b
        typ[i] = z

        if a not in by_left:
            by_left[a] = [[], []]
        if b not in by_right:
            by_right[b] = [[], []]

        if z == 1:
            by_left[a][0].append(i)
            by_right[b][0].append(i)
        else:
            by_left[a][1].append(i)
            by_right[b][1].append(i)

    size = 1
    while size < M:
        size <<= 1

    def find_crossings(indices):
        seg_left = [None] * (2 * size)
        seg_left_suffix_max_right = [None] * (2 * size)
        seg_right = [None] * (2 * size)
        seg_right_prefix_min_left = [None] * (2 * size)

        for i in indices:
            p = size + i
            seg_left[p] = array("i", [left[i]])
            seg_left_suffix_max_right[p] = array("i", [right[i]])
            seg_right[p] = array("i", [right[i]])
            seg_right_prefix_min_left[p] = array("i", [left[i]])

        for node in range(size - 1, 0, -1):
            lc = node << 1
            rc = lc | 1

            la = seg_left[lc]
            ra = seg_left[rc]

            if la is None:
                seg_left[node] = seg_left[rc]
                seg_left_suffix_max_right[node] = seg_left_suffix_max_right[rc]
                seg_right[node] = seg_right[rc]
                seg_right_prefix_min_left[node] = seg_right_prefix_min_left[rc]
                continue

            if ra is None:
                seg_left[node] = seg_left[lc]
                seg_left_suffix_max_right[node] = seg_left_suffix_max_right[lc]
                seg_right[node] = seg_right[lc]
                seg_right_prefix_min_left[node] = seg_right_prefix_min_left[lc]
                continue

            lsa = seg_left_suffix_max_right[lc]
            rsa = seg_left_suffix_max_right[rc]

            merged_left = array("i")
            merged_right_values = array("i")
            x = y = 0

            while x < len(la) and y < len(ra):
                if la[x] <= ra[y]:
                    merged_left.append(la[x])
                    merged_right_values.append(lsa[x])
                    x += 1
                else:
                    merged_left.append(ra[y])
                    merged_right_values.append(rsa[y])
                    y += 1

            while x < len(la):
                merged_left.append(la[x])
                merged_right_values.append(lsa[x])
                x += 1

            while y < len(ra):
                merged_left.append(ra[y])
                merged_right_values.append(rsa[y])
                y += 1

            suffix = array("i", [0]) * len(merged_right_values)
            best = -1
            for k in range(len(merged_right_values) - 1, -1, -1):
                if merged_right_values[k] > best:
                    best = merged_right_values[k]
                suffix[k] = best

            lb = seg_right[lc]
            rb = seg_right[rc]
            lpa = seg_right_prefix_min_left[lc]
            rpa = seg_right_prefix_min_left[rc]

            merged_right = array("i")
            merged_left_values = array("i")
            x = y = 0

            while x < len(lb) and y < len(rb):
                if lb[x] <= rb[y]:
                    merged_right.append(lb[x])
                    merged_left_values.append(lpa[x])
                    x += 1
                else:
                    merged_right.append(rb[y])
                    merged_left_values.append(rpa[y])
                    y += 1

            while x < len(lb):
                merged_right.append(lb[x])
                merged_left_values.append(lpa[x])
                x += 1

            while y < len(rb):
                merged_right.append(rb[y])
                merged_left_values.append(rpa[y])
                y += 1

            prefix = array("i", [0]) * len(merged_left_values)
            best = N + 1
            for k in range(len(merged_left_values)):
                if merged_left_values[k] < best:
                    best = merged_left_values[k]
                prefix[k] = best

            seg_left[node] = merged_left
            seg_left_suffix_max_right[node] = suffix
            seg_right[node] = merged_right
            seg_right_prefix_min_left[node] = prefix

        def has_conflict(node, a, b):
            arr = seg_left[node]
            if arr is not None:
                lo = bisect_right(arr, a)
                hi = bisect_left(arr, b)
                if lo < hi and seg_left_suffix_max_right[node][lo] > b:
                    return True

            arr = seg_right[node]
            if arr is not None:
                lo = bisect_right(arr, a)
                hi = bisect_left(arr, b)
                if lo < hi and seg_right_prefix_min_left[node][hi - 1] < a:
                    return True

            return False

        def first_crossing(node, nl, nr, ql, a, b):
            if nr <= ql:
                return M

            if nl >= ql and not has_conflict(node, a, b):
                return M

            if nr - nl == 1:
                return nl if nl < M else M

            mid = (nl + nr) >> 1
            ans = first_crossing(node << 1, nl, mid, ql, a, b)
            if ans != M:
                return ans
            return first_crossing(node << 1 | 1, mid, nr, ql, a, b)

        result = [M] * M
        for i in indices:
            result[i] = first_crossing(
                1, 0, size, i + 1, left[i], right[i]
            )
        return result

    positive = [i for i in range(M) if typ[i] == 1]
    negative = [i for i in range(M) if typ[i] == -1]

    nxt_pos = find_crossings(positive)
    nxt_neg = find_crossings(negative)

    nxt = [min(nxt_pos[i], nxt_neg[i]) for i in range(M)]

    for groups in (by_left, by_right):
        for pair in groups.values():
            pair[0].sort()
            pair[1].sort()

            same_a = pair[0]
            same_b = pair[1]

            for i in same_a:
                p = bisect_right(same_b, i)
                if p < len(same_b):
                    nxt[i] = min(nxt[i], same_b[p])

            for i in same_b:
                p = bisect_right(same_a, i)
                if p < len(same_a):
                    nxt[i] = min(nxt[i], same_a[p])

    limit = [M - 1] * (M + 1)
    for i in range(M - 1, -1, -1):
        limit[i] = min(limit[i + 1], nxt[i] - 1)

    out = []
    for _ in range(Q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        out.append("Yes" if r <= limit[l] else "No")

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()