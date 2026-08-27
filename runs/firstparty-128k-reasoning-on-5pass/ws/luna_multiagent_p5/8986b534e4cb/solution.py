import sys
from array import array
from bisect import bisect_left, bisect_right


class Fenwick:
    __slots__ = ("n", "bit")

    def __init__(self, n):
        self.n = n
        self.bit = array("i", [0]) * (n + 1)

    def add(self, i, value):
        bit = self.bit
        n = self.n
        while i <= n:
            bit[i] += value
            i += i & -i

    def prefix_sum(self, i):
        bit = self.bit
        result = 0
        while i:
            result += bit[i]
            i -= i & -i
        return result

    def kth(self, k):
        bit = self.bit
        n = self.n
        step = 1 << (n.bit_length() - 1)
        index = 0
        while step:
            nxt = index + step
            if nxt <= n and bit[nxt] < k:
                index = nxt
                k -= bit[nxt]
            step >>= 1
        return index + 1


class DynamicRangeReporter:
    __slots__ = ("intervals", "base", "leaf", "keys", "fws")

    def __init__(self, intervals, ids, town_count, person_count):
        self.intervals = intervals
        self.base = person_count + 1

        leaf = 1
        while leaf <= town_count:
            leaf <<= 1
        self.leaf = leaf

        keys = {}
        multiplier = self.base

        # Every segment-tree node receives its points in sorted
        # (right endpoint, person index) order.
        for person in sorted(ids, key=lambda i: intervals[i][1]):
            left, right = intervals[person]
            encoded = right * multiplier + person
            node = leaf + left - 1
            while node:
                arr = keys.get(node)
                if arr is None:
                    arr = array("Q")
                    keys[node] = arr
                arr.append(encoded)
                node >>= 1

        self.keys = keys
        self.fws = {
            node: Fenwick(len(arr))
            for node, arr in keys.items()
        }

    def _update(self, person, delta):
        left, right = self.intervals[person]
        encoded = right * self.base + person
        node = self.leaf + left - 1

        while node:
            arr = self.keys[node]
            position = bisect_left(arr, encoded) + 1
            self.fws[node].add(position, delta)
            node >>= 1

    def add(self, person):
        self._update(person, 1)

    def remove(self, person):
        self._update(person, -1)

    def _extract_from_node(self, node, low_encoded, high_encoded):
        arr = self.keys[node]
        fw = self.fws[node]

        left_pos = bisect_left(arr, low_encoded)
        right_pos = bisect_right(arr, high_encoded)

        before = fw.prefix_sum(left_pos)
        remaining = fw.prefix_sum(right_pos) - before
        result = []

        while remaining:
            position = fw.kth(before + 1)
            encoded = arr[position - 1]
            person = encoded % self.base
            result.append(person)

            self.remove(person)
            remaining -= 1

        return result

    def query_and_remove(self, x_low, x_high, y_low, y_high):
        if x_low > x_high or y_low > y_high:
            return []

        left_node = self.leaf + x_low - 1
        right_node = self.leaf + x_high - 1

        low_encoded = y_low * self.base
        high_encoded = y_high * self.base + self.base - 1

        result = []

        while left_node <= right_node:
            if left_node & 1:
                if left_node in self.keys:
                    result.extend(
                        self._extract_from_node(
                            left_node, low_encoded, high_encoded
                        )
                    )
                left_node += 1

            if not (right_node & 1):
                if right_node in self.keys:
                    result.extend(
                        self._extract_from_node(
                            right_node, low_encoded, high_encoded
                        )
                    )
                right_node -= 1

            left_node >>= 1
            right_node >>= 1

        return result


def solve():
    input = sys.stdin.buffer.readline
    n, m, q = map(int, input().split())

    intervals = [(0, 0)] * m
    directions = [0] * m
    by_left = {}
    by_right = {}

    for i in range(m):
        s, t = map(int, input().split())

        if s < t:
            left, right, direction = s, t, 1
        else:
            left, right, direction = t, s, -1

        intervals[i] = (left, right)
        directions[i] = direction

        by_left.setdefault(left, []).append(i)
        by_right.setdefault(right, []).append(i)

    next_conflict = [m] * m

    # Intervals sharing either endpoint are always incompatible.
    # Linking consecutive indices is sufficient for all subarray queries.
    for groups in (by_left, by_right):
        for group in groups.values():
            group.sort()
            for a, b in zip(group, group[1:]):
                if b < next_conflict[a]:
                    next_conflict[a] = b

    positive = [i for i in range(m) if directions[i] == 1]
    negative = [i for i in range(m) if directions[i] == -1]

    reporters = {
        1: DynamicRangeReporter(intervals, positive, n, m),
        -1: DynamicRangeReporter(intervals, negative, n, m),
    }

    for current in range(m):
        left, right = intervals[current]
        reporter = reporters[directions[current]]

        # Earlier interval [a,b] with a < left < b < right.
        for previous in reporter.query_and_remove(
            1, left - 1, left + 1, right - 1
        ):
            if current < next_conflict[previous]:
                next_conflict[previous] = current

        # Earlier interval [a,b] with left < a < right < b.
        for previous in reporter.query_and_remove(
            left + 1, right - 1, right + 1, n
        ):
            if current < next_conflict[previous]:
                next_conflict[previous] = current

        reporter.add(current)

    # earliest_conflict[i] is the first conflicting person index
    # among persons i, i+1, ..., M-1.
    suffix_min = [m] * (m + 1)
    best = m

    for i in range(m - 1, -1, -1):
        if next_conflict[i] < best:
            best = next_conflict[i]
        suffix_min[i] = best

    answer = []

    for _ in range(q):
        left, right = map(int, input().split())
        left -= 1
        right -= 1

        answer.append("Yes" if suffix_min[left] > right else "No")

    sys.stdout.write("\n".join(answer))


if __name__ == "__main__":
    solve()