from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Step 1: Compute next greater element (nxt) using monotonic stack
        # nxt[i] = smallest index > i with nums[nxt[i]] > nums[i], or n if none
        nxt = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            nxt[i] = stack[-1] if stack else n
            stack.append(i)
        
        # Step 2: Prefix sums for range sum queries
        ps = [0] * (n + 1)
        for i in range(n):
            ps[i + 1] = ps[i] + nums[i]
        
        # Step 3: Compute segment cost for each i
        # seg_cost[i] = cost to raise all elements in (i, nxt[i]) to nums[i]
        # If nxt[i] == n, the segment extends to the end of the array
        seg_cost = [0] * n
        for i in range(n):
            end = nxt[i]
            length = end - i - 1
            if length > 0:
                seg_sum = ps[end] - ps[i + 1]
                seg_cost[i] = nums[i] * length - seg_sum
            else:
                seg_cost[i] = 0
        
        # Step 4: Binary lifting tables
        max_log = n.bit_length()  # enough for n
        up = [[n] * max_log for _ in range(n + 1)]
        cost_up = [[0] * max_log for _ in range(n + 1)]
        
        for i in range(n):
            up[i][0] = nxt[i]
            cost_up[i][0] = seg_cost[i]
        # For index n (sentinel), up[n][*] = n, cost_up[n][*] = 0
        
        for j in range(1, max_log):
            for i in range(n + 1):
                mid = up[i][j - 1]
                up[i][j] = up[mid][j - 1]
                cost_up[i][j] = cost_up[i][j - 1] + cost_up[mid][j - 1]
        
        # Step 5: Function to compute cost for subarray [l, r]
        def get_cost(l: int, r: int) -> int:
            if l >= r:
                return 0
            current = l
            total = 0
            # Jump as far as possible while the ancestor is <= r
            for j in range(max_log - 1, -1, -1):
                nxt_node = up[current][j]
                if nxt_node <= r:
                    total += cost_up[current][j]
                    current = nxt_node
            # Now 'current' is the last peak <= r; compute partial cost from current to r
            # Partial segment: raise elements in (current, r] to nums[current]
            partial_len = r - current
            if partial_len > 0:
                partial_sum = ps[r + 1] - ps[current + 1]
                total += nums[current] * partial_len - partial_sum
            return total
        
        # Step 6: For each l, binary search maximal r such that cost(l, r) <= k
        ans = 0
        for l in range(n):
            lo, hi = l, n - 1
            # Find largest r in [l, n-1] with cost <= k
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if get_cost(l, mid) <= k:
                    lo = mid
                else:
                    hi = mid - 1
            ans += lo - l + 1
        
        return ans