from typing import List
import math

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        n = len(nums)
        m = len(target)
        
        # For each target, compute cost for every nums[i] to become a multiple of that target.
        # Keep only the L cheapest candidates per target.
        L = 30  # number of best candidates per target to keep
        cand = []  # cand[t] = list of (cost, idx) sorted by cost
        for t in target:
            costs = []
            for idx, val in enumerate(nums):
                # smallest multiple of t >= val
                mult = ((val + t - 1) // t) * t
                cost = mult - val
                costs.append((cost, idx))
            # sort by cost
            costs.sort(key=lambda x: (x[0], x[1]))
            # keep top L
            cand.append(costs[:L])
        
        # Sort targets by their best candidate cost (ascending) to improve pruning.
        order = sorted(range(m), key=lambda i: cand[i][0][0])
        
        used = set()
        best = [math.inf]
        
        # Lower bound: sum of minimum costs of remaining targets (ignoring conflicts)
        # We'll compute this incrementally.
        def lower_bound(pos):
            # pos is the current depth (number of targets already assigned)
            total = 0
            for j in range(pos, m):
                t_idx = order[j]
                total += cand[t_idx][0][0]
            return total
        
        def dfs(pos, current_cost):
            if current_cost >= best[0]:
                return
            if pos == m:
                if current_cost < best[0]:
                    best[0] = current_cost
                return
            
            # Lower bound check
            if current_cost + lower_bound(pos) >= best[0]:
                return
            
            t_idx = order[pos]
            # Try candidates for this target
            # We can try all candidates, but to speed up, we can also stop early if the current best cost + remaining minimum > best
            for cost, idx in cand[t_idx]:
                if idx in used:
                    continue
                # Early pruning: if current_cost + cost already exceeds best, skip
                if current_cost + cost >= best[0]:
                    # Since candidates are sorted by cost, further candidates only increase cost
                    break
                used.add(idx)
                dfs(pos + 1, current_cost + cost)
                used.remove(idx)
        
        dfs(0, 0)
        return best[0]