import sys
from array import array
from bisect import bisect_right

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    A = [next(it) for _ in range(n)]
    B = [next(it) for _ in range(n)]
    k = next(it)

    queries = []
    ys = set()
    for _ in range(k):
        x = next(it)
        y = next(it)
        queries.append((x, y))
        ys.add(y)

    ys = sorted(ys)
    y_rank = {y: i for i, y in enumerate(ys)}
    d = len(ys)

    block_size = max(1, int(n ** 0.5))
    block_count = (n + block_size - 1) // block_size

    # For every A-block and every queried Y, store
    # sum over all A-values in the block and B-prefix of length Y.
    block_table = array('q', [0]) * (block_count * d)

    for block in range(block_count):
        left = block * block_size
        right = min(n, left + block_size)
        vals = sorted(A[left:right])

        pref = [0]
        total = 0
        for v in vals:
            total += v
            pref.append(total)

        current = 0
        rank = 0
        target_pos = 0

        for j, b in enumerate(B, 1):
            pos = bisect_right(vals, b)
            current += (
                b * pos - pref[pos]
                + (pref[-1] - pref[pos])
                - b * (len(vals) - pos)
            )

            if target_pos < d and j == ys[target_pos]:
                block_table[block * d + target_pos] = current
                target_pos += 1

    # Persistent segment trees over compressed B-values.
    coords = sorted(set(B))
    m = len(coords)
    b_pos = [bisect_right(coords, v) - 1 for v in B]

    left_child = array('i', [0])
    right_child = array('i', [0])
    count = array('i', [0])
    total_sum = array('q', [0])

    sys.setrecursionlimit(1_000_000)

    def update(old, l, r, p, value):
        node = len(count)
        left_child.append(left_child[old])
        right_child.append(right_child[old])
        count.append(count[old] + 1)
        total_sum.append(total_sum[old] + value)

        if r - l > 1:
            mid = (l + r) >> 1
            if p < mid:
                nl = update(left_child[old], l, mid, p, value)
                left_child[node] = nl
            else:
                nr = update(right_child[old], mid, r, p, value)
                right_child[node] = nr
        return node

    roots = array('i', [0])
    for value, p in zip(B, b_pos):
        roots.append(update(roots[-1], 0, m, p, value))

    def prefix_query(node, l, r, limit):
        if node == 0 or limit <= l:
            return 0, 0
        if r <= limit:
            return count[node], total_sum[node]

        mid = (l + r) >> 1
        if limit <= mid:
            return prefix_query(left_child[node], l, mid, limit)

        c1 = count[left_child[node]]
        s1 = total_sum[left_child[node]]
        c2, s2 = prefix_query(right_child[node], mid, r, limit)
        return c1 + c2, s1 + s2

    answers = []

    for x, y in queries:
        full_blocks = x // block_size
        yr = y_rank[y]
        ans = 0

        base = yr
        for block in range(full_blocks):
            ans += block_table[block * d + base]

        start = full_blocks * block_size
        root = roots[y]

        for idx in range(start, x):
            a = A[idx]
            limit = bisect_right(coords, a)
            cnt_le, sum_le = prefix_query(root, 0, m, limit)
            cnt_gt = y - cnt_le
            sum_gt = 0  # filled from the prefix total below

            total_b_sum = total_sum[root]
            sum_gt = total_b_sum - sum_le

            ans += a * cnt_le - sum_le
            ans += sum_gt - a * cnt_gt

        answers.append(str(ans))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()