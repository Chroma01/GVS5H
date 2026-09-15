import sys
from bisect import bisect_left, bisect_right


def normalize(people):
    res = []
    for s, t in people:
        if s < t:
            res.append((s, t, 1))
        else:
            res.append((t, s, -1))
    return res


def exact_feasible_intervals(N, intervals):
    """Exact oracle for small cases: contract equalities, then check acyclicity."""
    if not intervals:
        return True

    parent = list(range(N + 1))
    sz = [1] * (N + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        if sz[ra] < sz[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        sz[ra] += sz[rb]

    for l, r, d in intervals:
        union(l, r)

    adj = {}
    for l, r, d in intervals:
        root = find(l)
        if d == 1:
            for v in range(l + 1, r):
                rv = find(v)
                if root == rv:
                    return False
                if root not in adj:
                    adj[root] = set()
                adj[root].add(rv)
        else:
            for v in range(l + 1, r):
                rv = find(v)
                if root == rv:
                    return False
                if rv not in adj:
                    adj[rv] = set()
                adj[rv].add(root)

    adj = {u: list(s) for u, s in adj.items()}

    color = {}
    for start in list(adj.keys()):
        if color.get(start, 0) != 0:
            continue
        stack = [(start, 0)]
        color[start] = 1
        while stack:
            node, idx = stack[-1]
            lst = adj.get(node)
            if not lst:
                color[node] = 2
                stack.pop()
                continue
            if idx < len(lst):
                nxt = lst[idx]
                stack[-1] = (node, idx + 1)
                c = color.get(nxt, 0)
                if c == 1:
                    return False
                if c == 0:
                    color[nxt] = 1
                    stack.append((nxt, 0))
            else:
                color[node] = 2
                stack.pop()

    return True


def pair_feasible_intervals(intervals):
    """Pair-based characterization used by the solver."""
    k = len(intervals)
    for i in range(k):
        l1, r1, d1 = intervals[i]
        for j in range(i + 1, k):
            l2, r2, d2 = intervals[j]
            if l1 == l2 or r1 == r2:
                return False
            if d1 == d2 and ((l1 < l2 < r1 < r2) or (l2 < l1 < r2 < r1)):
                return False
    return True


def seg_update_min(data, size, pos, val):
    idx = pos + size
    if data[idx] == val:
        return
    data[idx] = val
    idx >>= 1
    while idx:
        j = idx << 1
        a = data[j]
        b = data[j | 1]
        nv = a if a < b else b
        if data[idx] == nv:
            break
        data[idx] = nv
        idx >>= 1


def seg_update_max(data, size, pos, val):
    idx = pos + size
    if data[idx] == val:
        return
    data[idx] = val
    idx >>= 1
    while idx:
        j = idx << 1
        a = data[j]
        b = data[j | 1]
        nv = a if a > b else b
        if data[idx] == nv:
            break
        data[idx] = nv
        idx >>= 1


def compute_min_left_arrays(N, M, L, R, D):
    """
    Sliding-window solver.
    D is 0 for left-to-right (+), 1 for right-to-left (-).
    Returns min_left[r] (1-based) for every right endpoint r (0-based).
    """
    if M == 0:
        return []

    vals_l = [[], []]
    vals_r = [[], []]
    for i in range(M):
        d = D[i]
        vals_l[d].append(L[i])
        vals_r[d].append(R[i])

    vals_l[0] = sorted(set(vals_l[0]))
    vals_l[1] = sorted(set(vals_l[1]))
    vals_r[0] = sorted(set(vals_r[0]))
    vals_r[1] = sorted(set(vals_r[1]))

    l_id = [
        {v: i for i, v in enumerate(vals_l[0])},
        {v: i for i, v in enumerate(vals_l[1])},
    ]
    r_id = [
        {v: i for i, v in enumerate(vals_r[0])},
        {v: i for i, v in enumerate(vals_r[1])},
    ]

    l_comp = [0] * M
    r_comp = [0] * M

    # Precompute compressed coordinates and orthogonal query ranges once.
    qR_lo = [0] * M
    qR_hi = [-1] * M
    qL_lo = [0] * M
    qL_hi = [-1] * M

    bl = bisect_left
    br = bisect_right

    for i in range(M):
        l = L[i]
        r = R[i]
        d = D[i]

        l_comp[i] = l_id[d][l]
        r_comp[i] = r_id[d][r]

        a = l + 1
        b = r - 1
        if a <= b:
            lo = bl(vals_r[d], a)
            hi = br(vals_r[d], b) - 1
            qR_lo[i] = lo
            qR_hi[i] = hi

            lo = bl(vals_l[d], a)
            hi = br(vals_l[d], b) - 1
            qL_lo[i] = lo
            qL_hi[i] = hi

    r_len = [len(vals_r[0]), len(vals_r[1])]
    l_len = [len(vals_l[0]), len(vals_l[1])]
    del l_id, r_id, vals_l, vals_r

    INF = N + 1

    segR_data = []
    segR_size = []
    segL_data = []
    segL_size = []

    for d in range(2):
        sz = 1
        while sz < r_len[d]:
            sz <<= 1
        segR_data.append([INF] * (2 * sz))
        segR_size.append(sz)

        sz = 1
        while sz < l_len[d]:
            sz <<= 1
        segL_data.append([0] * (2 * sz))
        segL_size.append(sz)

    cntL = [0] * (N + 2)
    cntR = [0] * (N + 2)

    upd_min = seg_update_min
    upd_max = seg_update_max

    def add_interval(i):
        l = L[i]
        r = R[i]
        d = D[i]

        cntL[l] += 1
        cntR[r] += 1

        # A feasible active window has at most one interval per normalized
        # left/right endpoint, so leaves can be updated directly.
        upd_min(segR_data[d], segR_size[d], r_comp[i], l)
        upd_max(segL_data[d], segL_size[d], l_comp[i], r)

    def remove_interval(i):
        l = L[i]
        r = R[i]
        d = D[i]

        cntL[l] -= 1
        cntR[r] -= 1

        upd_min(segR_data[d], segR_size[d], r_comp[i], INF)
        upd_max(segL_data[d], segL_size[d], l_comp[i], 0)

    def is_conflict(i):
        l = L[i]
        r = R[i]
        d = D[i]

        if cntL[l] or cntR[r]:
            return True

        # Pattern 1: active interval (li, ri) with li < l < ri < r.
        lo = qR_lo[i]
        hi = qR_hi[i]
        if lo <= hi:
            data = segR_data[d]
            size = segR_size[d]
            x = lo + size
            y = hi + size
            while x <= y:
                if x & 1:
                    if data[x] < l:
                        return True
                    x += 1
                if not (y & 1):
                    if data[y] < l:
                        return True
                    y -= 1
                x >>= 1
                y >>= 1

        # Pattern 2: active interval (li, ri) with l < li < r < ri.
        lo = qL_lo[i]
        hi = qL_hi[i]
        if lo <= hi:
            data = segL_data[d]
            size = segL_size[d]
            x = lo + size
            y = hi + size
            while x <= y:
                if x & 1:
                    if data[x] > r:
                        return True
                    x += 1
                if not (y & 1):
                    if data[y] > r:
                        return True
                    y -= 1
                x >>= 1
                y >>= 1

        return False

    min_left = [0] * M
    left = 0

    for right in range(M):
        while is_conflict(right):
            remove_interval(left)
            left += 1
        add_interval(right)
        min_left[right] = left + 1

    return min_left


def solve_case_sliding(N, people, queries):
    M = len(people)
    L = [0] * M
    R = [0] * M
    D = [0] * M
    for i, (s, t) in enumerate(people):
        if s < t:
            L[i] = s
            R[i] = t
            D[i] = 0
        else:
            L[i] = t
            R[i] = s
            D[i] = 1

    min_left = compute_min_left_arrays(N, M, L, R, D)
    return ["Yes" if min_left[r - 1] <= l else "No" for l, r in queries]


def solve_case_exact(N, people, queries):
    intervals = normalize(people)
    out = []
    for l, r in queries:
        out.append("Yes" if exact_feasible_intervals(N, intervals[l - 1:r]) else "No")
    return out


def solve_case_pair_small(N, people, queries):
    intervals = normalize(people)
    M = len(intervals)
    if M == 0:
        return []

    min_left = [1] * M
    left = 0
    for r in range(M):
        while left <= r and not pair_feasible_intervals(intervals[left:r + 1]):
            left += 1
        min_left[r] = left + 1

    return ["Yes" if min_left[r - 1] <= l else "No" for l, r in queries]


def run_random_tests(seed=123456, tests=80):
    import random

    rng = random.Random(seed)

    for test_id in range(tests):
        N = rng.randint(3, 8)

        valid = []
        for s in range(1, N + 1):
            for t in range(1, N + 1):
                if abs(s - t) > 1:
                    valid.append((s, t))

        rng.shuffle(valid)
        M = rng.randint(1, min(8, len(valid)))
        people = valid[:M]
        intervals = normalize(people)

        # Validate the pair characterization against the exact oracle.
        for mask in range(1, 1 << M):
            subset = [intervals[i] for i in range(M) if (mask >> i) & 1]
            if exact_feasible_intervals(N, subset) != pair_feasible_intervals(subset):
                print("FAIL")
                print("test_id", test_id)
                print("N", N)
                print("people", people)
                print("mask", mask)
                print("subset", subset)
                return False

        queries = [(l, r) for l in range(1, M + 1) for r in range(l, M + 1)]

        ans_exact = solve_case_exact(N, people, queries)
        ans_sliding = solve_case_sliding(N, people, queries)
        ans_pair = solve_case_pair_small(N, people, queries)

        if ans_sliding != ans_exact or ans_pair != ans_exact:
            print("FAIL")
            print("test_id", test_id)
            print("N", N)
            print("people", people)
            print("exact", ans_exact)
            print("sliding", ans_sliding)
            print("pair", ans_pair)
            return False

    print("PASS")
    return True


def run_stress_tests():
    import time

    # Large deterministic performance stress: many same-direction crossings,
    # alternating directions to exercise both segment-tree families.
    N = 400000
    M = 200000
    Q = 200000

    L = [0] * M
    R = [0] * M
    D = [0] * M

    max_l = N - 1005
    for i in range(M):
        l = (i % max_l) + 1
        r = l + 2 + (i % 1000)
        L[i] = l
        R[i] = r
        D[i] = i & 1

    t0 = time.perf_counter()
    min_left = compute_min_left_arrays(N, M, L, R, D)
    t1 = time.perf_counter()

    del L, R, D

    prev = 1
    for i, v in enumerate(min_left):
        if v < 1 or v > i + 1 or v < prev:
            print("STRESS FAIL", i, v, prev)
            return False
        prev = v

    yes = 0
    for k in range(Q):
        l = (k % M) + 1
        r = l + (k % 1000)
        if r > M:
            r = M
        if min_left[r - 1] <= l:
            yes += 1

    t2 = time.perf_counter()
    print(f"stress PASS yes={yes} compute={t1 - t0:.3f}s total={t2 - t0:.3f}s")
    return True


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        if run_random_tests():
            run_stress_tests()
        return

    p = 0
    N = int(data[p])
    p += 1
    M = int(data[p])
    p += 1
    Q = int(data[p])
    p += 1

    L = [0] * M
    R = [0] * M
    D = [0] * M

    for i in range(M):
        s = int(data[p])
        t = int(data[p + 1])
        p += 2
        if s < t:
            L[i] = s
            R[i] = t
            D[i] = 0
        else:
            L[i] = t
            R[i] = s
            D[i] = 1

    ql = [0] * Q
    qr = [0] * Q
    for k in range(Q):
        ql[k] = int(data[p])
        qr[k] = int(data[p + 1])
        p += 2

    del data

    min_left = compute_min_left_arrays(N, M, L, R, D)
    del L, R, D

    out = ["Yes" if min_left[qr[k] - 1] <= ql[k] else "No" for k in range(Q)]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()