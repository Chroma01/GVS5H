import sys
from bisect import bisect_right
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

    queries_by_block = []

    # Balance the O(number_of_blocks * N) fixed-prefix work and
    # O(K * block_size * log N) persistent-tree queries.
    block_size = max(1, int(n / (k * max(1.0, n.bit_length())) ** 0.5))
    block_count = (n + block_size - 1) // block_size
    queries_by_block = [[] for _ in range(block_count)]

    queries = []
    for qi in range(k):
        x = data[p]
        y = data[p + 1]
        p += 2
        queries_by_block[(x - 1) // block_size].append((y, x, qi))
        queries.append((x, y))

    # Persistent segment tree for prefixes of B.
    coords = sorted(set(b))
    m = len(coords)

    left = array("i", [0])
    right = array("i", [0])
    count = array("i", [0])
    total = array("q", [0])

    def add_node(prev, lo, hi, pos, value):
        node = len(left)
        left.append(left[prev])
        right.append(right[prev])
        count.append(count[prev] + 1)
        total.append(total[prev] + value)

        if hi - lo > 1:
            mid = (lo + hi) >> 1
            if pos < mid:
                child = add_node(left[prev], lo, mid, pos, value)
                left[node] = child
            else:
                child = add_node(right[prev], mid, hi, pos, value)
                right[node] = child
        return node

    roots = [0] * (n + 1)
    for i, value in enumerate(b, 1):
        pos = bisect_right(coords, value) - 1
        roots[i] = add_node(roots[i - 1], 0, m, pos, value)

    def query_leq(root, rank):
        """Return (count, sum) of values whose compressed index is < rank."""
        if rank <= 0 or root == 0:
            return 0, 0
        if rank >= m:
            return count[root], total[root]

        node = root
        lo = 0
        hi = m
        result_count = 0
        result_sum = 0

        while hi - lo > 1 and node:
            mid = (lo + hi) >> 1
            if rank <= mid:
                node = left[node]
                hi = mid
            else:
                ln = left[node]
                result_count += count[ln]
                result_sum += total[ln]
                node = right[node]
                lo = mid

        if node and lo < rank:
            result_count += count[node]
            result_sum += total[node]

        return result_count, result_sum

    a_ranks = [bisect_right(coords, value) for value in a]
    b_order = sorted(range(n), key=b.__getitem__)
    answers = [0] * k

    # Incrementally maintain sorted A-prefixes, avoiding repeated sorting
    # of every fixed prefix.
    sorted_base = []
    base_total = 0

    for block in range(block_count):
        block_left = block * block_size
        block_right = min(n, block_left + block_size)
        block_values = a[block_left:block_right]
        block_ranks = a_ranks[block_left:block_right]

        group = queries_by_block[block]

        if group:
            base_len = block_left
            base_prefix = [0] * (n + 1)

            if base_len:
                contributions = [0] * n
                ptr = 0
                sum_le = 0

                for idx in b_order:
                    value = b[idx]
                    while ptr < base_len and sorted_base[ptr] <= value:
                        sum_le += sorted_base[ptr]
                        ptr += 1

                    greater_count = base_len - ptr
                    greater_sum = base_total - sum_le
                    contributions[idx] = (
                        value * ptr - sum_le
                        + greater_sum - value * greater_count
                    )

                running = 0
                for i in range(n):
                    running += contributions[i]
                    base_prefix[i + 1] = running

            # Each suffix contribution is answered directly from the
            # persistent B-prefix tree. Total pairs handled are O(K*S).
            for y, x, qi in group:
                root = roots[y]
                suffix = 0
                limit = x - block_left

                for i in range(limit):
                    value = block_values[i]
                    le_count, le_sum = query_leq(root, block_ranks[i])
                    suffix += (
                        value * le_count - le_sum
                        + total[root] - le_sum
                        - value * (y - le_count)
                    )

                answers[qi] = base_prefix[y] + suffix

        # Prepare the sorted fixed prefix for the next block by merging,
        # rather than sorting the entire prefix again.
        chunk = sorted(block_values)
        if not sorted_base:
            sorted_base = chunk
        else:
            merged = []
            i = j = 0
            old_len = len(sorted_base)
            chunk_len = len(chunk)

            while i < old_len and j < chunk_len:
                if sorted_base[i] <= chunk[j]:
                    merged.append(sorted_base[i])
                    i += 1
                else:
                    merged.append(chunk[j])
                    j += 1

            if i < old_len:
                merged.extend(sorted_base[i:])
            if j < chunk_len:
                merged.extend(chunk[j:])

            sorted_base = merged

        base_total += sum(block_values)

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()