from typing import List
from bisect import bisect_left, bisect_right

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ps = [0] * (n + 1)
        for i in range(n):
            ps[i+1] = ps[i] + nums[i]
        
        def solve(l: int, r: int) -> int:
            if l == r:
                return 1
            m = (l + r) // 2
            ans = solve(l, m) + solve(m+1, r)
            if m < r:
                # Build right side segments
                right_start = m + 1
                right_end = r
                # Compute suffix max for right side
                suff_max = []
                cur = -10**18
                for idx in range(right_start, right_end + 1):
                    if nums[idx] > cur:
                        cur = nums[idx]
                    suff_max.append(cur)
                # Build segments
                segments = []
                i = right_start
                while i <= right_end:
                    start = i
                    val = suff_max[i - right_start]
                    length = 0
                    sum_nums = 0
                    while i <= right_end and suff_max[i - right_start] == val:
                        length += 1
                        sum_nums += nums[i]
                        i += 1
                    segments.append((val, length, sum_nums, start))
                # Extract arrays
                seg_vals = [s[0] for s in segments]
                seg_lens = [s[1] for s in segments]
                seg_sums = [s[2] for s in segments]
                seg_starts = [s[3] for s in segments]
                n_seg = len(segments)
                len_pref = [0] * n_seg
                sum_pref = [0] * n_seg
                val_sum_pref = [0] * n_seg
                for idx in range(n_seg):
                    l_val = seg_lens[idx]
                    s_val = seg_sums[idx]
                    v_val = seg_vals[idx]
                    if idx == 0:
                        len_pref[idx] = l_val
                        sum_pref[idx] = s_val
                        val_sum_pref[idx] = v_val * l_val - s_val
                    else:
                        len_pref[idx] = len_pref[idx-1] + l_val
                        sum_pref[idx] = sum_pref[idx-1] + s_val
                        val_sum_pref[idx] = val_sum_pref[idx-1] + v_val * l_val - s_val
                
                def g(A: int, j: int) -> int:
                    # j must be >= right_start
                    s = bisect_right(seg_starts, j) - 1
                    s0 = bisect_left(seg_vals, A)
                    if s <= s0:
                        if s > 0:
                            total_len = len_pref[s-1]
                            total_sum = sum_pref[s-1]
                        else:
                            total_len = 0
                            total_sum = 0
                        full_contrib = A * total_len - total_sum
                    else:
                        if s0 > 0:
                            total_len_s0 = len_pref[s0-1]
                            total_sum_s0 = sum_pref[s0-1]
                            full_contrib = A * total_len_s0 - total_sum_s0
                        else:
                            full_contrib = 0
                        if s > s0:
                            if s0 > 0:
                                full_contrib += val_sum_pref[s-1] - val_sum_pref[s0-1]
                            else:
                                full_contrib += val_sum_pref[s-1]
                    seg_start = seg_starts[s]
                    count = j - seg_start + 1
                    sum_nums_partial = ps[j+1] - ps[seg_start]
                    partial_contrib = max(A, seg_vals[s]) * count - sum_nums_partial
                    return full_contrib + partial_contrib
                
                # Count crossing subarrays
                ans_cross = 0
                j = r
                left_stack = []
                cur_cost = 0
                for i in range(m, l-1, -1):
                    new_val = nums[i]
                    new_len = 1
                    new_sum = nums[i]
                    while left_stack and new_val >= left_stack[-1][0]:
                        next_val, next_len, next_sum = left_stack.pop()
                        cur_cost -= (next_val * next_len - next_sum)
                        new_len += next_len
                        new_sum += next_sum
                    cur_cost += (new_val * new_len - new_sum)
                    left_stack.append((new_val, new_len, new_sum))
                    left_max_i = new_val
                    left_cost_i = cur_cost
                    
                    while j >= m+1 and left_cost_i + g(left_max_i, j) > k:
                        j -= 1
                    if j < m+1:
                        break
                    ans_cross += (j - m)
                ans += ans_cross
            return ans
        
        return solve(0, n-1)