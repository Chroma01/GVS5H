import sys
from array import array


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    p = 0

    n = data[p]
    p += 1
    a = data[p:p + n]
    p += n
    b = data[p:p + n]
    p += n

    k = data[p]
    p += 1
    queries = []
    for qi in range(k):
        x = data[p]
        y = data[p + 1]
        p += 2
        queries.append((x, y, qi))

    values = sorted(set(a + b))
    m = len(values)
    rank = {v: i + 1 for i, v in enumerate(values)}

    # Persistent segment tree for B prefixes.
    # roots[y] stores all B[0:y].
    left = array('i', [0])
    right = array('i', [0])
    count = array('i', [0])
    total = array('q', [0])
    roots = array('i', [0])

    def clone(old, value):
        left.append(left[old])
        right.append(right[old])
        count.append(count[old] + 1)
        total.append(total[old] + value)
        return len(count) - 1

    for value in b:
        pos = rank[value]
        old_root = roots[-1]

        new_root = clone(old_root, value)
        roots.append(new_root)

        old_node = old_root
        new_node = new_root
        lo = 1
        hi = m

        while lo < hi:
            mid = (lo + hi) >> 1
            if pos <= mid:
                old_child = left[old_node]
                new_child = clone(old_child, value)
                left[new_node] = new_child
                old_node = old_child
                new_node = new_child
                hi = mid
            else:
                old_child = right[old_node]
                new_child = clone(old_child, value)
                right[new_node] = new_child
                old_node = old_child
                new_node = new_child
                lo = mid + 1

    def distance_to_b_prefix(y, value, value_rank):
        """Return sum_{j < y} abs(value - B[j])."""
        node = roots[y]
        lo = 1
        hi = m
        less_count = 0
        less_sum = 0

        while node and lo < hi:
            mid = (lo + hi) >> 1
            if value_rank <= mid:
                node = left[node]
                hi = mid
            else:
                child = left[node]
                less_count += count[child]
                less_sum += total[child]
                node = right[node]
                lo = mid + 1

        if node:
            less_count += count[node]
            less_sum += total[node]

        all_sum = total[roots[y]]
        return (
            value * less_count
            - less_sum
            + (all_sum - less_sum)
            - value * (y - less_count)
        )

    # The block method avoids a 2D Mo traversal.  A block has one fixed
    # A-prefix base and at most BLOCK extra A values per query.
    block_size = 400
    block_count = (n + block_size - 1) // block_size
    groups = [[] for _ in range(block_count)]

    for x, y, qi in queries:
        groups[(x - 1) // block_size].append((x, y, qi))

    # Value order is used to compute all distances from a fixed A multiset
    # to B positions by one sorted sweep.
    sorted_b = sorted((value, index) for index, value in enumerate(b))

    answers = [0] * k
    sorted_base_a = []
    base_end_now = 0
    base_sum_now = 0

    for block_id, group in enumerate(groups):
        if not group:
            continue

        base_end = block_id * block_size

        if base_end_now < base_end:
            added = sorted(a[base_end_now:base_end])
            base_sum_now += sum(added)

            old = sorted_base_a
            merged = []
            append = merged.append
            i = 0
            j = 0
            old_len = len(old)
            add_len = len(added)

            while i < old_len and j < add_len:
                if old[i] <= added[j]:
                    append(old[i])
                    i += 1
                else:
                    append(added[j])
                    j += 1

            if i < old_len:
                merged.extend(old[i:])
            if j < add_len:
                merged.extend(added[j:])

            sorted_base_a = merged
            base_end_now = base_end

        max_y = max(y for _, y, _ in group)
        base_values = sorted_base_a
        base_count = len(base_values)
        base_sum = base_sum_now

        # dist_b[j] = sum_{i < base_end} abs(A[i] - B[j]).
        dist_b = [0] * max_y
        ptr = 0
        left_sum = 0

        for bv, bidx in sorted_b:
            if bidx >= max_y:
                continue

            while ptr < base_count and base_values[ptr] <= bv:
                left_sum += base_values[ptr]
                ptr += 1

            dist_b[bidx] = (
                bv * ptr
                - left_sum
                + (base_sum - left_sum)
                - bv * (base_count - ptr)
            )

        # Prefix the base contributions only at requested Y positions.
        running = 0
        current_y = 0
        for x, y, qi in sorted(group, key=lambda q: q[1]):
            while current_y < y:
                running += dist_b[current_y]
                current_y += 1
            answers[qi] = running

        # Add contributions of the short A suffix using persistent B prefixes.
        for x, y, qi in group:
            extra = 0
            for ai in range(base_end, x):
                value = a[ai]
                extra += distance_to_b_prefix(y, value, rank[value])
            answers[qi] += extra

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()