from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(nums)
        k = len(target)
        
        # For each target, compute (cost, index) for all nums
        # cost = ((t - n % t) % t)
        candidates_per_target = []
        for t in target:
            lst = []
            for i, n in enumerate(nums):
                cost = (t - n % t) % t
                lst.append((cost, i))
            lst.sort()  # sort by cost ascending
            # Keep top K candidates (K bounded, e.g., 60)
            K = min(len(lst), 60)
            candidates_per_target.append(lst[:K])
        
        # Backtracking: assign each target a distinct num
        best = float('inf')
        used = [False] * m
        
        def dfs(idx: int, current_cost: int):
            nonlocal best
            # Prune if current cost already not better than best
            if current_cost >= best:
                return
            # If all targets assigned, update best
            if idx == k:
                best = current_cost
                return
            # Iterate over candidates for target idx
            for cost, num_idx in candidates_per_target[idx]:
                if used[num_idx]:
                    continue
                used[num_idx] = True
                dfs(idx + 1, current_cost + cost)
                used[num_idx] = False
                # Optional early break: if cost is 0, we can stop trying more expensive ones?
                # But other targets may also need this num, so don't break.
        
        dfs(0, 0)
        return best