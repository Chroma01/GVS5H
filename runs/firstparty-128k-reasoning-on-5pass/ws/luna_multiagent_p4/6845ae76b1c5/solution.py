import sys
import math
from bisect import bisect_right


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0

    n = data[pos]
    pos += 1
    a = data[pos:pos + n]
    pos += n
    b = data[pos:pos + n]
    pos += n

    k = data[pos]
    pos += 1

    # A slightly smaller block than N/sqrt(K) reduces the expensive
    # persistent-tree work in partial blocks while keeping preprocessing
    # manageable.
    block = max(1, int(n / math.sqrt(4 * k)))

    groups = {}
    for qi in range(k):
        x = data[pos]
        y = data[pos + 1]
        pos += 2
        boundary = (x // block) * block
        groups.setdefault(boundary, []).append((x, y, qi))

    coords = sorted(set(b))
    m = len(coords)
    coord_index = {v: i for i, v in enumerate(coords)}

    left = [0]
    right = [0]
    count = [0]
    total = [0]

    def update(node, lo, hi, p, value):
        new_node = len(count)
        left.append(left[node])
        right.append(right[node])
        count.append(count[node] + 1)
        total.append(total[node] + value)

        if hi - lo == 1:
            return new_node

        mid = (lo + hi) >> 1
        if p < mid:
            left[new_node] = update(left[node], lo, mid, p, value)
        else:
            right[new_node] = update(right[node], mid, hi, p, value)
        return new_node

    roots = [0]
    for value in b:
        roots.append(
            update(roots[-1], 0, m, coord_index[value], value)
        )

    a_rank = [bisect_right(coords, value) for value in a]

    def absolute_sum(root, y, value, rank):
        if rank == 0:
            lower_count = 0
            lower_sum = 0
        elif rank >= m:
            lower_count = count[root]
            lower_sum = total[root]
        else:
            lo = 0
            hi = m
            node = root
            lower_count = 0
            lower_sum = 0

            while hi - lo > 1:
                mid = (lo + hi) >> 1
                left_node = left[node]
                if rank <= mid:
                    node = left_node
                    hi = mid
                else:
                    lower_count += count[left_node]
                    lower_sum += total[left_node]
                    node = right[node]
                    lo = mid

            if lo < rank:
                lower_count += count[node]
                lower_sum += total[node]

        upper_count = y - lower_count
        upper_sum = total[root] - lower_sum
        return (
            value * lower_count - lower_sum
            + upper_sum - value * upper_count
        )

    sorted_b = sorted((value, index) for index, value in enumerate(b))
    answers = [0] * k

    current_boundary = 0
    sorted_a = []

    for boundary in sorted(groups):
        while current_boundary < boundary:
            end = min(boundary, current_boundary + block)
            chunk = sorted(a[current_boundary:end])

            merged = []
            i = j = 0
            while i < len(sorted_a) and j < len(chunk):
                if sorted_a[i] <= chunk[j]:
                    merged.append(sorted_a[i])
                    i += 1
                else:
                    merged.append(chunk[j])
                    j += 1

            if i < len(sorted_a):
                merged.extend(sorted_a[i:])
            if j < len(chunk):
                merged.extend(chunk[j:])

            sorted_a = merged
            current_boundary = end

        sum_a = sum(sorted_a)
        contribution = [0] * n

        ptr = 0
        lower_sum = 0
        for value, original_index in sorted_b:
            while ptr < boundary and sorted_a[ptr] <= value:
                lower_sum += sorted_a[ptr]
                ptr += 1

            upper_count = boundary - ptr
            upper_sum = sum_a - lower_sum
            contribution[original_index] = (
                value * ptr - lower_sum
                + upper_sum - value * upper_count
            )

        complete_prefix = [0] * (n + 1)
        for j in range(n):
            complete_prefix[j + 1] = (
                complete_prefix[j] + contribution[j]
            )

        for x, y, qi in groups[boundary]:
            root = roots[y]
            result = complete_prefix[y]

            for idx in range(boundary, x):
                result += absolute_sum(
                    root, y, a[idx], a_rank[idx]
                )

            answers[qi] = result

    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()