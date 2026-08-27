from typing import List


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, index: int, value: int) -> None:
        while index <= self.n:
            self.tree[index] += value
            index += index & -index

    def prefix_sum(self, index: int) -> int:
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result

    def kth(self, k: int) -> int:
        index = 0
        step = 1 << (self.n.bit_length() - 1)

        while step:
            nxt = index + step
            if nxt <= self.n and self.tree[nxt] < k:
                index = nxt
                k -= self.tree[nxt]
            step >>= 1

        return index + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        values = sorted(set(nums))
        rank = {value: i + 1 for i, value in enumerate(values)}
        compressed = [rank[value] for value in nums]

        count_tree = Fenwick(len(values))
        sum_tree = Fenwick(len(values))
        window_sum = 0

        def update(position: int, delta: int) -> None:
            nonlocal window_sum
            value = nums[position]
            index = compressed[position]
            count_tree.add(index, delta)
            sum_tree.add(index, delta * value)
            window_sum += delta * value

        for position in range(x):
            update(position, 1)

        def window_cost() -> int:
            median_index = count_tree.kth((x + 1) // 2)
            median = values[median_index - 1]

            left_count = count_tree.prefix_sum(median_index)
            left_sum = sum_tree.prefix_sum(median_index)

            right_count = x - left_count
            right_sum = window_sum - left_sum

            return (
                median * left_count
                - left_sum
                + right_sum
                - median * right_count
            )

        window_count = n - x + 1
        costs = [0] * window_count
        costs[0] = window_cost()

        for start in range(1, window_count):
            update(start - 1, -1)
            update(start + x - 1, 1)
            costs[start] = window_cost()

        inf = 10**30

        # prev[i] is the minimum cost to choose exactly taken - 1
        # non-overlapping windows within nums[:i].
        prev = [0] * (n + 1)

        for taken in range(1, k + 1):
            cur = [inf] * (n + 1)

            for end in range(1, n + 1):
                cur[end] = cur[end - 1]

                if end >= x:
                    start = end - x
                    candidate = prev[start] + costs[start]
                    if candidate < cur[end]:
                        cur[end] = candidate

            prev = cur

        return prev[n]