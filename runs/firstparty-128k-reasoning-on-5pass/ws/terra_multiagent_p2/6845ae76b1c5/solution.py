import sys
from array import array


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0

    n = data[p]
    p += 1
    a0 = data[p:p + n]
    p += n
    b0 = data[p:p + n]
    p += n

    k = data[p]
    p += 1
    raw_queries = []
    for qi in range(k):
        x = data[p]
        y = data[p + 1]
        p += 2
        raw_queries.append((x, y, qi))

    # Select a block size and, exploiting symmetry, decide whether to block A
    # or B. The estimate reflects:
    # - O(N^2 / block) simple preprocessing work
    # - O(sum of remainders * log N) persistent-tree work.
    candidates = []
    s = 64
    while s < n:
        candidates.append(s)
        ns = int(s * 1.28)
        if ns <= s:
            ns = s + 1
        s = ns
    candidates.append(n)

    best_cost = None
    best_s = 1
    swap = False

    xs = [q[0] for q in raw_queries]
    ys = [q[1] for q in raw_queries]

    for block in candidates:
        blocks = (n + block - 1) // block
        preprocess = n * blocks
        rem_x = sum(x % block for x in xs)
        rem_y = sum(y % block for y in ys)

        cost_x = preprocess + 10 * rem_x
        if best_cost is None or cost_x < best_cost:
            best_cost = cost_x
            best_s = block
            swap = False

        cost_y = preprocess + 10 * rem_y
        if cost_y < best_cost:
            best_cost = cost_y
            best_s = block
            swap = True

    block = best_s

    if not swap:
        A = a0
        B = b0
        queries = raw_queries
    else:
        A = b0
        B = a0
        queries = [(y, x, qi) for x, y, qi in raw_queries]

    # Compress values for the persistent segment tree over B prefixes.
    vals = sorted(set(A + B))
    rank = {v: i + 1 for i, v in enumerate(vals)}
    m = len(vals)

    # Persistent segment tree arrays. Node 0 is the null node.
    left = array('i', [0])
    right = array('i', [0])
    cnt = array('i', [0])
    sm = array('q', [0])

    def new_node(lc, rc, cc, ss):
        left.append(lc)
        right.append(rc)
        cnt.append(cc)
        sm.append(ss)
        return len(cnt) - 1

    roots = array('i', [0])

    # Build one persistent root per B prefix.
    for value in B:
        pos = rank[value]
        old = roots[-1]
        lo = 1
        hi = m
        path_nodes = []
        path_dirs = []

        while lo < hi:
            mid = (lo + hi) >> 1
            path_nodes.append(old)
            if pos <= mid:
                path_dirs.append(0)
                old = left[old]
                hi = mid
            else:
                path_dirs.append(1)
                old = right[old]
                lo = mid + 1

        cur = new_node(left[old], right[old], cnt[old] + 1, sm[old] + value)

        for z in range(len(path_nodes) - 1, -1, -1):
            old_parent = path_nodes[z]
            if path_dirs[z] == 0:
                cur = new_node(
                    cur,
                    right[old_parent],
                    cnt[old_parent] + 1,
                    sm[old_parent] + value
                )
            else:
                cur = new_node(
                    left[old_parent],
                    cur,
                    cnt[old_parent] + 1,
                    sm[old_parent] + value
                )

        roots.append(cur)

    pref_b_sum = [0] * (n + 1)
    for i, v in enumerate(B):
        pref_b_sum[i + 1] = pref_b_sum[i] + v

    def prefix_count_sum(root, pos):
        """Count and value sum among this version's values with rank <= pos."""
        node = root
        lo = 1
        hi = m
        res_c = 0
        res_s = 0

        while node and lo < hi:
            mid = (lo + hi) >> 1
            if pos <= mid:
                node = left[node]
                hi = mid
            else:
                lc = left[node]
                res_c += cnt[lc]
                res_s += sm[lc]
                node = right[node]
                lo = mid + 1

        if node and lo <= pos:
            res_c += cnt[node]
            res_s += sm[node]

        return res_c, res_s

    num_blocks = (n + block - 1) // block
    groups = [[] for _ in range(num_blocks + 1)]
    ans = [0] * k

    for x, y, qi in queries:
        groups[x // block].append((x, y, qi))

    # Sort B once by value. For every full A block, sweep it against this order.
    order_b = sorted(range(n), key=B.__getitem__)
    sorted_b_values = [B[i] for i in order_b]

    # Contributions of every complete A block to all queries that contain it.
    temp = [0] * n

    for b in range(num_blocks):
        l = b * block
        r = min(n, l + block)

        block_values = sorted(A[l:r])
        plen = len(block_values)
        block_pref = [0] * (plen + 1)
        for i, v in enumerate(block_values):
            block_pref[i + 1] = block_pref[i] + v
        total_a = block_pref[plen]

        t = 0
        sum_le = 0

        for z in range(n):
            v = sorted_b_values[z]
            while t < plen and block_values[t] <= v:
                sum_le += block_values[t]
                t += 1

            contribution = v * t - sum_le + (total_a - sum_le) - v * (plen - t)
            temp[order_b[z]] = contribution

        run = 0
        for j in range(n):
            run += temp[j]
            temp[j] = run

        # Every query in a later block contains this entire A block.
        for g in range(b + 1, num_blocks + 1):
            for _, y, qi in groups[g]:
                ans[qi] += temp[y - 1]

    # Add the incomplete final A block of every query using persistent B prefixes.
    for g in range(num_blocks + 1):
        base = g * block
        for x, y, qi in groups[g]:
            root = roots[y]
            total_sum_b = pref_b_sum[y]

            extra = 0
            for i in range(base, x):
                v = A[i]
                c_le, s_le = prefix_count_sum(root, rank[v])
                extra += (
                    v * c_le - s_le
                    + (total_sum_b - s_le)
                    - v * (y - c_le)
                )

            ans[qi] += extra

    sys.stdout.write("\n".join(map(str, ans)))


if __name__ == "__main__":
    solve()