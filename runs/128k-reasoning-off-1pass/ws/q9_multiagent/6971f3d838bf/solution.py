from typing import List
from collections import defaultdict

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Determine size for segment tree (power of 2)
        size = 1
        while size < n:
            size *= 2
        
        # Use a large negative number for -infinity
        NEG_INF = -10**18 
        
        # Tree array to store nodes. Each node is a dictionary.
        tree = [None] * (2 * size)
        
        # Initialize leaves
        for i in range(n):
            tree[size + i] = {
                'l': i, 'r': i,
                'max_sub': nums[i],
                'max_pref': nums[i],
                'max_suff': nums[i],
                'total': nums[i]
            }
        # Initialize padding leaves with empty properties
        # Total sum of empty range is 0. Max subarray/prefix/suffix is -inf.
        for i in range(n, size):
            tree[size + i] = {
                'l': i, 'r': i,
                'max_sub': NEG_INF,
                'max_pref': NEG_INF,
                'max_suff': NEG_INF,
                'total': 0
            }
            
        # Build the tree bottom-up
        for i in range(size - 1, 0, -1):
            left = tree[2 * i]
            right = tree[2 * i + 1]
            
            node = {
                'l': left['l'],
                'r': right['r'],
                'total': left['total'] + right['total'],
                'max_pref': max(left['max_pref'], left['total'] + right['max_pref']),
                'max_suff': max(right['max_suff'], right['total'] + left['max_suff']),
                'max_sub': max(left['max_sub'], right['max_sub'], left['max_suff'] + right['max_pref'])
            }
            tree[i] = node
            
        # Function to query the max subarray sum in range [l, r]
        def query(node_idx, l, r):
            if l > r:
                return None
            
            # Check for no overlap
            if r < tree[node_idx]['l'] or l > tree[node_idx]['r']:
                return None
            
            # Check for full overlap
            if l <= tree[node_idx]['l'] and tree[node_idx]['r'] <= r:
                return tree[node_idx]
            
            mid = (tree[node_idx]['l'] + tree[node_idx]['r']) // 2
            left_res = query(2 * node_idx, l, r)
            right_res = query(2 * node_idx + 1, l, r)
            
            if left_res is None:
                return right_res
            if right_res is None:
                return left_res
            
            # Merge results
            res = {
                'total': left_res['total'] + right_res['total'],
                'max_pref': max(left_res['max_pref'], left_res['total'] + right_res['max_pref']),
                'max_suff': max(right_res['max_suff'], right_res['total'] + left_res['max_suff']),
                'max_sub': max(left_res['max_sub'], right_res['max_sub'], left_res['max_suff'] + right_res['max_pref'])
            }
            return res

        # Group indices by value
        indices_map = defaultdict(list)
        for i, x in enumerate(nums):
            indices_map[x].append(i)
            
        unique_elements = list(indices_map.keys())
        
        # Initial answer: global max subarray sum (equivalent to removing nothing)
        global_max = tree[1]['max_sub']
        ans = global_max
        
        for x in unique_elements:
            idxs = indices_map[x]
            current_max = NEG_INF
            
            # 1. Segment before the first occurrence of x
            if idxs[0] > 0:
                res = query(1, 0, idxs[0] - 1)
                if res:
                    current_max = max(current_max, res['max_sub'])
            
            # 2. Segment after the last occurrence of x
            if idxs[-1] < n - 1:
                res = query(1, idxs[-1] + 1, n - 1)
                if res:
                    current_max = max(current_max, res['max_sub'])
            
            # 3. Segments between consecutive occurrences of x
            for k in range(len(idxs) - 1):
                start = idxs[k] + 1
                end = idxs[k+1] - 1
                if start <= end:
                    res = query(1, start, end)
                    if res:
                        current_max = max(current_max, res['max_sub'])
            
            if current_max > ans:
                ans = current_max
                
        return ans