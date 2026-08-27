from typing import List


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def query(self, i: int) -> int:
        total = 0
        while i > 0:
            total += self.bit[i]
            i -= i & -i
        return total

    def kth(self, k: int) -> int:
        """Return the smallest index whose prefix count is at least k."""
        idx = 0
        step = 1 << (self.n.bit_length() - 1)

        while step:
            nxt = idx + step
            if nxt <= self.n and self.bit[nxt] < k:
                idx = nxt
                k -= self.bit[nxt]
            step >>= 1

        return idx + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        values = sorted(set(nums))
        m = len(values)
        position = {value: i + 1 for i, value in enumerate(values)}

        count_tree = Fenwick(m)
        sum_tree = Fenwick(m)

        def add_value(value: int, delta: int) -> None:
            index = position[value]
            count_tree.add(index, delta)
            sum_tree.add(index, value * delta)

        def get_window_cost() -> int:
            # Lower median, valid for both odd and even window lengths.
            median_rank = (x + 1) // 2
            median_index = count_tree.kth(median_rank)
            median = values[median_index - 1]

            # Prefix includes every occurrence equal to the median.
            left_count = count_tree.query(median_index)
            left_sum = sum_tree.query(median_index)

            total_sum = sum_tree.query(m)
            right_count = x - left_count
            right_sum = total_sum - left_sum

            return (
                median * left_count - left_sum
                + right_sum - median * right_count
            )

        for i in range(x):
            add_value(nums[i], 1)

        costs = [0] * (n - x + 1)
        costs[0] = get_window_cost()

        for start in range(1, n - x + 1):
            add_value(nums[start - 1], -1)
            add_value(nums[start + x - 1], 1)
            costs[start] = get_window_cost()

        inf = 10**30

        # prev[i]: minimum cost for exactly t - 1 windows in first i elements.
        # For zero chosen windows, every prefix has cost zero.
        prev = [0] * (n + 1)

        for _ in range(1, k + 1):
            cur = [inf] * (n + 1)

            for i in range(1, n + 1):
                # Do not use element i - 1 as the end of a selected window.
                cur[i] = cur[i - 1]

                # Select the length-x window ending at i - 1.
                if i >= x and prev[i - x] != inf:
                    candidate = prev[i - x] + costs[i - x]
                    if candidate < cur[i]:
                        cur[i] = candidate

            prev = cur

        return prev[n]