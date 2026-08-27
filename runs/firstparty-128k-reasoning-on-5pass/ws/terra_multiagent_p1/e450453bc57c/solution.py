from typing import List
from bisect import bisect_left


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

        count_bit = Fenwick(m)
        sum_bit = Fenwick(m)

        def add_value(value: int, delta: int) -> None:
            pos = bisect_left(values, value) + 1
            count_bit.add(pos, delta)
            sum_bit.add(pos, value * delta)

        for i in range(x):
            add_value(nums[i], 1)

        costs = [0] * (n - x + 1)
        median_rank = (x + 1) // 2

        for start in range(n - x + 1):
            median_pos = count_bit.kth(median_rank)
            median = values[median_pos - 1]

            left_count = count_bit.query(median_pos)
            left_sum = sum_bit.query(median_pos)
            total_sum = sum_bit.query(m)

            costs[start] = (
                median * left_count - left_sum
                + (total_sum - left_sum) - median * (x - left_count)
            )

            if start + x < n:
                add_value(nums[start], -1)
                add_value(nums[start + x], 1)

        inf = 10**30
        prev = [0] * (n + 1)

        for chosen in range(1, k + 1):
            curr = [inf] * (n + 1)
            for length in range(1, n + 1):
                curr[length] = curr[length - 1]
                if length >= x and prev[length - x] != inf:
                    curr[length] = min(
                        curr[length],
                        prev[length - x] + costs[length - x]
                    )
            prev = curr

        return prev[n]