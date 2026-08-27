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
        """Return the smallest index having prefix frequency at least k."""
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
        rank = {value: i + 1 for i, value in enumerate(values)}
        m = len(values)

        count_tree = Fenwick(m)
        sum_tree = Fenwick(m)

        def add_value(value: int, delta: int) -> None:
            pos = rank[value]
            count_tree.add(pos, delta)
            sum_tree.add(pos, value * delta)

        def get_window_cost() -> int:
            # The lower median is optimal, including when x is even.
            median_pos = count_tree.kth((x + 1) // 2)
            median = values[median_pos - 1]

            left_count = count_tree.query(median_pos)
            left_sum = sum_tree.query(median_pos)
            total_sum = sum_tree.query(m)

            right_count = x - left_count
            right_sum = total_sum - left_sum

            return (
                median * left_count - left_sum
                + right_sum - median * right_count
            )

        for value in nums[:x]:
            add_value(value, 1)

        costs = [0] * (n - x + 1)
        for start in range(n - x + 1):
            costs[start] = get_window_cost()

            if start + x < n:
                add_value(nums[start], -1)
                add_value(nums[start + x], 1)

        # prev[i] is the best cost for exactly (chosen - 1) windows
        # using only nums[0:i].
        prev = [0] * (n + 1)
        inf = 10**30

        for chosen in range(1, k + 1):
            cur = [inf] * (n + 1)

            for i in range(1, n + 1):
                cur[i] = cur[i - 1]

                if i >= x and prev[i - x] != inf:
                    candidate = prev[i - x] + costs[i - x]
                    if candidate < cur[i]:
                        cur[i] = candidate

            prev = cur

        return prev[n]