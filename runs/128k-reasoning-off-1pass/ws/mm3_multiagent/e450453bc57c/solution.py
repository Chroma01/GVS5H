from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1
        
        # Coordinate compression
        vals = sorted(set(nums))
        coord = {v: i+1 for i, v in enumerate(vals)}
        size = len(vals)
        
        class BIT:
            def __init__(self, size):
                self.n = size
                self.tree = [0] * (size + 1)
            def update(self, i, delta):
                while i <= self.n:
                    self.tree[i] += delta
                    i += i & -i
            def query(self, i):
                s = 0
                while i > 0:
                    s += self.tree[i]
                    i -= i & -i
                return s
            def find_kth(self, k):
                idx = 0
                bit_mask = 1 << (self.n.bit_length() - 1)
                while bit_mask:
                    t = idx + bit_mask
                    if t <= self.n and self.tree[t] < k:
                        idx = t
                        k -= self.tree[t]
                    bit_mask >>= 1
                return idx + 1
        
        count_bt = BIT(size)
        sum_bt = BIT(size)
        total_sum = 0
        
        # Initialize first window
        for i in range(x):
            v = nums[i]
            idx = coord[v]
            count_bt.update(idx, 1)
            sum_bt.update(idx, v)
            total_sum += v
        
        cost = [0] * m
        target = (x + 1) // 2  # 1-indexed position of median
        
        def compute_current_cost():
            med_idx = count_bt.find_kth(target)
            med_val = vals[med_idx - 1]
            L = count_bt.query(med_idx - 1)
            sumL = sum_bt.query(med_idx - 1)
            count_eq = count_bt.query(med_idx) - L
            R = x - L - count_eq
            sumR = total_sum - sumL - med_val * count_eq
            return med_val * L - sumL + sumR - med_val * R
        
        cost[0] = compute_current_cost()
        
        for i in range(1, m):
            # Slide window: remove nums[i-1], add nums[i+x-1]
            out_v = nums[i-1]
            out_idx = coord[out_v]
            count_bt.update(out_idx, -1)
            sum_bt.update(out_idx, -out_v)
            
            in_v = nums[i + x - 1]
            in_idx = coord[in_v]
            count_bt.update(in_idx, 1)
            sum_bt.update(in_idx, in_v)
            total_sum += in_v - out_v
            
            cost[i] = compute_current_cost()
        
        # DP to select k non-overlapping windows
        INF = 10**18
        dp_prev = [0] + [INF] * n
        for t in range(1, k + 1):
            dp_curr = [INF] * (n + 1)
            best = INF
            for i in range(1, n + 1):
                if i >= x:
                    cand = dp_prev[i - x] + cost[i - x]
                    if cand < best:
                        best = cand
                # dp_curr[i] = min(dp_curr[i-1], best)
                if dp_curr[i-1] < best:
                    dp_curr[i] = dp_curr[i-1]
                else:
                    dp_curr[i] = best
            dp_prev = dp_curr
        
        return dp_prev[n]