from typing import List


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, index: int, value: int) -> None:
        index += 1
        while index <= self.n:
            self.bit[index] += value
            index += index & -index

    def sum_prefix(self, end: int) -> int:
        """Returns the sum over indices [0, end)."""
        result = 0
        while end > 0:
            result += self.bit[end]
            end -= end & -end
        return result

    def kth(self, k: int) -> int:
        """Returns the smallest index whose prefix sum is at least k."""
        index = 0
        step = 1 << (self.n.bit_length() - 1)
        while step:
            nxt = index + step
            if nxt <= self.n and self.bit[nxt] < k:
                index = nxt
                k -= self.bit[nxt]
            step >>= 1
        return index


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        values = sorted(set(nums))
        rank = {value: i for i, value in enumerate(values)}
        size = len(values)

        count_tree = Fenwick(size)
        sum_tree = Fenwick(size)

        def add(value: int, delta: int) -> None:
            idx = rank[value]
            count_tree.add(idx, delta)
            sum_tree.add(idx, value * delta)

        def window_cost() -> int:
            total_count = x
            total_sum = sum_tree.sum_prefix(size)

            median_idx = count_tree.kth((total_count + 1) // 2)
            median = values[median_idx]

            count_le = count_tree.sum_prefix(median_idx + 1)
            sum_le = sum_tree.sum_prefix(median_idx + 1)

            left_cost = median * count_le - sum_le
            right_count = total_count - count_le
            right_sum = total_sum - sum_le
            right_cost = right_sum - median * right_count

            return left_cost + right_cost

        for i in range(x):
            add(nums[i], 1)

        window_costs = [0] * (n - x + 1)
        window_costs[0] = window_cost()

        for start in range(1, n - x + 1):
            add(nums[start - 1], -1)
            add(nums[start + x - 1], 1)
            window_costs[start] = window_cost()

        m = len(window_costs)
        inf = 10**30

        # prev[p] = minimum cost to choose exactly t-1 windows
        # among starts [0, p).
        prev = [0] * (m + 1)

        for t in range(1, k + 1):
            cur = [inf] * (m + 1)

            for p in range(m):
                skip = cur[p]

                # If selecting the window starting at p, all previous
                # windows must start at most p-x.
                previous_boundary = max(0, p - x + 1)
                select = prev[previous_boundary] + window_costs[p]

                cur[p + 1] = min(skip, select)

            prev = cur

        return prev[m]