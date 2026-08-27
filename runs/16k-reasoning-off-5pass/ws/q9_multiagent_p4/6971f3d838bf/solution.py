from typing import List
import math

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Segment Tree Node
        # Stores: (max_subarray_sum, max_prefix_sum, max_suffix_sum, total_sum)
        class Node:
            __slots__ = 'max_sub', 'max_pref', 'max_suff', 'total'
            def __init__(self, max_sub: int, max_pref: int, max_suff: int, total: int):
                self.max_sub = max_sub
                self.max_pref = max_pref
                self.max_suff = max_suff
                self.total = total
        
        # Merge two nodes
        def merge(left: Node, right: Node) -> Node:
            new_total = left.total + right.total
            new_max_pref = max(left.max_pref, left.total + right.max_pref)
            new_max_suff = max(right.max_suff, right.total + left.max_suff)
            new_max_sub = max(left.max_sub, right.max_sub, left.max_suff + right.max_pref)
            return Node(new_max_sub, new_max_pref, new_max_suff, new_total)
        
        # Build Segment Tree
        tree = [None] * (4 * n)
        
        def build(node: int, start: int, end: int) -> None:
            if start == end:
                val = nums[start]
                tree[node] = Node(val, val, val, val)
            else:
                mid = (start + end) // 2
                build(2 * node, start, mid)
                build(2 * node + 1, mid + 1, end)
                tree[node] = merge(tree[2 * node], tree[2 * node + 1])
        
        build(1, 0, n - 1)
        
        # Query Segment Tree for range [l, r]
        def query(node: int, start: int, end: int, l: int, r: int) -> Node:
            if r < start or end < l:
                return None
            
            if l <= start and end <= r:
                return tree[node]
            
            mid = (start + end) // 2
            p1 = query(2 * node, start, mid, l, r)
            p2 = query(2 * node + 1, mid + 1, end, l, r)
            
            if p1 is None:
                return p2
            if p2 is None:
                return p1
            
            return merge(p1, p2)
        
        # Precompute first and last occurrence of each element
        first_occurrence = {}
        last_occurrence = {}
        for i, x in enumerate(nums):
            if x not in first_occurrence:
                first_occurrence[x] = i
            last_occurrence[x] = i
        
        unique_elements = list(first_occurrence.keys())
        
        # Initialize answer with the max subarray sum of the original array (case: no operation)
        ans = tree[1].max_sub
        
        for x in unique_elements:
            first = first_occurrence[x]
            last = last_occurrence[x]
            
            # The array after removing x consists of:
            # Left part: [0, first-1]
            # Middle part: [first+1, last-1] (elements between first and last occurrence)
            # Right part: [last+1, n-1]
            
            # We need to combine these three parts.
            # If a part is empty, we skip it.
            
            # Query Left
            if first > 0:
                left_node = query(1, 0, n - 1, 0, first - 1)
            else:
                left_node = None
            
            # Query Middle
            if first + 1 <= last - 1:
                mid_node = query(1, 0, n - 1, first + 1, last - 1)
            else:
                mid_node = None
            
            # Query Right
            if last + 1 < n:
                right_node = query(1, 0, n - 1, last + 1, n - 1)
            else:
                right_node = None
            
            # Combine nodes
            # Order: Left -> Middle -> Right
            
            current_node = left_node
            if mid_node is not None:
                if current_node is None:
                    current_node = mid_node
                else:
                    current_node = merge(current_node, mid_node)
            
            if right_node is not None:
                if current_node is None:
                    current_node = right_node
                else:
                    current_node = merge(current_node, right_node)
            
            if current_node is not None:
                ans = max(ans, current_node.max_sub)
        
        return ans