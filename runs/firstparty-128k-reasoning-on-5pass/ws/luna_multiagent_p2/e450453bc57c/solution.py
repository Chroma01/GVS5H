from typing import List
import heapq


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        window_count = n - x + 1

        low = []   # max-heap via negated values
        high = []  # min-heap

        removed = [False] * n
        where = [-1] * n  # 0 for low, 1 for high

        low_size = high_size = 0
        low_sum = high_sum = 0
        target_low = (x + 1) // 2

        def prune(heap) -> None:
            while heap and removed[heap[0][1]]:
                heapq.heappop(heap)

        def rebalance() -> None:
            nonlocal low_size, high_size, low_sum, high_sum

            prune(low)
            prune(high)

            total = low_size + high_size
            target = min(target_low, total)

            while low_size > target:
                neg_value, idx = heapq.heappop(low)
                value = -neg_value

                low_size -= 1
                low_sum -= value
                high_size += 1
                high_sum += value
                where[idx] = 1
                heapq.heappush(high, (value, idx))
                prune(low)

            while low_size < target:
                value, idx = heapq.heappop(high)

                high_size -= 1
                high_sum -= value
                low_size += 1
                low_sum += value
                where[idx] = 0
                heapq.heappush(low, (-value, idx))
                prune(high)

        def add(idx: int) -> None:
            nonlocal low_size, high_size, low_sum, high_sum

            value = nums[idx]
            prune(low)

            if not low or value <= -low[0][0]:
                heapq.heappush(low, (-value, idx))
                where[idx] = 0
                low_size += 1
                low_sum += value
            else:
                heapq.heappush(high, (value, idx))
                where[idx] = 1
                high_size += 1
                high_sum += value

            rebalance()

        def remove(idx: int) -> None:
            nonlocal low_size, high_size, low_sum, high_sum

            value = nums[idx]
            removed[idx] = True

            if where[idx] == 0:
                low_size -= 1
                low_sum -= value
            else:
                high_size -= 1
                high_sum -= value

            rebalance()

        def current_cost() -> int:
            prune(low)
            prune(high)

            median = -low[0][0]
            return (
                median * low_size
                - low_sum
                + high_sum
                - median * high_size
            )

        window_cost = [0] * window_count

        for i in range(x):
            add(i)
        window_cost[0] = current_cost()

        for start in range(1, window_count):
            remove(start - 1)
            add(start + x - 1)
            window_cost[start] = current_cost()

        inf = 10**30

        # prev[end] is the minimum cost for exactly the current number
        # of selected windows in nums[0:end].
        prev = [inf] * (n + 1)
        prev[0] = 0

        for _ in range(k):
            cur = [inf] * (n + 1)

            for end in range(1, n + 1):
                cur[end] = cur[end - 1]

                start = end - x
                if start >= 0 and prev[start] != inf:
                    cur[end] = min(
                        cur[end],
                        prev[start] + window_cost[start]
                    )

            prev = cur

        return prev[n]