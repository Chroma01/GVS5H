from typing import List


class Fenwick:
    def __init__(self, size: int):
        self.size = size
        self.count = [0] * (size + 1)
        self.total = [0] * (size + 1)

    def add(self, index: int, count_delta: int, total_delta: int) -> None:
        while index <= self.size:
            self.count[index] += count_delta
            self.total[index] += total_delta
            index += index & -index

    def prefix_count(self, index: int) -> int:
        result = 0
        while index > 0:
            result += self.count[index]
            index -= index & -index
        return result

    def prefix_sum(self, index: int) -> int:
        result = 0
        while index > 0:
            result += self.total[index]
            index -= index & -index
        return result

    def kth(self, rank: int) -> int:
        index = 0
        step = 1 << (self.size.bit_length() - 1)

        while step:
            next_index = index + step
            if next_index <= self.size and self.count[next_index] < rank:
                index = next_index
                rank -= self.count[next_index]
            step >>= 1

        return index + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)

        values = sorted(set(nums))
        compressed = {value: i + 1 for i, value in enumerate(values)}

        fenwick = Fenwick(len(values))
        window_sum = 0

        for i in range(x):
            value = nums[i]
            fenwick.add(compressed[value], 1, value)
            window_sum += value

        window_count = n - x + 1
        costs = [0] * window_count

        def get_cost() -> int:
            median_index = fenwick.kth((x + 1) // 2)
            median = values[median_index - 1]

            left_count = fenwick.prefix_count(median_index)
            left_sum = fenwick.prefix_sum(median_index)
            right_count = x - left_count
            right_sum = window_sum - left_sum

            return (
                median * left_count
                - left_sum
                + right_sum
                - median * right_count
            )

        costs[0] = get_cost()

        for start in range(1, window_count):
            outgoing = nums[start - 1]
            incoming = nums[start + x - 1]

            fenwick.add(compressed[outgoing], -1, -outgoing)
            fenwick.add(compressed[incoming], 1, incoming)
            window_sum += incoming - outgoing

            costs[start] = get_cost()

        inf = 10**30

        # prev[p] = minimum cost to choose exactly t-1 windows
        # whose starting indices are in [0, p-1].
        prev = [0] * (window_count + 1)

        for t in range(1, k + 1):
            curr = [inf] * (window_count + 1)

            for p in range(1, window_count + 1):
                # Skip the window starting at p - 1.
                best = curr[p - 1]

                if t == 1:
                    candidate = costs[p - 1]
                    if candidate < best:
                        best = candidate
                elif p >= x:
                    # Taking start p-1 requires all previous starts < p-x.
                    candidate = prev[p - x] + costs[p - 1]
                    if candidate < best:
                        best = candidate

                curr[p] = best

            prev = curr

        return prev[window_count]