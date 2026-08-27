from typing import List


class Fenwick:
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index: int, value: int) -> None:
        while index <= self.size:
            self.tree[index] += value
            index += index & -index

    def prefix_sum(self, index: int) -> int:
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result

    def kth(self, rank: int) -> int:
        index = 0
        step = 1 << (self.size.bit_length() - 1)

        while step:
            candidate = index + step
            if candidate <= self.size and self.tree[candidate] < rank:
                index = candidate
                rank -= self.tree[candidate]
            step >>= 1

        return index + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        values = sorted(set(nums))
        compressed = {value: i + 1 for i, value in enumerate(values)}

        count_tree = Fenwick(len(values))
        sum_tree = Fenwick(len(values))
        total_sum = 0

        def update(value: int, delta: int) -> None:
            nonlocal total_sum
            index = compressed[value]
            count_tree.add(index, delta)
            sum_tree.add(index, value * delta)
            total_sum += value * delta

        for i in range(x):
            update(nums[i], 1)

        window_count = n - x + 1
        costs = [0] * window_count
        median_rank = (x + 1) // 2

        def get_cost() -> int:
            median_index = count_tree.kth(median_rank)
            median = values[median_index - 1]

            left_count = count_tree.prefix_sum(median_index)
            left_sum = sum_tree.prefix_sum(median_index)

            right_count = x - left_count
            right_sum = total_sum - left_sum

            return (
                median * left_count
                - left_sum
                + right_sum
                - median * right_count
            )

        costs[0] = get_cost()

        for start in range(1, window_count):
            update(nums[start - 1], -1)
            update(nums[start + x - 1], 1)
            costs[start] = get_cost()

        inf = 10**30
        previous = [0] + [inf] * n

        for selected in range(1, k + 1):
            current = [inf] * (n + 1)

            for prefix_length in range(1, n + 1):
                current[prefix_length] = current[prefix_length - 1]

                if prefix_length >= x:
                    start = prefix_length - x
                    candidate = previous[start] + costs[start]
                    if candidate < current[prefix_length]:
                        current[prefix_length] = candidate

            previous = current

        return previous[n]