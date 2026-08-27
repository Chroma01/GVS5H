from typing import List

class Fenwick:
    """Fenwick tree for range add and point query."""
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def _add(self, i, delta):
        i += 1
        while i <= self.n + 1:
            self.bit[i] += delta
            i += i & -i

    def range_add(self, l, r, delta):
        if l > r:
            return
        self._add(l, delta)
        if r + 1 <= self.n:
            self._add(r + 1, -delta)

    def point_query(self, i):
        i += 1
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ft = Fenwick(n)
        # Monotonic decreasing stack: (value, index)
        stack = []
        stack_left = 0  # pointer to first valid element in stack
        total_original = 0
        total_effective = 0
        ans = 0
        l = 0
        current_max = 0  # current maximum value in the window
        
        for r in range(n):
            val = nums[r]
            total_original += val
            ft.range_add(r, r, val)
            total_effective += val
            
            # Update current max
            if val > current_max:
                current_max = val
            
            # Maintain decreasing stack: pop elements that are <= new value
            while stack_left < len(stack) and stack[-1][0] <= val:
                old_val, old_idx = stack.pop()
                if stack:
                    right = stack[-1][1] - 1
                else:
                    right = r - 1
                if old_idx <= right:
                    delta = val - old_val
                    ft.range_add(old_idx, right, delta)
                    total_effective += delta * (right - old_idx + 1)
            
            stack.append((val, r))
            
            # Shrink window from the left while the cost exceeds k
            while total_effective - total_original > k:
                eff_val = ft.point_query(l)
                ft.range_add(l, l, -eff_val)
                total_effective -= eff_val
                total_original -= nums[l]
                
                # If the leftmost valid stack element is at index l, 
                # advance the pointer and restore effective values for 
                # the segment that was under that max
                if stack_left < len(stack) and stack[stack_left][1] == l:
                    old_val, old_idx = stack[stack_left]
                    stack_left += 1
                    if stack_left < len(stack):
                        new_val = stack[stack_left][0]
                    else:
                        new_val = current_max
                    left = l + 1
                    if stack_left < len(stack):
                        right = stack[stack_left][1] - 1
                    else:
                        right = r
                    if left <= right:
                        delta = new_val - old_val
                        ft.range_add(left, right, delta)
                        total_effective += delta * (right - left + 1)
                
                l += 1
            
            ans += r - l + 1
        
        return ans