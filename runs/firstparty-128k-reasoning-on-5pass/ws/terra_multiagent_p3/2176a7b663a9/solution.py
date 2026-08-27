import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0

    n = data[p]
    p += 1
    w = [0] + data[p:p + n]
    p += n

    limit = 2 * n
    L = [0] * (n + 1)
    R = [0] * (n + 1)

    INF = 10**30
    by_l = [INF] * (limit + 2)
    by_r = [INF] * (limit + 2)

    for i in range(1, n + 1):
        l = data[p]
        r = data[p + 1]
        p += 2
        L[i] = l
        R[i] = r
        if w[i] < by_l[l]:
            by_l[l] = w[i]
        if w[i] < by_r[r]:
            by_r[r] = w[i]

    # Minimum weight among intervals whose right endpoint is at most x.
    pref_r = [INF] * (limit + 2)
    cur = INF
    for x in range(1, limit + 1):
        if by_r[x] < cur:
            cur = by_r[x]
        pref_r[x] = cur

    # Minimum weight among intervals whose left endpoint is at least x.
    suff_l = [INF] * (limit + 3)
    cur = INF
    for x in range(limit, 0, -1):
        if by_l[x] < cur:
            cur = by_l[x]
        suff_l[x] = cur

    size = 1
    while size < limit + 1:
        size <<= 1

    tree_l = [INF] * (2 * size)
    tree_r = [INF] * (2 * size)

    for x in range(1, limit + 1):
        tree_l[size + x - 1] = by_l[x]
        tree_r[size + x - 1] = by_r[x]

    for i in range(size - 1, 0, -1):
        a = tree_l[i << 1]
        b = tree_l[i << 1 | 1]
        tree_l[i] = a if a < b else b

        a = tree_r[i << 1]
        b = tree_r[i << 1 | 1]
        tree_r[i] = a if a < b else b

    def range_min(tree, left, right):
        if left > right:
            return INF
        left += size - 1
        right += size - 1
        res = INF
        while left <= right:
            if left & 1:
                if tree[left] < res:
                    res = tree[left]
                left += 1
            if not (right & 1):
                if tree[right] < res:
                    res = tree[right]
                right -= 1
            left >>= 1
            right >>= 1
        return res

    q = data[p]
    p += 1
    ans = []

    for _ in range(q):
        s = data[p]
        t = data[p + 1]
        p += 2

        ls, rs = L[s], R[s]
        lt, rt = L[t], R[t]

        # A direct edge exists exactly when the two intervals are disjoint.
        if rs < lt or rt < ls:
            ans.append(str(w[s] + w[t]))
            continue

        best_internal = INF

        # Paths with two edges: an interval wholly left of both endpoints,
        # or wholly right of both endpoints.
        left_limit = ls if ls < lt else lt
        right_limit = rs if rs > rt else rt

        x = pref_r[left_limit - 1]
        if x < best_internal:
            best_internal = x

        x = suff_l[right_limit + 1]
        if x < best_internal:
            best_internal = x

        # Chordless three-edge paths have one of exactly two orientations.
        #
        # s - x - y - t with x left of y:
        #   Lt <= Rx < Ls, and Rt < Ly <= Rs.
        if ls > lt and rs > rt:
            a = range_min(tree_r, lt, ls - 1)
            b = range_min(tree_l, rt + 1, rs)
            if a < INF and b < INF:
                v = a + b
                if v < best_internal:
                    best_internal = v

        # s - x - y - t with y left of x:
        #   Ls <= Ry < Lt, and Rs < Lx <= Rt.
        elif ls < lt and rs < rt:
            a = range_min(tree_r, ls, lt - 1)
            b = range_min(tree_l, rs + 1, rt)
            if a < INF and b < INF:
                v = a + b
                if v < best_internal:
                    best_internal = v

        if best_internal == INF:
            ans.append("-1")
        else:
            ans.append(str(w[s] + w[t] + best_internal))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()