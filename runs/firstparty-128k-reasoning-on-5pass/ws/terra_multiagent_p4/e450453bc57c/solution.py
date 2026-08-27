from typing import List


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, index: int, delta: int) -> None:
        while index <= self.n:
            self.bit[index] += delta
            index += index & -index

    def query(self, index: int) -> int:
        result = 0
        while index > 0:
            result += self.bit[index]
            index -= index & -index
        return result

    def kth(self, k: int) -> int:
        index = 0
        step = 1 << (self.n.bit_length() - 1)

        while step:
            nxt = index + step
            if nxt <= self.n and self.bit[nxt] < k:
                index = nxt
                k -= self.bit[nxt]
            step >>= 1

        return index + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        values = sorted(set(nums))
        m = len(values)
        compressed = {value: i + 1 for i, value in enumerate(values)}

        count_tree = Fenwick(m)
        sum_tree = Fenwick(m)
        total_sum = 0

        def add_value(value: int, delta: int) -> None:
            nonlocal total_sum
            pos = compressed[value]
            count_tree.add(pos, delta)
            sum_tree.add(pos, value * delta)
            total_sum += value * delta

        def window_cost() -> int:
            median_pos = count_tree.kth((x + 1) // 2)
            median = values[median_pos - 1]

            left_count = count_tree.query(median_pos)
            left_sum = sum_tree.query(median_pos)
            right_count = x - left_count
            right_sum = total_sum - left_sum

            return (
                median * left_count
                - left_sum
                + right_sum
                - median * right_count
            )

        for i in range(x):
            add_value(nums[i], 1)

        costs = [0] * (n - x + 1)
        costs[0] = window_cost()

        for start in range(1, n - x + 1):
            add_value(nums[start - 1], -1)
            add_value(nums[start + x - 1], 1)
            costs[start] = window_cost()

        inf = 10**30

        # Zero selected windows have cost zero for every prefix.
        prev = [0] * (n + 1)

        for chosen in range(1, k + 1):
            curr = [inf] * (n + 1)

            for length in range(1, n + 1):
                curr[length] = curr[length - 1]

                if length >= x:
                    start = length - x
                    candidate = prev[start] + costs[start]
                    if candidate < curr[length]:
                        curr[length] = candidate

            prev = curr

        return prev[n]