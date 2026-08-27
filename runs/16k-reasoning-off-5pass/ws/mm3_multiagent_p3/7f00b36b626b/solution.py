from typing import List
from math import gcd

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        n = len(nums)
        
        # Map value -> index for all unique nums
        val_to_idx = {v: i for i, v in enumerate(nums)}
        
        dsu = DSU(n)
        
        # Track which indices are "small" (value <= threshold)
        is_small = [v <= threshold for v in nums]
        
        # For small numbers: union if lcm(a, b) <= threshold
        # Strategy: for each small a, iterate multiples k*a up to threshold
        # If k*a is in the set, union them.
        # To get O(threshold * H(threshold)) complexity, iterate a in sorted order
        # and for each a, iterate k from 2 upward while k*a <= threshold.
        
        # Create mapping from small value to its index in nums
        small_val_to_idx = {v: i for i, v in enumerate(nums) if v <= threshold}
        
        # For fast lookup, use a boolean array of size threshold+1
        # But threshold can be up to 2*10^5, which is fine
        # Actually, we can iterate through sorted small values
        
        small_values = sorted(small_val_to_idx.keys())
        
        # Precompute: for each multiple m <= threshold, is it in the small set?
        # We can use a set for O(1) lookup
        small_set = set(small_values)
        
        for a in small_values:
            # Iterate multiples of a: 2*a, 3*a, ... up to threshold
            k = 2
            while k * a <= threshold:
                m = k * a
                if m in small_val_to_idx:
                    dsu.union(small_val_to_idx[a], small_val_to_idx[m])
                k += 1
        
        # Large numbers (> threshold) are isolated components
        # because lcm(a, b) >= max(a, b) > threshold for any b > threshold
        
        # Count unique roots
        roots = set()
        for i, v in enumerate(nums):
            if is_small[i]:
                roots.add(dsu.find(i))
            else:
                # Large numbers are their own component
                # But if there are duplicate large values? No, nums are unique.
                # So each large number is its own component.
                # However, if multiple large numbers have the same value... no, unique.
                # So just add the index as its own root.
                # But wait: could two large numbers be in the same component? No, as proven.
                # Could a large number be in the same component as a small number? No, as proven.
                # So we can just count them.
                # But to be safe with the DSU, we don't union them with anything.
                # So we just count them as separate components.
                # Actually, since we never union large numbers with anything,
                # each large number's find() is itself, so we can just add i.
                # But to avoid confusion, let's just add the index directly.
                pass
        
        # Count small components
        small_roots = set()
        for i, v in enumerate(nums):
            if is_small[i]:
                small_roots.add(dsu.find(i))
        
        num_small_components = len(small_roots)
        num_large_components = sum(1 for v in nums if v > threshold)
        
        return num_small_components + num_large_components


