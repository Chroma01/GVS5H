import sys
from bisect import bisect_left, bisect_right
from array import array


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0

    n = data[p]
    p += 1
    A = data[p:p + n]
    p += n
    B = data[p:p + n]
    p += n

    # Persistent segment trees for prefixes of B.
    coords = sorted(set(B))
    m = len(coords)

    left = array('i', [0])
    right = array('i', [0])
    cnt = array('i', [0])
    sm = array('q', [0])

    sys.setrecursionlimit(1000000)

    def update(node, lo, hi, pos):
        new_node = len(cnt)
        left.append(left[node])
        right.append(right[node])
        cnt.append(cnt[node] + 1)
        sm.append(sm[node] + coords[pos])

        if lo != hi:
            mid = (lo + hi) >> 1
            if pos <= mid:
                child = update(left[node], lo, mid, pos)
                left[new_node] = child
            else:
                child = update(right[node], mid + 1, hi, pos)
                right[new_node] = child
        return new_node

    roots = array('i', [0])
    if m == 1:
        for value in B:
            roots.append(update(roots[-1], 0, 0, 0))
    else:
        for value in B:
            rank = bisect_left(coords, value)
            roots.append(update(roots[-1], 0, m - 1, rank))

    # Prefix sums of B, used for the total sum in an absolute-difference query.
    bprefix = [0] * (n + 1)
    running = 0
    for i, value in enumerate(B, 1):
        running += value
        bprefix[i] = running

    # Block-prefix table:
    # table[q][y] = contribution of the first q complete A-blocks
    # against B[0:y].
    block_size = 700
    num_blocks = (n + block_size - 1) // block_size
    width = n + 1
    table = array('q', [0]) * ((num_blocks + 1) * width)

    for block in range(num_blocks):
        start = block * block_size
        end = min(n, start + block_size)
        vals = sorted(A[start:end])
        sz = len(vals)

        vpref = [0] * (sz + 1)
        s = 0
        for i, value in enumerate(vals, 1):
            s += value
            vpref[i] = s
        total_vals = s

        base = (block + 1) * width
        prev_base = block * width
        cumulative = 0

        for y in range(1, n + 1):
            b = B[y - 1]
            t = bisect_right(vals, b)
            cumulative += (
                b * t - vpref[t]
                + (total_vals - vpref[t]) - b * (sz - t)
            )
            table[base + y] = table[prev_base + y] + cumulative

    def less_than(root, pos):
        """Return (count, sum) of values whose compressed rank is < pos."""
        if pos <= 0:
            return 0, 0
        if pos >= m:
            return cnt[root], sm[root]

        lo = 0
        hi = m - 1
        node = root
        count_less = 0
        sum_less = 0

        while lo != hi:
            mid = (lo + hi) >> 1
            if pos <= mid:
                node = left[node]
                hi = mid
            else:
                lc = left[node]
                count_less += cnt[lc]
                sum_less += sm[lc]
                node = right[node]
                lo = mid + 1

        if lo < pos:
            count_less += cnt[node]
            sum_less += sm[node]
        return count_less, sum_less

    k = data[p]
    p += 1
    answers = []

    for _ in range(k):
        x = data[p]
        y = data[p + 1]
        p += 2

        complete_blocks = x // block_size
        remainder_start = complete_blocks * block_size
        remainder_end = x

        answer = table[complete_blocks * width + y]
        root = roots[y]
        total_b = bprefix[y]

        for i in range(remainder_start, remainder_end):
            value = A[i]
            rank = bisect_left(coords, value)
            less_count, less_sum = less_than(root, rank)
            greater_count = y - less_count
            answer += (
                value * less_count - less_sum
                + (total_b - less_sum) - value * greater_count
            )

        answers.append(str(answer))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()