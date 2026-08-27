from typing import List

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # DSU implementation
        parent = {}
        
        def find(x):
            # Path compression
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            rootX = find(x)
            rootY = find(y)
            if rootX != rootY:
                parent[rootX] = rootY
                return True
            return False
        
        # Filter numbers <= threshold. Numbers > threshold are isolated components.
        # Any number x > threshold cannot form an edge with any y >= 1 because lcm(x, y) >= x > threshold.
        relevant_nums = [x for x in nums if x <= threshold]
        isolated_count = len(nums) - len(relevant_nums)
        
        # Initialize DSU for relevant numbers
        for x in relevant_nums:
            parent[x] = x
        
        # We need a fast lookup for relevant_nums to check existence of multiples
        relevant_set = set(relevant_nums)
        
        # Iterate through each number v in relevant_nums
        # For each v, check its multiples k*v that are also in relevant_nums.
        # The condition for an edge is lcm(v, k*v) <= threshold.
        # Since lcm(v, k*v) = k*v, we only need to check if k*v <= threshold.
        # This avoids O(N^2) checks and leverages the small threshold constraint.
        for v in relevant_nums:
            # Start from k=2 because k=1 is v itself (no edge to self needed)
            k = 2
            while k * v <= threshold:
                multiple = k * v
                if multiple in relevant_set:
                    union(v, multiple)
                k += 1
        
        # Count components in the relevant set
        components_in_relevant = 0
        for x in relevant_nums:
            if parent[x] == x:
                components_in_relevant += 1
        
        return components_in_relevant + isolated_count