from typing import List
import heapq
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Deduplicate targets: covering a value once is enough.
        target = list(dict.fromkeys(target))
        m = len(target)
        size = 1 << m
        full = size - 1

        # lcm for every nonempty subset of targets.
        lcm = [1] * size
        for mask in range(1, size):
            l = 1
            for i in range(m):
                if mask & (1 << i):
                    l = l * target[i] // gcd(l, target[i])
            lcm[mask] = l

        # An optimal (inclusion-minimal) solution uses at most m elements,
        # so for each subset only the m cheapest elements can ever be needed.
        K = m
        heaps = [[] for _ in range(size)]  # max-heaps (stores -cost)
        for idx, v in enumerate(nums):
            for mask in range(1, size):
                c = (-v) % lcm[mask]   # cost to raise v to next multiple of lcm
                hp = heaps[mask]
                if len(hp) < K:
                    heapq.heappush(hp, (-c, idx))
                elif -hp[0][0] > c:
                    heapq.heapreplace(hp, (-c, idx))

        candidates = set()
        for mask in range(1, size):
            for _, idx in heaps[mask]:
                candidates.add(idx)

        # 0/1 bitmask DP over the union of candidate elements.
        INF = float('inf')
        dp = [INF] * size
        dp[0] = 0
        for idx in candidates:
            v = nums[idx]
            costs = [0] * size
            for mask in range(1, size):
                costs[mask] = (-v) % lcm[mask]
            ndp = dp[:]  # optionally skip this element
            for mask in range(size):
                base = dp[mask]
                if base == INF:
                    continue
                for S in range(1, size):
                    nm = mask | S
                    val = base + costs[S]
                    if val < ndp[nm]:
                        ndp[nm] = val
            dp = ndp

        return dp[full]