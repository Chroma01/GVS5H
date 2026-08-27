from typing import List
import math
import itertools

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        
        def lcm(a, b):
            if a == 0 or b == 0:
                return 0
            return abs(a * b) // gcd(a, b)
        
        def get_lcm_list(lst):
            result = 1
            for x in lst:
                result = lcm(result, x)
            return result
        
        def min_ops_for_multiple(nums, multiple):
            if multiple == 0:
                return 0
            min_ops = float('inf')
            for n in nums:
                if n % multiple == 0:
                    return 0
                else:
                    rem = n % multiple
                    ops = multiple - rem
                    if ops < min_ops:
                        min_ops = ops
            return min_ops
        
        n = len(target)
        if n == 0:
            return 0
        
        # Generate all unique partitions of target indices
        # Since n <= 4, we can iterate through all assignments and canonicalize
        all_partitions = set()
        for assignment in itertools.product(range(n), repeat=n):
            groups = {}
            for i, g_id in enumerate(assignment):
                if g_id not in groups:
                    groups[g_id] = []
                groups[g_id].append(i)
            # Canonicalize: sort indices within groups, then sort the groups themselves
            sorted_groups = sorted([sorted(groups[k]) for k in groups])
            all_partitions.add(tuple(sorted_groups))
        
        min_total_ops = float('inf')
        
        for partition in all_partitions:
            current_ops = 0
            for group_indices in partition:
                group_targets = [target[i] for i in group_indices]
                group_lcm = get_lcm_list(group_targets)
                ops = min_ops_for_multiple(nums, group_lcm)
                current_ops += ops
            
            if current_ops < min_total_ops:
                min_total_ops = current_ops
        
        return min_total_ops