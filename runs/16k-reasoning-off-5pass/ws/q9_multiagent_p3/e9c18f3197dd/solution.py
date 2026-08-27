from typing import List
from math import gcd
from functools import reduce

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Helper to calculate LCM of two numbers
        def lcm(a, b):
            return (a * b) // gcd(a, b)
        
        # Helper to calculate LCM of a list of numbers
        def lcm_list(lst):
            return reduce(lcm, lst)
        
        # Generate all partitions of a list of indices
        # Each partition represents a grouping of targets that can be satisfied by a single nums element
        def get_partitions(items):
            if not items:
                yield []
                return
            
            first = items[0]
            rest = items[1:]
            
            # Option 1: Put first in its own group
            for p in get_partitions(rest):
                yield [[first]] + p
            
            # Option 2: Put first in each existing group of the partitions of rest
            for p in get_partitions(rest):
                for i in range(len(p)):
                    new_p = [group[:] for group in p]  # Deep copy of groups
                    new_p[i].append(first)
                    yield new_p
        
        indices = list(range(len(target)))
        all_partitions = list(get_partitions(indices))
        
        min_ops = float('inf')
        
        for partition in all_partitions:
            num_groups = len(partition)
            group_candidates = []
            
            # For each group in the partition, find the best nums elements to satisfy it
            for group in partition:
                group_targets = [target[i] for i in group]
                group_lcm = lcm_list(group_targets)
                
                # We need to find nums elements that minimize the cost to become a multiple of group_lcm
                # Cost = (group_lcm - (x % group_lcm)) % group_lcm
                # We only need the top 'num_groups' best candidates because we have 'num_groups' groups to fill
                candidates = []
                for idx, x in enumerate(nums):
                    cost = (group_lcm - x % group_lcm) % group_lcm
                    candidates.append((cost, idx))
                
                # Sort by cost ascending
                candidates.sort(key=lambda p: p[0])
                # Take top num_groups candidates
                group_candidates.append(candidates[:num_groups])
            
            # Now solve the assignment problem: assign each group to a distinct nums element
            # Since num_groups is small (<= 4), we can use simple backtracking
            used_indices = set()
            
            def backtrack(group_idx, current_cost):
                if group_idx == num_groups:
                    return current_cost
                
                best_res = float('inf')
                # Try each candidate for the current group
                for cost, idx in group_candidates[group_idx]:
                    if idx not in used_indices:
                        used_indices.add(idx)
                        res = backtrack(group_idx + 1, current_cost + cost)
                        if res < best_res:
                            best_res = res
                        used_indices.remove(idx)
                        # Optimization: if we found a solution with 0 cost, we can't do better
                        if best_res == 0:
                            return 0
                return best_res
            
            total_ops = backtrack(0, 0)
            if total_ops < min_ops:
                min_ops = total_ops
        
        return min_ops if min_ops != float('inf') else 0

# Test cases
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    nums1 = [1, 2, 3]
    target1 = [4]
    result1 = sol.minimumIncrements(nums1, target1)
    print(f"Example 1: {result1} (Expected: 1)")
    
    # Example 2
    nums2 = [8, 4]
    target2 = [10, 5]
    result2 = sol.minimumIncrements(nums2, target2)
    print(f"Example 2: {result2} (Expected: 2)")
    
    # Example 3
    nums3 = [7, 9, 10]
    target3 = [7]
    result3 = sol.minimumIncrements(nums3, target3)
    print(f"Example 3: {result3} (Expected: 0)")
    
    # Additional test case: target elements can be satisfied by the same nums element
    nums4 = [2, 3]
    target4 = [2, 3]
    result4 = sol.minimumIncrements(nums4, target4)
    print(f"Additional 1: {result4} (Expected: 0)")
    
    # Additional test case: need to increment to satisfy multiple targets with one nums
    nums5 = [5]
    target5 = [2, 3]
    result5 = sol.minimumIncrements(nums5, target5)
    print(f"Additional 2: {result5} (Expected: 1 -> 5->6 satisfies 2 and 3? No, 6 is multiple of 2 and 3. Cost 1)")
    
    # Edge case: Large numbers
    nums6 = [10000]
    target6 = [10000]
    result6 = sol.minimumIncrements(nums6, target6)
    print(f"Edge case 1: {result6} (Expected: 0)")
    
    # Edge case: Need to increment significantly
    nums7 = [1]
    target7 = [100]
    result7 = sol.minimumIncrements(nums7, target7)
    print(f"Edge case 2: {result7} (Expected: 99)")