# Verification with examples and edge cases
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    nums1 = [2, 4, 8, 3, 9]
    threshold1 = 5
    # Expected: 4
    # Components: (2,4), (8), (3), (9)
    # Wait: 2 and 4: lcm(2,4)=4 <=5, union
    # 8: lcm(2,8)=8>5, lcm(4,8)=8>5, so isolated
    # 3: lcm(3,2)=6>5, lcm(3,4)=12>5, lcm(3,8)=24>5, lcm(3,9)=9>5, isolated
    # 9: lcm(9,3)=9>5, lcm(9,2)=18>5, lcm(9,4)=36>5, lcm(9,8)=72>5, isolated
    # So components: {2,4}, {8}, {3}, {9} = 4
    print(f"Example 1: {sol.countComponents(nums1, threshold1)} (expected 4)")
    
    # Example 2
    nums2 = [2, 4, 8, 3, 9, 12]
    threshold2 = 10
    # Expected: 2
    # Components: (2,3,4,8,9) and (12)
    # Let's check:
    # 2 connects to 4 (lcm=4<=10), to 8 (lcm=8<=10), to 3 (lcm=6<=10), to 9 (lcm=18>10)
    # 4 connects to 2, to 8 (lcm=8<=10), to 3 (lcm=12>10), to 9 (lcm=36>10)
    # 8 connects to 2 (lcm=8<=10), to 4 (lcm=8<=10), to 3 (lcm=24>10), to 9 (lcm=72>10)
    # 3 connects to 2 (lcm=6<=10), to 9 (lcm=9<=10), to 4 (lcm=12>10), to 8 (lcm=24>10)
    # 9 connects to 3 (lcm=9<=10), to 2 (lcm=18>10)
    # So: 2-4-8 connected, 3-9 connected, 2 connected to 3? lcm(2,3)=6<=10 YES
    # So all of {2,3,4,8,9} connected via 2-3 edge
    # 12: lcm(12,2)=12>10, lcm(12,3)=12>10, lcm(12,4)=12>10, lcm(12,8)=24>10, lcm(12,9)=36>10, isolated
    # So 2 components
    print(f"Example 2: {sol.countComponents(nums2, threshold2)} (expected 2)")
    
    # Edge case: all numbers > threshold
    nums3 = [100, 200, 300]
    threshold3 = 50
    # Each is isolated
    print(f"Edge case all large: {sol.countComponents(nums3, threshold3)} (expected 3)")
    
    # Edge case: all numbers <= threshold
    nums4 = [1, 2, 3, 4, 5, 6]
    threshold4 = 6
    # All connect via multiples
    # 1 connects to everything (lcm(1,x)=x<=6)
    # So all in one component
    print(f"Edge case all small: {sol.countComponents(nums4, threshold4)} (expected 1)")
    
    # Edge case: threshold = 1
    nums5 = [1, 2, 3]
    threshold5 = 1
    # Only 1 <= 1, others are large
    # 1 is its own component, 2 and 3 are large
    # Total: 3
    print(f"Edge case threshold=1: {sol.countComponents(nums5, threshold5)} (expected 3)")
    
    # Edge case: single element
    nums6 = [5]
    threshold6 = 5
    # 5 <= 5, one component
    print(f"Single element small: {sol.countComponents(nums6, threshold6)} (expected 1)")
    
    nums7 = [10]
    threshold7 = 5
    # 10 > 5, isolated
    print(f"Single element large: {sol.countComponents(nums7, threshold7)} (expected 1)")
    
    # Edge case: n=1, threshold large
    nums8 = [100000]
    threshold8 = 200000
    # 100000 <= 200000, one component
    print(f"Large threshold single: {sol.countComponents(nums8, threshold8)} (expected 1)")
    
    # Edge case: primes
    nums9 = [2, 3, 5, 7, 11]
    threshold9 = 10
    # 2,3,5,7 <= 10, 11 > 10
    # 2 connects to nothing (multiples 4,6,8,10 not in set, except check: 2*2=4 not in set, 2*3=6 not in set...)
    # Actually for a=2: 2*2=4 not in set, 2*3=6 not in set, 2*4=8 not in set, 2*5=10 not in set
    # So 2 isolated
    # 3: 3*2=6 not in set, 3*3=9 not in set. Isolated
    # 5: 5*2=10 not in set. Isolated
    # 7: 7*2=14>10. Isolated
    # 11 > 10, isolated
    # Total: 5
    print(f"Primes: {sol.countComponents(nums9, threshold9)} (expected 5)")
    
    # Edge case: coprime numbers
    nums10 = [2, 3]
    threshold10 = 6
    # lcm(2,3)=6 <=6, connected
    # 1 component
    print(f"Coprime: {sol.countComponents(nums10, threshold10)} (expected 1)")
    
    # Edge case: consecutive numbers
    nums11 = [1, 2, 3, 4, 5]
    threshold11 = 5
    # 1 connects to all
    # So all connected, 1 component
    print(f"Consecutive: {sol.countComponents(nums11, threshold11)} (expected 1)")
    
    # Edge case: numbers around threshold
    nums12 = [4, 5, 6]
    threshold12 = 5
    # 4,5 <=5, 6>5
    # 4 and 5: lcm(4,5)=20>5, not connected
    # So {4}, {5}, {6} = 3
    print(f"Around threshold: {sol.countComponents(nums12, threshold12)} (expected 3)")