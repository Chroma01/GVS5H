from typing import List
from collections import defaultdict

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        
        # Standard Kadane for the no-removal case
        max_ending = max_sofar = nums[0]
        for i in range(1, n):
            max_ending = max(nums[i], max_ending + nums[i])
            max_sofar = max(max_sofar, max_ending)
        
        NEG_INF = -10**18
        
        size = 1
        while size < n:
            size *= 2
        tree = [[NEG_INF, NEG_INF, NEG_INF, NEG_INF] for _ in range(2 * size)]
        
        for i in range(n):
            v = nums[i]
            tree[size + i] = [v, v, v, v]
        
        for i in range(size - 1, 0, -1):
            left_node = tree[2*i]
            right_node = tree[2*i+1]
            if left_node[0] == NEG_INF:
                tree[i] = right_node[:]
            elif right_node[0] == NEG_INF:
                tree[i] = left_node[:]
            else:
                total = left_node[0] + right_node[0]
                max_prefix = max(left_node[1], left_node[0] + right_node[1])
                max_suffix = max(right_node[2], right_node[0] + left_node[2])
                max_subarray = max(left_node[3], right_node[3], left_node[2] + right_node[1])
                tree[i] = [total, max_prefix, max_suffix, max_subarray]
        
        def query(l, r):
            if l > r:
                return NEG_INF
            l += size
            r += size
            left_res = None
            right_res = None
            while l <= r:
                if l % 2 == 1:
                    if left_res is None:
                        left_res = tree[l][:]
                    else:
                        a, b = left_res, tree[l]
                        if a[0] == NEG_INF:
                            left_res = b[:]
                        elif b[0] == NEG_INF:
                            left_res = a[:]
                        else:
                            total = a[0] + b[0]
                            max_prefix = max(a[1], a[0] + b[1])
                            max_suffix = max(b[2], b[0] + a[2])
                            max_subarray = max(a[3], b[3], a[2] + b[1])
                            left_res = [total, max_prefix, max_suffix, max_subarray]
                    l += 1
                if r % 2 == 0:
                    if right_res is None:
                        right_res = tree[r][:]
                    else:
                        a, b = tree[r], right_res
                        if a[0] == NEG_INF:
                            right_res = b[:]
                        elif b[0] == NEG_INF:
                            right_res = a[:]
                        else:
                            total = a[0] + b[0]
                            max_prefix = max(a[1], a[0] + b[1])
                            max_suffix = max(b[2], b[0] + a[2])
                            max_subarray = max(a[3], b[3], a[2] + b[1])
                            right_res = [total, max_prefix, max_suffix, max_subarray]
                    r -= 1
                l //= 2
                r //= 2
            if left_res is None:
                return right_res[3] if right_res else NEG_INF
            if right_res is None:
                return left_res[3]
            a, b = left_res, right_res
            if a[0] == NEG_INF:
                return b[3]
            if b[0] == NEG_INF:
                return a[3]
            total = a[0] + b[0]
            max_prefix = max(a[1], a[0] + b[1])
            max_suffix = max(b[2], b[0] + a[2])
            max_subarray = max(a[3], b[3], a[2] + b[1])
            return max_subarray
        
        positions = defaultdict(list)
        for i, v in enumerate(nums):
            positions[v].append(i)
        
        result = max_sofar
        
        for x, pos_list in positions.items():
            if len(pos_list) == n:
                continue
            ans_x = NEG_INF
            start = 0
            for p in pos_list:
                if p > start:
                    val = query(start, p - 1)
                    ans_x = max(ans_x, val)
                start = p + 1
            if start < n:
                val = query(start, n - 1)
                ans_x = max(ans_x, val)
            result = max(result, ans_x)
        
        return result