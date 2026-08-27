import sys
from math import isqrt
from array import array
from bisect import bisect_right

sys.setrecursionlimit(1 << 20)


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    k = next(it)

    queries = []
    for qi in range(k):
        x = next(it)
        y = next(it)
        queries.append((x, y, qi))

    # Block size balancing:
    # O((number of used blocks) * N log N + K * block_size log N)
    block_size = max(1, min(n, n // max(1, isqrt(k))))

    groups = {}
    for x, y, qi in queries:
        block = (x - 1) // block_size
        groups.setdefault(block, []).append((y, x, qi))

    # Coordinate compression for the Fenwick tree over active A values.
    all_values = sorted(set(a + b))
    m_all = len(all_values)

    rank_a = [bisect_right(all_values, v) for v in a]
    rank_b_all = [bisect_right(all_values, v) for v in b]

    # Persistent segment tree for B prefixes.
    # Coordinates only need B values.
    b_values = sorted(set(b))
    m_b = len(b_values)
    rank_a_b = [bisect_right(b_values, v) for v in a]
    rank_b = [bisect_right(b_values, v) - 1 for v in b]

    left = array('i', [0])
    right = array('i', [0])
    cnt = array('i', [0])
    sm = array('q', [0])

    def update(node, lo, hi, pos, value):
        new_node = len(cnt)
        left.append(left[node])
        right.append(right[node])
        cnt.append(cnt[node] + 1)
        sm.append(sm[node] + value)

        if hi - lo > 1:
            mid = (lo + hi) >> 1
            if pos < mid:
                child = update(left[node], lo, mid, pos, value)
                left[new_node] = child
            else:
                child = update(right[node], mid, hi, pos, value)
                right[new_node] = child
        return new_node

    roots_b = [0] * (n + 1)
    prefix_sum_b = [0] * (n + 1)

    for i, value in enumerate(b):
        roots_b[i + 1] = update(roots_b[i], 0, m_b, rank_b[i], value)
        prefix_sum_b[i + 1] = prefix_sum_b[i] + value

    def prefix_count_sum(root, p):
        """Count and sum of values among the first p compressed B coordinates."""
        node = root
        lo = 0
        hi = m_b
        c = 0
        s = 0

        while hi - lo > 1:
            mid = (lo + hi) >> 1
            if p <= mid:
                node = left[node]
                hi = mid
            else:
                q = left[node]
                c += cnt[q]
                s += sm[q]
                node = right[node]
                lo = mid

        if node and p > lo:
            c += cnt[node]
            s += sm[node]

        return c, s

    def distance_to_b_prefix(root, total_count, total_sum, value, p):
        lc, ls = prefix_count_sum(root, p)
        return value * lc - ls + (total_sum - ls) - value * (total_count - lc)

    # Fenwick trees for the currently fixed A prefix.
    bit_count = [0] * (m_all + 1)
    bit_sum = [0] * (m_all + 1)

    def add_a(pos, value):
        while pos <= m_all:
            bit_count[pos] += 1
            bit_sum[pos] += value
            pos += pos & -pos

    def active_a_distance(value, pos, active_count, active_sum):
        c = 0
        s = 0
        while pos > 0:
            c += bit_count[pos]
            s += bit_sum[pos]
            pos -= pos & -pos
        return value * c - s + (active_sum - s) - value * (active_count - c)

    answers = [0] * k
    added = 0
    active_sum = 0

    for block in sorted(groups):
        fixed_len = block * block_size

        while added < fixed_len:
            add_a(rank_a[added], a[added])
            active_sum += a[added]
            added += 1

        block_queries = groups[block]
        block_queries.sort()

        current_y = 0
        base = 0

        for y, x, qi in block_queries:
            while current_y < y:
                value = b[current_y]
                if fixed_len:
                    base += active_a_distance(
                        value,
                        rank_b_all[current_y],
                        fixed_len,
                        active_sum
                    )
                current_y += 1

            residual = 0
            root = roots_b[y]
            total_sum = prefix_sum_b[y]

            for ai in range(fixed_len, x):
                value = a[ai]
                residual += distance_to_b_prefix(
                    root,
                    y,
                    total_sum,
                    value,
                    rank_a_b[ai]
                )

            answers[qi] = base + residual

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    main()