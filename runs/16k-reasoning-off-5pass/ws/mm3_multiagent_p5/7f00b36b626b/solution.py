from typing import List
from collections import defaultdict

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.size[px] < self.size[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]

class Solution:
    def countComponents(self, nums: List[int], threshold: int) -> int:
        # Count large numbers (isolated components)
        large_count = 0
        small_nums = []  # values <= threshold
        
        for num in nums:
            if num > threshold:
                large_count += 1
            else:
                small_nums.append(num)
        
        n_small = len(small_nums)
        if n_small <= 1:
            return large_count + n_small
        
        # Sieve: for each multiple k up to threshold, collect indices of values dividing it
        divisors_of_k = [[] for _ in range(threshold + 1)]
        for i, v in enumerate(small_nums):
            for multiple in range(v, threshold + 1, v):
                divisors_of_k[multiple].append(i)
        
        # Union all indices that share a common multiple
        dsu = DSU(n_small)
        for k in range(1, threshold + 1):
            if len(divisors_of_k[k]) >= 2:
                first = divisors_of_k[k][0]
                for idx in divisors_of_k[k][1:]:
                    dsu.union(first, idx)
        
        # Count distinct roots among small_nums
        roots = set()
        for i in range(n_small):
            roots.add(dsu.find(i))
        
        return large_count + len(roots)


# Test the solution with the given examples
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    nums1 = [2, 4, 8, 3, 9]
    threshold1 = 5
    result1 = sol.countComponents(nums1, threshold1)
    print(f"Example 1: {result1} (expected 4) - {'PASS' if result1 == 4 else 'FAIL'}")
    
    # Example 2
    nums2 = [2, 4, 8, 3, 9, 12]
    threshold2 = 10
    result2 = sol.countComponents(nums2, threshold2)
    print(f"Example 2: {result2} (expected 2) - {'PASS' if result2 == 2 else 'FAIL'}")
    
    # Additional test cases
    # All numbers > threshold
    nums3 = [100, 200, 300]
    threshold3 = 50
    result3 = sol.countComponents(nums3, threshold3)
    print(f"Test 3 (all > threshold): {result3} (expected 3) - {'PASS' if result3 == 3 else 'FAIL'}")
    
    # Single number
    nums4 = [5]
    threshold4 = 10
    result4 = sol.countComponents(nums4, threshold4)
    print(f"Test 4 (single num): {result4} (expected 1) - {'PASS' if result4 == 1 else 'FAIL'}")
    
    # Number 1 connects to everything
    nums5 = [1, 2, 3, 5]
    threshold5 = 5
    result5 = sol.countComponents(nums5, threshold5)
    print(f"Test 5 (contains 1): {result5} (expected 1) - {'PASS' if result5 == 1 else 'FAIL'}")
    
    # Numbers that don't share multiples
    nums6 = [7, 11, 13]
    threshold6 = 20
    result6 = sol.countComponents(nums6, threshold6)
    print(f"Test 6 (primes > threshold/2): {result6} (expected 3) - {'PASS' if result6 == 3 else 'FAIL'}")