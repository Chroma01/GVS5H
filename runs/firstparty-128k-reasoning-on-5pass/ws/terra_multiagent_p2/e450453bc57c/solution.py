from typing import List


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, index: int, value: int) -> None:
        while index <= self.n:
            self.bit[index] += value
            index += index & -index

    def query(self, index: int) -> int:
        result = 0
        while index > 0:
            result += self.bit[index]
            index -= index & -index
        return result

    def kth(self, target: int) -> int:
        """Return the smallest 1-based index with prefix sum at least target."""
        index = 0
        step = 1 << (self.n.bit_length() - 1)

        while step:
            nxt = index + step
            if nxt <= self.n and self.bit[nxt] < target:
                index = nxt
                target -= self.bit[nxt]
            step >>= 1

        return index + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        values = sorted(set(nums))
        compressed = {value: i + 1 for i, value in enumerate(values)}
        size = len(values)

        count_tree = Fenwick(size)
        sum_tree = Fenwick(size)

        def add_value(value: int, delta: int) -> None:
            pos = compressed[value]
            count_tree.add(pos, delta)
            sum_tree.add(pos, value * delta)

        window_count = n - x + 1
        costs = [0] * window_count

        for i in range(x):
            add_value(nums[i], 1)

        total_sum = sum(nums[:x])
        median_rank = (x + 1) // 2

        for start in range(window_count):
            median_pos = count_tree.kth(median_rank)
            median = values[median_pos - 1]

            # Includes all duplicate median values in the left side.
            left_count = count_tree.query(median_pos)
            left_sum = sum_tree.query(median_pos)
            right_count = x - left_count
            right_sum = total_sum - left_sum

            costs[start] = (
                median * left_count - left_sum
                + right_sum - median * right_count
            )

            if start + x < n:
                removed = nums[start]
                added = nums[start + x]
                add_value(removed, -1)
                add_value(added, 1)
                total_sum += added - removed

        inf = 10**30

        # prev[p] is the best cost for choosing exactly chosen-1 windows
        # entirely within nums[:p].
        prev = [0] * (n + 1)

        for chosen in range(1, k + 1):
            cur = [inf] * (n + 1)

            for prefix_len in range(1, n + 1):
                # Do not use an interval ending at prefix_len.
                cur[prefix_len] = cur[prefix_len - 1]

                # Use nums[prefix_len-x : prefix_len] as the final interval.
                if prefix_len >= x:
                    start = prefix_len - x
                    candidate = prev[start] + costs[start]
                    if candidate < cur[prefix_len]:
                        cur[prefix_len] = candidate

            prev = cur

        return prev[n]