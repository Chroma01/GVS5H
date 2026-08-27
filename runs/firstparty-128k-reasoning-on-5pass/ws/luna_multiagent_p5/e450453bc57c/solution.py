from typing import List


class Fenwick:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, index: int, value: int) -> None:
        while index <= self.n:
            self.bit[index] += value
            index += index & -index

    def sum(self, index: int) -> int:
        result = 0
        while index > 0:
            result += self.bit[index]
            index -= index & -index
        return result

    def kth(self, target: int) -> int:
        """Return the smallest index whose prefix sum is at least target."""
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

        coordinates = sorted(set(nums))
        rank = {value: i + 1 for i, value in enumerate(coordinates)}
        m = len(coordinates)

        count_tree = Fenwick(m)
        sum_tree = Fenwick(m)

        window_sum = 0
        for i in range(x):
            r = rank[nums[i]]
            count_tree.add(r, 1)
            sum_tree.add(r, nums[i])
            window_sum += nums[i]

        costs = []
        median_rank_target = (x + 1) // 2

        for start in range(n - x + 1):
            median_rank = count_tree.kth(median_rank_target)
            median = coordinates[median_rank - 1]

            left_count = count_tree.sum(median_rank)
            left_sum = sum_tree.sum(median_rank)
            right_count = x - left_count
            right_sum = window_sum - left_sum

            cost = (
                median * left_count - left_sum
                + right_sum - median * right_count
            )
            costs.append(cost)

            if start + x < n:
                outgoing = nums[start]
                incoming = nums[start + x]

                outgoing_rank = rank[outgoing]
                count_tree.add(outgoing_rank, -1)
                sum_tree.add(outgoing_rank, -outgoing)
                window_sum -= outgoing

                incoming_rank = rank[incoming]
                count_tree.add(incoming_rank, 1)
                sum_tree.add(incoming_rank, incoming)
                window_sum += incoming

        inf = 10**30

        # prev[i] = minimum cost to choose exactly (taken - 1) windows
        # from the prefix nums[:i].
        prev = [0] + [inf] * n

        for taken in range(1, k + 1):
            cur = [inf] * (n + 1)

            for end in range(1, n + 1):
                cur[end] = cur[end - 1]

                if end >= x:
                    start = end - x
                    if prev[start] != inf:
                        candidate = prev[start] + costs[start]
                        if candidate < cur[end]:
                            cur[end] = candidate

            prev = cur

        return prev[n]