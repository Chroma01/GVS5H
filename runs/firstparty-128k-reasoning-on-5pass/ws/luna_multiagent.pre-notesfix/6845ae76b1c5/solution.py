import sys
from bisect import bisect_left
from array import array


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    A = [next(it) for _ in range(n)]
    B = [next(it) for _ in range(n)]

    k = next(it)
    queries = []
    groups = {}

    block_size = 300
    for qi in range(k):
        x = next(it)
        y = next(it)
        boundary = ((x - 1) // block_size) * block_size
        queries.append((x, y, boundary))
        groups.setdefault(boundary, set()).add(y)

    # Persistent segment tree over prefixes of B.
    values = sorted(set(B))
    m = len(values)

    left = array("i", [0])
    right = array("i", [0])
    count = array("i", [0])
    total = array("q", [0])

    def update(prev, lo, hi, pos, value):
        node = len(count)
        left.append(left[prev])
        right.append(right[prev])
        count.append(count[prev] + 1)
        total.append(total[prev] + value)

        if hi - lo > 1:
            mid = (lo + hi) >> 1
            if pos < mid:
                left[node] = update(left[prev], lo, mid, pos, value)
            else:
                right[node] = update(right[prev], mid, hi, pos, value)

        return node

    roots = [0]
    for value in B:
        pos = bisect_left(values, value)
        roots.append(update(roots[-1], 0, m, pos, value))

    def less_than(root, pos):
        """Return count and sum of values whose compressed index is < pos."""
        if pos <= 0:
            return 0, 0
        if pos >= m:
            return count[root], total[root]

        lo = 0
        hi = m
        node = root
        c = 0
        s = 0

        while hi - lo > 1:
            mid = (lo + hi) >> 1
            if pos <= mid:
                node = left[node]
                hi = mid
            else:
                lc = left[node]
                c += count[lc]
                s += total[lc]
                node = right[node]
                lo = mid

        # The descent ends at a leaf. Include it when its index is < pos.
        if lo < pos:
            c += count[node]
            s += total[node]

        return c, s

    sorted_b = sorted((value, index) for index, value in enumerate(B))

    boundary_tables = {0: {y: 0 for y in groups.get(0, ())}}

    sorted_a = []
    boundary_sum = 0
    max_boundary = ((n - 1) // block_size) * block_size

    for boundary in range(block_size, max_boundary + 1, block_size):
        chunk = sorted(A[boundary - block_size:boundary])

        merged = []
        i = 0
        j = 0
        old_len = len(sorted_a)
        chunk_len = len(chunk)

        while i < old_len and j < chunk_len:
            if sorted_a[i] <= chunk[j]:
                merged.append(sorted_a[i])
                i += 1
            else:
                merged.append(chunk[j])
                j += 1

        if i < old_len:
            merged.extend(sorted_a[i:])
        if j < chunk_len:
            merged.extend(chunk[j:])

        sorted_a = merged
        boundary_sum += sum(chunk)

        wanted = groups.get(boundary)
        if not wanted:
            continue

        max_y = max(wanted)
        contribution = [0] * max_y

        ptr = 0
        low_sum = 0
        size_a = boundary

        for value, original_index in sorted_b:
            while ptr < size_a and sorted_a[ptr] <= value:
                low_sum += sorted_a[ptr]
                ptr += 1

            current = (
                value * ptr
                - low_sum
                + (boundary_sum - low_sum)
                - value * (size_a - ptr)
            )

            if original_index < max_y:
                contribution[original_index] = current

        table = {}
        running = 0
        for idx, current in enumerate(contribution, 1):
            running += current
            if idx in wanted:
                table[idx] = running

        boundary_tables[boundary] = table

    answers = [0] * k

    for qi, (x, y, boundary) in enumerate(queries):
        answer = boundary_tables[boundary][y]
        root = roots[y]

        for idx in range(boundary, x):
            value = A[idx]
            pos = bisect_left(values, value)
            less_count, less_sum = less_than(root, pos)

            answer += (
                value * less_count
                - less_sum
                + (total[root] - less_sum)
                - value * (y - less_count)
            )

        answers[qi] = answer

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()